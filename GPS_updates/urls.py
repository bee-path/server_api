from django.conf.urls.defaults import *
from GPS_updates import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.server_works, name='server_works'),
    url(r'html_app/$', views.html_app, name='index'),
    #url(r'^create_user$', views.create_user, name='create_user'),
    #url(r'^user_check$', views.user_check, name='user_check'),
    # ex: /polls/5/
    url(r'validate_email/$', views.validate_email, name='validate_email'),
    url(r'validate_username/$', views.validate_username, name='validate_username'),
    url(r'validate_user/$', views.validate_user, name='validate_user'),
    url(r'ranking/$', views.ranking, name='ranking'),
    #url(r'validate_username/$', views.validate_username, name='validate_username'),
    #url(r'stop_all/$', views.stop_all, name='stop_all'),
    # ex: /polls/5/results/
    #url(r'^(?P<GPS_updates_id>\d+)/results/$', views.results, name='results'),
)
