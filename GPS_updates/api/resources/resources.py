# myapp/api.py
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.authentication import ApiKeyAuthentication, Authentication, BasicAuthentication
from authentification_custom import SillyAuthentication, PerUserAuthorization
from tastypie.exceptions import BadRequest, NotFound, ImmediateHttpResponse
import GPS_updates.models as gmodels

from django.contrib.auth.models import User
from tastypie import fields

import user as UserResource


# ### The ones that work fine ###
# class TargetResource(ModelResource):
#     class Meta:
#         queryset = gmodels.Target.objects.all() # all gps_updates
#         resource_name = 'target'
#         allowed_methods = ['get'] #allows only allows posts (just need to check)
#         authentication= BasicAuthentication()
#         authorization=ReadOnlyAuthorization()
#         #no filtering needed

# class User_detailsResource(ModelResource):
#     user = fields.ForeignKey(UserResource, 'user' ) # related to registered user
#     #sessions = fields.ToManyField('GPS_updates.api.resources.GPS_sessionResource', 'sessions', blank=True, null=True)
#     class Meta:
#         queryset = gmodels.User_details.objects.all() # all gps_updates
#         excludes = ['email'] # excludes email --> emails are defined as unique in the model, raises error 
#         resource_name = 'user_details'
#         list_allowed_methods = ['get'] #allows only gets on foreign users
#         detail_allowed_methods = ['patch','get'] #allows gets and puts without limit, not posts (use 'create_user')
#         include_resource_uri = False
#         authorization  = Authorization() # all permissions
#         #authentication = ApiKeyAuthentication() # works!
#         authentication = BasicAuthentication() # works!
#         filtering = {
#             'user': ALL_WITH_RELATIONS,
#             'is_active': ALL,
#             'total_time': ALL, # for rankings
#             'total_length': ALL, # for rankings
#         }
#         ordering = ['total_time', 'total_length']


#     def hydrate_user(self, bundle): # overrides user field in creation
#         bundle.data['user'] =  bundle.request.user
#         return bundle

#     def obj_get(self, bundle, **kwargs): # we override the user (only gets allowed on own user)
#         return super(User_detailsResource, self).obj_get(bundle, user=bundle.request.user)
        
#     def obj_update(self, bundle, **kwargs): # we override the user (only puts allowed on own user)
#         return super(User_detailsResource, self).obj_update(bundle, user=bundle.request.user)

#     def apply_authorization_limits(self, request, object_list):
#         return object_list.filter(user=request.user) # only over get method

# ########### Create things #################
# from django.db import IntegrityError, models
# from tastypie.models import create_api_key, ApiKey
# from django.contrib.auth import authenticate
# from datetime import datetime
# from GPS_updates.models import User_details
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError

# class LoginResource(ModelResource):
#     class Meta:
#         queryset = User.objects.all()
#         resource_name = 'user_log'
#         excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
#         list_allowed_methods = ['post']  #use list_allowed_methods and #detail_allowed_methods
#         detail_allowed_methods = ['post']  #use list_allowed_methods and #detail_allowed_methods
#         include_resource_uri = False        
#         authorization = Authorization() # only reads
#         authentication = Authentication()
#         #authentication = ApiKeyAuthentication()
#         filtering = {
#             'username': ALL,
#         }

#         always_return_data = False

#     def obj_create(self, bundle, **kwargs):
#         try:
#             # get user params
#             username = bundle.data.get('username', None)
#             email = username
#             try:
#                 validate_email(email)
#             except ValidationError:
#                 raise BadRequest('Username must be an email')
#             password = bundle.data.get('password', None)
#             phone_os = bundle.data.get('phone_os', None)
#             if not phone_os:
#                 phone_os = 'unknown'
#             user = authenticate(username = username, password = password )

#             # check if user exists
#             if user is not None:
#                 raise BadRequest('User already exists')
#             #    if user.api_key is not None:
#             #        api_key = user.api_key
#             #    else:
#             #        api_key = ApiKey.objects.create(user = user)
#             else:
#             # or creates a new user with User_details
#                 bundle = super(LoginResource, self).obj_create(bundle, **kwargs)
#                 bundle.obj.set_password(bundle.data.get('password', None))
#                 bundle.email = email
#                 bundle.obj.save()

