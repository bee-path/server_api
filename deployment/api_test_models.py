#!/usr/bin/env python
# This scripts plays around with models # just copy paste to django api

import GPS_updates.models as gg
from django.contrib.auth.models import User

import json
import datetime

z={'lat':23,'lon':43}
zz=json.dumps(z)
# We create two Targets
T1=gg.Target(lat=32,lon=4.5)
T2=gg.Target(lat=25,lon=55.3)
T1.save()
T2.save()


# Create generic user(s)

username='beepath_generic2'
passw='1234'
g_name='bee_path'

user = User.objects.create_user(username=username, email="beepath2@beepath2.ula",  password=passw)
user.is_staff=False
user.is_active=True
user.save()

username='beepath_generic'
user2 = User.objects.create_user(username=username, email="beepath@beepath.ula",  password=passw)
user2.is_staff=False
user2.is_active=True
user2.save()

# Create group
from django.contrib.auth.models import Group
group = Group(name=g_name)
group.save()
# Add to group
g = Group.objects.get(name=g_name) 
g.user_set.add(user)
g.user_set.add(user2)
g.save()



# We create user-details

U1=gg.User_details( update_rate=15, user=user, phone_os='android')
U2=gg.User_details( update_rate=15, user=user2, phone_os = 'iphone')
U1.save()
U2.save()

# We create sessions

S2=gg.GPS_session(user=user2)
S1=gg.GPS_session(user=user)
S2._start_session()
S1._start_session()
assert(S2._is_active())

S1._save_all()
S2._save_all()

# We create a position
P1=gg.GPS_update(lat= 33.2, lon = 32.3, session=S1, timestamp = 1, provider = 'net')
P1.save()
P1=gg.GPS_update(lat= 33.2, lon = 32.25, session=S1, alt=12, timestamp = 10, provider = 'GPS')
P1.save()
P1=gg.GPS_update(lat= 33.2, lon = 32.4, session=S1, alt = 23, timestamp = 20, pow_bat = 25, provider = 'GPS')
P1.save()
P1=gg.GPS_update(lat= 33.3, lon = 32.3, session=S2, timestamp = 13, provider = 'GPS')
P1.save()
P1=gg.GPS_update(lat= 33.3, lon = 32.3, session=S2, timestamp = 23, acc=2, provider = 'GPS')
P1.save()
P1=gg.GPS_update(lat= 33.3, lon = 32.4, session=S2, timestamp = 25, acc=32, provider = 'net')
P1.save()


SS1 = gg.Sensor_update(session = S1, v1= 32.3, timestamp = 5, sensortype = 3, maxrange = 32, mindelay = 3.4, res = 3, sensorname = 'accelerometer') 
SS2 = gg.Sensor_update(session = S2, v1= 32.3, timestamp = 5, sensortype = 3, maxrange = 32, mindelay = 3.4, res = 3, sensorname = 'compass') 
SS1.save()
SS2.save()

# We create a found Target from Target
F1=gg.Found_target( target=T1, session=S1)
F1.save()
F1._register()
F1.save()
F2=gg.Found_target( target=T2, session=S2)
F2.save()
F2._register()
F2.save()
F3=gg.Found_target( target=T2, session=S1)
F3._register()
F3.save()

#### Done ! ###
