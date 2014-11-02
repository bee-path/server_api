from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie import fields

import GPS_updates.models as gmodels

from tastypie.exceptions import BadRequest

from tastypie.exceptions import BadRequest, ImmediateHttpResponse

from tastypie import http
import json


class ICUB_modelResource(ModelResource):
    class Meta:
        queryset = gmodels.ICUB_model.objects.all() # all gps_updates
        resource_name = 'ICUB'
        list_allowed_methods = ['get','post','patch'] # can post, can get, can patch (bulk insert)
        detail_allowed_methods = [] # can put (for bulk insert) 
        authentication= BasicAuthentication()
        authorization=Authorization()
        #authentication= SillyAuthentication()
        always_return_data = True