#                 # authenticate user
#                 user = authenticate(username = username, password = password )

#                 # create user details
#                 details = User_details( update_rate=15, user=user, phone_os=phone_os)
#                 details.save()
#                 return bundle
#                 # create API key
#                 #api_key = ApiKey.objects.create(user = user)

#         except IntegrityError:
#             raise BadRequest('Could not create or authenticate user')
#             #return null

#######################################
#######################################
# class GPS_sessionResource(ModelResource):
#     user = fields.ForeignKey(UserResource, 'user') # related to registered user
#     class Meta:
#         queryset = gmodels.GPS_session.objects.all() # all gps_updates
#         resource_name = 'session'
#         list_allowed_methods = ['get','post'] # allows gets and posts on list
#         detail_allowed_methods = ['get','patch'] # allows gets and posts and patchs without limit
#         authorization = Authorization()
#         # authorization = PerUserAuthorization()
#         #authentication = ApiKeyAuthentication()
#         authentication = BasicAuthentication()
#         #authentication = Authentication()
#         filtering = {
#             'user': ALL_WITH_RELATIONS,
#             'is_interrupted': ALL, # by interruption
#             'is_active': ALL, # by active
#             'is_finished': ALL, # by active
#             'date_start': ALL, # by date
#             'date_stop': ALL, # by date
#         }
#         ordering = ['total_time', 'total_length', 'date_start']
#         always_return_data = True

#     def get_object_list(self, request):
#         """
#         Overrides get_object_list to allow filtering over user
#         """
#         return self._meta.queryset.filter(user=request.user)

#     def hydrate_user(self, bundle): # overrides user field in creation
#         bundle.data['user'] =  bundle.request.user
#         return bundle

#     #def hydrate(self, bundle):
#         #if bundle.request.method == 'PATCH': # if patch, only allows start, stop, pause
#             #b = bundle.data.get('is_interrupted', None)
#             #c = bundle.data.get('is_finished', None)
#             #a = bundle.data.get('is_active', None)
#             #print a,b,c
#             #if c:
#                 #b=False # Not interrupted
#                 #a=False # Not acrtive
#             #else:
#                 #if b: #declared paused
#                     #a = b = False
#             #print a,b,c
#             #bundle.data = {'is_active' : a, 'is_interrupted': b, 'is_finished':c}
#         #return bundle

#     def obj_create(self, bundle, **kwargs):
#         if bundle.request.user.user_details.is_active: # If the user is active, does not allow
#             raise BadRequest("User already active, close exsiting session first")
#         bundle.request.user.user_details.is_active = True # no longer active
#         bundle.request.user.user_details.current_session = bundle.obj
#         # no longer active
#         bundle.request.user.user_details.save() # save and proceed
#         bundle.data['is_active'] = True # also sets session to active
#         bundle.data['is_finished'] = False # also sets session to active
#         bundle.data['is_interrupted'] = False # also sets session to active
#         return super(GPS_sessionResource, self).obj_create(bundle, user=bundle.request.user)
    
#     def obj_update(self, bundle, **kwargs): # we override the updates
#         if bundle.obj.is_finished:
#             raise BadRequest("Cannot modify a finished session")
#         if bundle.data['is_finished']: # if finished
#             bundle.data['is_active'] = bundle.data['is_interrupted'] = False
#             bundle.obj.is_active = bundle.obj.is_interrupted = False
#         else: #not finished command
#             if bundle.data['is_interrupted']: # if pause command or paused
#                 if not bundle.obj.is_active:
#                     if not bundle.data['is_active']:
#                         raise BadRequest("Cannot pause an inactive session")
#                     else:
#                         bundle.data['is_interrupted'] = bundle.obj.is_interrupted = False
#                 else:
#                     bundle.data['is_active'] = bundle.obj.is_active = False
#             else:
#                 if bundle.data['is_active']: # if session not active, activate
#                     if bundle.obj.is_active:
#                         raise BadRequest("Cannot start an active session")
#                     else: bundle.obj.is_active = True
#         bundle.request.user.user_details.is_active = bundle.data['is_active'] # copy active status
#         bundle.request.user.user_details.save() # save and proceed                
#         return super(GPS_sessionResource, self).obj_update(bundle, user=bundle.request.user)

