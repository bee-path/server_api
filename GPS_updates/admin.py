from django.contrib import admin
from GPS_updates.models import Target,User_details, GPS_session

admin.site.register(User_details)
admin.site.register(Target)
admin.site.register(GPS_session)


#class PollAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
#https://docs.djangoproject.com/en/1.5/intro/tutorial02/
