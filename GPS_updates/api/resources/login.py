from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.contrib.auth import authenticate
from user_details import User_details

from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie import http
import json

from tastypie import http

class LoginResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user_log'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        list_allowed_methods = ['post']  #use list_allowed_methods and #detail_allowed_methods
        detail_allowed_methods = ['post']  #use list_allowed_methods and #detail_allowed_methods
        include_resource_uri = False        
        authorization = Authorization() # only reads
        authentication = Authentication()
        #authentication = ApiKeyAuthentication()
        filtering = {
            'username': ALL,
        }
        always_return_data = True


    def obj_create(self, bundle, **kwargs):
        try:
            # get user params
            email = bundle.data.get('email', None)
            username = bundle.data.get('username', None) 
            try:
                validate_email(email)
            except ValidationError:
                raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Email must be valid"}),content_type="application/json"))
            if User.objects.filter(email=email):
                raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"This email already has an associated account"}),content_type="application/json"))
            password = bundle.data.get('password', None)
            phone_os = bundle.data.get('phone_os', None)
            if not phone_os:
                phone_os = 'unknown'
            user = authenticate(username = username, password = password)
            try:
                if user.get_username() != username:
                    raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Cannot create new user identified as an another user"}),content_type="application/json"))
            except AttributeError: pass
            # check if user exists
            if user is not None:
                raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"User already exists"}),content_type="application/json"))
            #    if user.api_key is not None:
            #        api_key = user.api_key
            #    else:
            #        api_key = ApiKey.objects.create(user = user)
            else:
            # or creates a new user with User_details
                bundle = super(LoginResource, self).obj_create(bundle, **kwargs)
                bundle.obj.set_password(bundle.data.get('password', None))
                bundle.obj.email = email
                bundle.obj.save()
                age = bundle.data.get('age',0)
                gender = bundle.data.get('age','N') # unchecked
                alone = bundle.data.get('age',False)
                future_emails = bundle.data.get('future_emails',False)
                # authenticate user
                user = authenticate(username = username, password = password)
                # create user details
                details = User_details( user=user, phone_os=phone_os, age=age, alone=alone, future_emails = future_emails, gender = gender  )
                details.save()
                return bundle
                # create API key
                #api_key = ApiKey.objects.create(user = user)

        except IntegrityError:
            raise ImmediateHttpResponse(http.HttpBadRequest(json.dumps({'response':400,'message':"Something weird went on.."}),content_type="application/json"))
            #return null

