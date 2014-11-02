from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication
from tastypie import fields
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie import http
import json
from user import UserResource
from gps_session import GPS_sessionResource
from target import TargetResource
import GPS_updates.models as gmodels



class Found_targetResource(ModelResource):
    session = fields.ForeignKey(GPS_sessionResource, 'session') # related to registered user
    target = fields.ForeignKey(TargetResource, 'target') # related to registered user
    #user = fields.ForeignKey(UserResource, 'user') # related to registered user
    class Meta:
        queryset = gmodels.Found_target.objects.all() # all gps_updates
        resource_name = 'found_target'
        list_allowed_methods = ['get','post'] # can post, can get
        detail_allowed_methods = [] # can only get
        authorization=Authorization()
        authentication= BasicAuthentication()
        #authentication= ApiKeyAuthentication()
        filtering = {
            'session': ALL_WITH_RELATIONS, # by session
        }
        ordering = ['classment','time_found']
        always_return_data = True

    #def dehydrate(self, bundle): # mar asked for this, shall take it off aferwards
    #    bundle.data['response'] = 200
    #    return bundle

    def hydrate_user(self, bundle): # overrides user field in creation
        bundle.data['user'] =  bundle.request.user
        return bundle

    def check_target(self, target):
        if not target:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Specify a target!"}),content_type="application/json"))
        target = gmodels.Target.objects.filter(id=target) # gets target
        if not target or len(target)>1:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"This target does not exist!"}),content_type="application/json"))            
        return target[0]
        

    def hydrate_target(self, bundle):
        bundle.data['target'] = self.check_target(bundle.data.get('target',None))
        return bundle

    #def obj_create(self, bundle, **kwargs):
        #tgt = super(Found_targetResource, self).obj_create(bundle, session=sess, user=bundle.request.user)
        #z = sess._add_target(tgt.obj.id)
        #if not z:
            ##Adding of target failed
            #raise BadRequest("Target already detected")
        #sess.save()
        #return tgt
            
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
        a = sess._add_target(self.check_target(bundle.data['target']))
        print sess.targets_list
        if a:
            sess.save()
            bundle.data['classment'] = sess.targets_found
            return super(Found_targetResource, self).obj_create(bundle, session=sess)
        else:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Target already registered!"}),content_type="application/json"))

    def get_object_list(self, request):
        """
        Overrides get_object_list to allow filtering
        """
        return self._meta.queryset.filter(session__user = request.user) # filtering over user


    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(session__user=request.user) # only over get method
