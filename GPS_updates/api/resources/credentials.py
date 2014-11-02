from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from tastypie.models import ApiKey

class CredentialsResource(ModelResource):
    class Meta:
        allowed_methods         = ['get', 'post']
        resource_name           = 'credentials'
        queryset                = ApiKey.objects.all()
        authorization           = Authorization()
        always_return_data      = True

    def obj_create(self, bundle, **kwargs):
        # get user params
        username = bundle.data.get('username', None)
        password = bundle.data.get('password', None)

        # authenticate user
        user = authenticate(username = username , password = password)

        # if user exists
        if user is not None:
            if user.api_key is not None:
                # get API key
                api_key = user.api_key
            else:
                # create API key
                api_key = ApiKey.objects.create(user = user)
            
        # if user doesn't exist
        # else:
        #     # # create user
        #     # new_user = User.objects.create_user(username, email, password)
        #     # new_user.save()

        #     new_user = User.objects.get(username__exact = username)

        #     # create user details
        #     details = User_details(user = new_user, atts_n = 7)
        #     details.save()

        #     # create API key
        #     api_key = ApiKey.objects.create(user = new_user)

            bundle.obj = user.api_key

        return bundle