#     def apply_authorization_limits(self, request, object_list):
#         return object_list.filter(user=request.user) # only over get method


        
# class Found_targetResource(ModelResource):
#     session = fields.ForeignKey(GPS_sessionResource, 'session') # related to registered user
#     user = fields.ForeignKey(UserResource, 'user') # related to registered user
#     class Meta:
#         queryset = gmodels.Found_target.objects.all() # all gps_updates
#         resource_name = 'found_target'
#         list_allowed_methods = ['get','post'] # can post, can get
#         detail_allowed_methods = ['get'] # can only get
#         authorization=Authorization()
#         authentication= BasicAuthentication()
#         #authentication= ApiKeyAuthentication()
#         filtering = {
#             'session': ALL_WITH_RELATIONS, # by session
#         }
#         ordering = ['classment','time_found']

#     def hydrate_user(self, bundle): # overrides user field in creation
#         bundle.data['user'] =  bundle.request.user
#         return bundle

#     def get_object_list(self, request):
#         """
#         Overrides get_object_list to allow filtering
#         """
#         return self._meta.queryset.filter(session = request.session)

#     def obj_create(self, bundle, **kwargs):
#         if not bundle.request.user.is_active:
#             raise BadRequest("User is not active, cannot upload")
#         us_d = gmodels.User_details.objects.get(user = bundle.request.user)
#         sess = us_d.current_session # not working
#         print us_d
#         if not sess:
#             raise BadRequest("There are no sessions to update to. Create one!")
#         if sess.is_finished:
#             raise BadRequest("Current Session is closed, no updates allowed")
#         if sess.is_interrupted:
#             raise BadRequest("Current Session is paused, no updates allowed")
#         if not sess.is_active:
#             raise BadRequest("Current Session is not active, no updates allowed")

#         return super(Found_targetResource, self).obj_create(bundle, session=sess)

#     def obj_get(self, bundle, **kwargs):
#         return super(Found_targetResource, self).obj_create(bundle, user=bundle.request.user)


#     def apply_authorization_limits(self, request, object_list):
#         return object_list.filter(user=request.user) # only over get method


# class SensorResource(ModelResource):
#     session = fields.ForeignKey(GPS_sessionResource, 'session') # related to registered user
#     class Meta:
#         queryset = gmodels.Sensor_update.objects.all() # all gps_updates
#         resource_name = 'sensor_update'
#         list_allowed_methods = ['post'] # can post, can get
#         detail_allowed_methods = [] # not exposing the data
#         authentication= BasicAuthentication()
#         #authentication= ApiKeyAuthentication()
#         authorization=Authorization()
#         #authentication= SillyAuthentication()

#     def hydrate_user(self, bundle): # overrides user field in creation
#         bundle.data['user'] =  bundle.request.user
#         return bundle
                
        
# class GPS_updateResource(ModelResource):
#     session = fields.ForeignKey(GPS_sessionResource, 'session') # related to registered user
#     class Meta:
#         queryset = gmodels.GPS_update.objects.all() # all gps_updates
#         resource_name = 'update'
#         list_allowed_methods = ['get','post'] # can post, can get
#         detail_allowed_methods = ['get'] # can only get
#         authentication= BasicAuthentication()
#         authorization=Authorization()
#         #authentication= SillyAuthentication()
#         filtering = {
#             'session': ALL_WITH_RELATIONS, # by session
#             #'user': ALL, # redundant
#         }
#         ordering = ['time']
        
#     def hydrate_user(self, bundle): # overrides user field in creation
#         bundle.data['user'] =  bundle.request.user
#         return bundle
        

####### Dehydrate cycle --> data from server to client

#    def dehydrate(self, bundle):
        # If they're requesting their own record, add in their email address.
#        if bundle.request.user.pk == bundle.obj.pk:
            # Note that there isn't an ``email`` field on the ``Resource``.
            # By this time, it doesn't matter, as the built data will no
            # longer be checked against the fields on the ``Resource``.
#            bundle.data['email'] = bundle.obj.email

#        return bundle
##### Log ####
# Implemented current session, user for creation. Implement if request.method == POST
# Check changes
# Implement return results only by user with get_authorization_limits!
