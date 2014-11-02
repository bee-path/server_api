from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication
from tastypie import fields

from gps_session import GPS_sessionResource
import GPS_updates.models as gmodels

from tastypie.exceptions import BadRequest

from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie import http
import json
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie import http
import json


class GPS_updateResource(ModelResource):
    session = fields.ForeignKey(GPS_sessionResource, 'session') # related to registered user
    class Meta:
        queryset = gmodels.GPS_update.objects.all() # all gps_updates
        resource_name = 'update'
        list_allowed_methods = ['get','post','patch'] # can post, can get, can patch (bulk insert)
        detail_allowed_methods = ['put'] # can put (for bulk insert)
        authentication= BasicAuthentication()
        authorization=Authorization()
        #authentication= SillyAuthentication()
        filtering = {
            'session': ALL_WITH_RELATIONS, # by session
            #'user': ALL, # redundant
        }
        ordering = ['time']
        always_return_data = True

    def hydrate_user(self, bundle): # overrides user field in creation
        bundle.data['user'] =  bundle.request.user
        return bundle
        
    def obj_create(self, bundle, **kwargs):
        if not bundle.request.user.is_active:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"User not active.Can't update!"}),content_type="application/json"))
        sess = gmodels.GPS_session.objects.filter(user = bundle.request.user, is_active = True).order_by('id')
        if len(sess)>1: # more than one
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Multiple sessions opened. Close them!"}),content_type="application/json"))
        elif not sess: # not opened sessions
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"No active sessions. Create one!"}),content_type="application/json"))
        sess = sess[0]
        if sess.is_finished:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Current session is closed.!"}),content_type="application/json"))
        if sess.is_interrupted:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Paused session, no updates allowed!"}),content_type="application/json"))
        #if not sess.is_active: --> not needed in principle
        #    raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Inactive session, no updates allowed!"}),content_type="application/json"))
        #if sess.id != bundle.data['session']:
        #    print "Ignoring session to active sessions"
        return super(GPS_updateResource, self).obj_create(bundle, session=sess)

    def get_object_list(self, request):
        """
        Overrides get_object_list to allow filtering
        """
        return self._meta.queryset.filter(session__user = request.user) # filtering over user


    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(session__user=request.user) # only over get method
