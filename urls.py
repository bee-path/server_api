from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from GPS_updates.api.resources import resources, user, user_details, credentials, gps_update, gps_session, target, found_target, login, sensor

v1_api = Api(api_name='v1')
#v1_api.register(resources.EntryResource())
v1_api.register(user.UserResource())
v1_api.register(user_details.User_detailsResource())
v1_api.register(gps_update.GPS_updateResource())
v1_api.register(gps_session.GPS_sessionResource())
v1_api.register(target.TargetResource())
v1_api.register(found_target.Found_targetResource())
v1_api.register(login.LoginResource())
v1_api.register(sensor.SensorResource())
v1_api.register(sensor.ICUB_modelResource())
#v1_api.register(credentials.CredentialsResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'beepath.views.home', name='home'),
    # url(r'^beepath/', include('beepath.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^GPS_updates/', include('GPS_updates.urls')), # project registered
    url(r'^api/', include(v1_api.urls)), # api registered
)
