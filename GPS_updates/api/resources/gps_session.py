from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication
from tastypie import fields

from user import UserResource
import GPS_updates.models as gmodels

from tastypie.exceptions import BadRequest

from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie import http
import json

from GPS_updates import get_results

class GPS_sessionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True) # related to registered user
    class Meta:
        queryset = gmodels.GPS_session.objects.all() # all gps_updates
        resource_name = 'session'
        list_allowed_methods = ['get','post'] # allows gets and posts on list
        detail_allowed_methods = ['get','patch'] # allows gets and posts and patchs without limit
        authorization = Authorization()
        # authorization = PerUserAuthorization()
        #authentication = ApiKeyAuthentication()
        authentication = BasicAuthentication()
        #authentication = Authentication()
        always_return_data = True
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'is_interrupted': ALL, # by interruption
            'is_active': ALL, # by active
            'is_finished': ALL, # by active
            'date_start': ALL, # by date
            'date_stop': ALL, # by date
        }
        ordering = ['total_time', 'total_length', 'date_start']

    def get_object_list(self, request):
        """
        Overrides get_object_list to allow filtering over user
        """
        return self._meta.queryset.filter(user=request.user)

    def hydrate_user(self, bundle): # overrides user field in creation --> unallow to get complete list of sessions
        bundle.data['user'] =  bundle.request.user
        return bundle

    def dehydrate(self, bundle):
        bundle.data['results'] = get_results.results(bundle.obj.total_length, bundle.obj.total_time, bundle.obj.targets_found)  
        return bundle
    #def hydrate(self, bundle):
        #if bundle.request.method == 'PATCH': # if patch, only allows start, stop, pause
            #b = bundle.data.get('is_interrupted', None)
            #c = bundle.data.get('is_finished', None)
            #a = bundle.data.get('is_active', None)
            #print a,b,c
            #if c:
                #b=False # Not interrupted
                #a=False # Not acrtive
            #else:
                #if b: #declared paused
                    #a = b = False
            #print a,b,c
            #bundle.data = {'is_active' : a, 'is_interrupted': b, 'is_finished':c}
        #return bundle

    def obj_create(self, bundle, **kwargs):
        if bundle.request.user.user_details.is_active: # If the user is active, does not allow
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"User already active. Close current session!"}),content_type="application/json"))
        bundle.request.user.user_details.is_active = True # activate
        sess = gmodels.GPS_session.objects.filter(user = bundle.request.user, is_active = True).order_by('id')
        if sess:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"User already active. Close current session!"}),content_type="application/json"))
        bundle.request.user.user_details.save() # save and proceed
        bundle.data['is_active'] = True # also sets session to active
        bundle.data['is_finished'] = False # also sets session to active
        bundle.data['is_interrupted'] = False # also sets session to active
        return super(GPS_sessionResource, self).obj_create(bundle, user=bundle.request.user)
    
    def obj_update(self, bundle, **kwargs): # we override the updates
        if bundle.obj.is_finished:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Can't modify a closed session"}),content_type="application/json"))
        if bundle.data['is_finished']: # if finished
            bundle.data['is_active'] = False # if interrupted, do not change
            bundle.obj.is_active = bundle.obj.is_interrupted = False
            bundle.obj.user.user_details.sessions_n +=1
            bundle.obj._compute_stats() # compute stats (it does compute statistics) # smelly hack...
            bundle.data['total_time']= bundle.obj.total_time
            bundle.data['total_length']= bundle.obj.total_length
            bundle.data['updates_n']= bundle.obj.updates_n
        else: #not finished command
            if bundle.data['is_interrupted']: # if pause command or paused
                if not bundle.obj.is_active:
                    if not bundle.data['is_active']:
                        raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Can't pause inactive session"}),content_type="application/json"))
                    else:
                        bundle.data['is_interrupted'] = bundle.obj.is_interrupted = False # restart
                else:
                    bundle.data['is_active'] = bundle.obj.is_active = False #pause
                    bundle.obj._compute_stats() # compute stats (it does compute statistics)
                    bundle.data['total_time']= bundle.obj.total_time
                    bundle.data['total_length']= bundle.obj.total_length
                    bundle.data['updates_n']= bundle.obj.updates_n

            else: # restart command
                if bundle.data['is_active']: #or not bundle.data['is_interrupted']    : # if session not active, activate
                    if bundle.obj.is_active:
                        raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Can't start an already active session."}),content_type="application/json"))
                    else: bundle.obj.is_active = True
                else:
                    raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"To pause a session, use is_interrupted command."}),content_type="application/json"))
        bundle.obj.user.user_details.is_active = bundle.obj.is_active # copy active status
        bundle.obj.user.user_details.save() # save and proceed      
        # here need to compute different stuff (total time and so on...)          
        return super(GPS_sessionResource, self).obj_update(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user) # only user
