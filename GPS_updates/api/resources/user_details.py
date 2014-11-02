from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication
from tastypie import fields

from user import UserResource
from GPS_updates.models import User_details

class User_detailsResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full = True ) # related to registered user
    #sessions = fields.ToManyField('GPS_updates.api.resources.GPS_sessionResource', 'sessions', blank=True, null=True)
    class Meta:
        queryset = User_details.objects.all() # all gps_updates
        excludes = ['email'] # excludes email --> emails are defined as unique in the model, raises error 
        resource_name = 'user_details'
        list_allowed_methods = ['get'] #allows only gets on foreign users
        detail_allowed_methods = ['patch','get'] #allows gets and puts without limit, not posts (use 'create_user')
        include_resource_uri = False
        authorization  = Authorization() # all permissions
        #authentication = ApiKeyAuthentication() # works!
        authentication = BasicAuthentication() # works!
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'is_active': ALL,
            'total_time': ALL, # for rankings
            'total_length': ALL, # for rankings
            'alone' : ALL,
            'gender' : ALL,
            'age': ALL,
        }
        ordering = ['total_time', 'total_length']
        always_return_data = True


    def hydrate_user(self, bundle): # overrides user field in creation
        bundle.data['user'] =  bundle.request.user
        return bundle

    
    def obj_get(self, bundle, **kwargs): # we override the user (only gets allowed on own user)
        return super(User_detailsResource, self).obj_get(bundle, user=bundle.request.user)
        
    def obj_update(self, bundle, **kwargs): # we override the user (only puts allowed on own user)
        # security breach: make is_active read only
        return super(User_detailsResource, self).obj_update(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user) # only over get method
