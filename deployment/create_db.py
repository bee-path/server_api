#!/usr/bin/env python
# This script creates database #
import MySQLdb as mdb
# Create beepath_server database
usr='root'
passw='' # your pass
server='localhost'
db=mdb.connect(server,usr,passw)
db_name="beepath_server"
cur=db.cursor()
cur.execute("create database %s" % db_name)


########## Generate api keys for everyon ###########
#from django.contrib.auth.models import User
#from tastypie.models import ApiKey, create_api_key
#from django.db import models

#for user in User.objects.all():
    #models.signals.post_save.connect(create_api_key, sender=User)
