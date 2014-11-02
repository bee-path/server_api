from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication

import GPS_updates.models as gmodels

### The ones that work fine ###
class TargetResource(ModelResource):
    class Meta:
        queryset = gmodels.Target.objects.all() # all gps_updates
        resource_name = 'target'
        allowed_methods = ['get'] #allows only allows posts (just need to check)
        authentication= BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True
        #no filtering needed
