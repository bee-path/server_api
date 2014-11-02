# GPS_updates/authetification_custom.py
from tastypie.authentication import ApiKeyAuthentication, Authentication # username / api_key autentification

# Will implement this naive identification #

### Silly identification class ####
# Can be made custom if we wish to #
#from tastypie.authentication import Authentication

custom_number=123456
g_name='bee_path_generic'

# Only allows admin through
class SillyAuthentication(Authentication): # works!
    def is_authenticated(self, request, **kwargs):
        if g_name == request.user.username:
          return True
        
        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization

### Per user authorization (not working) ###
class PerUserAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        # if request.user.date_joined.year == 2010:
        #     return True
        # else:
        #     return False
        return False;

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        # if request and hasattr(request, 'user'):
        #     return object_list.filter(user=request.user)

        # return object_list.none()
        return object_list.none()
