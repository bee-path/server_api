from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication
from django.contrib.auth.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name', 'last_login']
        list_allowed_methods = ['get']  #use list_allowed_methods and #detail_allowed_methods
        detail_allowed_methods = []  #use list_allowed_methods and #detail_allowed_methods
        include_resource_uri = False        
        authorization = ReadOnlyAuthorization() # only reads
        authentication = BasicAuthentication()
        #authentication = ApiKeyAuthentication()
        filtering = {
            'username': ALL,
        }
