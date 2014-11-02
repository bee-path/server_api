from django.db import models
from django.contrib.auth.models import User

#import GPS_updates.aux_module as am
import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError

import get_results as gr
import time

### Special funcs ###
def time_spent(t1,t2,abss=True):
    """ Computes timedelta difference from two datetime objects, if abss is true, returns absoulte value.
    Does t1-t2
    Returns seconds
    """
    if abss:
        return abs(datetime.timedelta(minutes=t1.minute-t2.minute,days=t1.day-t2.day,hours=t1.hour-t2.hour,seconds=t1.second-t2.second).seconds)
    else:
        return datetime.timedelta(minutes=t1.minute-t2.minute,days=t1.day-t2.day,hours=t1.hour-t2.hour,seconds=t1.second-t2.second).seconds
### Rewritte the __unicode__ methods of the classes for a better representation ###
# This cannot exist if no users exist

# This is for stupid trials
class Entry(models.Model):
    choice_text = models.CharField(max_length=200)
    def foo(self):
        return self.choice_text+u'kokokok'
###


class User_details(models.Model):
    """
        Custom class that represents the user details
        Check readme for information
    """
    user = models.OneToOneField(User,unique=True)
    current_session = models.ForeignKey("GPS_session", null=True, blank=True, default = None)
    phone_os= models.CharField(max_length=50)
    update_rate = models.PositiveIntegerField(default=15)
    sessions_n = models.PositiveIntegerField(default=0)
    updates_n = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    total_time = models.PositiveIntegerField(default=0)
    total_length = models.FloatField(default=0)
    future_emails = models.BooleanField(default=False)
    alone = models.BooleanField(default=True)
    gender = models.CharField(default='I', max_length=2)
    age = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return "User ID: %s" % str(self.id)
    #def _activate_user(self):
        #if not self.is_active:
            #self.is_active=True
            #return 1
        #else:
            #print "User is already active!"
            #return 0
   
    #def _deactivate_user(self):
        #if self.is_active:
            #self.is_active=False
            #return 1
        #else:
            #print "User is already not active!"
            #return 0
        
    def _is_active(self):
        return self._is_active
    # define total_time, total_length, number of sessions, found_targets
    #def _save_all(self):
        #try:
            #if self.current_session: self.current_session.save()
            #self.save()
            #return 1
        #except:
            #return 0


class GPS_session(models.Model):
    """
    User_id (foreign key)
    Status_active (bool)
    Session ID (int)
    Status interrupted (bool)
    targets_n (int)
    targets_list --> list
    total Time --> int
    total length --> int
    Start --> dict
        Position --> geoJSON
        Time in properties (Date-time)
    Stop --> dict
        Position --> geoJSON
        Time in properties (Date-time)
    n_up    dates (int)
        """
    user=models.ForeignKey(User)
    is_active =models.BooleanField(default=False) # defautls as falsE!
    is_interrupted = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    targets_found = models.PositiveIntegerField(default=0)
    targets_list = models.CharField(max_length=200) # char field
    total_time = models.PositiveIntegerField(default=0)
    total_length = models.FloatField(default=0)
    updates_n = models.PositiveIntegerField(default=0)
    date_start= models.DateTimeField(auto_now_add=True)
    date_stop= models.DateTimeField(auto_now=True)
    #position_start= models.ForeignKey('GPS_update',related_name='position_start')
    #position_stop= models.ForeignKey('GPS_update', related_name='position_stop')
    
    #def _start_session(self):
        #status = False
        #if not self._is_current(): # not current session
            #if not self.user.user_details.current_session: #non existing session
                #status = True
            #else:
                #if self.user.user_details.current_session.is_finished: # existing session, but finished!
                    #status = True
        #else: # current session
            #if not self.user.is_active and not self.is_active and not self.is_finished: # user not active, session not active, session not ended 
                #status = True
        #if status:
            #self.is_active = True # activate
            #self.user.user_details.is_active = True # user
            #self.user.user_details.current_session = self #enforce current session
            #return 1
        #return 0
            
    #def _end_session(self):
        #status=False
        #if self.user.user_details.is_active and self.is_active: #if sesison and user active
            #status=True
        #else:
            #if self.is_interrupted: #not active but paused
                #status=True
        #if status:    
            #self.user.user_details.is_active = False
            #self.is_active = False
            #self.is_interrupted = False
            #self.is_finished = True
            #return 1            
        #return 0
    
    #def _pause_session(self):
        #status = True
        #if self.user.user_details.is_active and self.is_active and self._is_current(): # user active, session active, current session
            #self.is_interrupted = True
            #self.user.user_details.is_active = False
            #self.is_active = False
            #return 1
        #return 0

    def _is_active(self):
        return self.is_active
    
    def _is_current(self):
        ss = self.user.user_details.current_session
        if ss == self:
            return True
        else:
            return False
    
    def _add_target(self,target):
        a=str(self.targets_list)
        if str(target.id) not in a.split(','):
            try:
                self.targets_list=unicode(a+str(target.id)+',')
                self.targets_found+=1
                return 1
            except:
                return 0
        else:
            return 0
            
    #def _save_all(self):
        #try:
            #self.user.user_details.save()
        #except: pass
        #self.save()
        #return 1
    
    def _compute_stats(self):
        """ Computes stats of the session:
            Total time
            Total length
            N_updates
        """
        try:
            ups = self._get_updates()
            # apply time_conversion
            if ups:
                adds = abs(ups[0].timestamp - time.mktime(self.date_stop.timetuple()))  # sum time since last patch (accounts for pause sessions)
                add_length = gr.calc_distance([(p.lat,p.lon,p.time) for p in ups])
                self.total_length += add_length 
                self.user.user_details.total_length += add_length 
                self.total_time += adds
                self.updates_n += int(len(ups))
                self.user.user_details.updates_n += int(len(ups))
                self.user.user_details.total_time += adds 
                
            return 1
        except:
            return 0
            
    #def __unicode__(self):
    #    print "GPS session %s for user %s" % (int(self.id),int(self.user.id)) 
    # define total_time, total_length, found_targets
    def _get_updates(self):
        return GPS_update.objects.filter(session = self, time_recorded__gte = self.date_stop ).order_by('-timestamp') # get all ups
    def _stop(self):
        if self.is_active:
            self.is_active= False            
            self.is_interrupted= True            
            self.is_finished= True            
            self._compute_stats()
            self.save()
            
class Target(models.Model):
    """ Target
            target_id (int)
            Position --> geoJSON
    """
    code = models.CharField(max_length=20)
    lat = models.FloatField()
    lon = models.FloatField()
    alt = models.FloatField(default=-1)
    
    def __unicode__(self):
        return "Target %s" % self.id


class Found_target(models.Model):
    """ Target found by user 
    Since cannot override __init__ methods we need to first declare it, then register.
    """
 
    time_found = models.DateTimeField(auto_now_add=True)  
    timestamp = models.BigIntegerField()  
    classment = models.PositiveIntegerField(default=0) # redefine init
    target = models.ForeignKey('Target')
    session =models.ForeignKey("GPS_session")
    
    @classmethod
    def create(cls, target, session, **kwargs):
        dummy = cls(target=target, session=session, **kwargs)
        a = dummy._register()
        if a:
            return dummy
        else:
            raise ValidationError("Target already registered in this session")

    def __unicode__(self):
        return "Target found %r" % self.target.id
        
    def _is_repeated(self):
        return str(self.target.id) in self.session.targets_list.split(',')

    def _time_spent(self):
        initial_time = self.session.date_start
        return time_spent(self.time_found , initial_time)

    def _register(self):
        if not self._is_repeated():
            self.session._add_target(self.target)
            self.classment = self.session.targets_found
            return 1
        else:
            return 0



class GPS_update(models.Model):
    """See readme    """
    lat = models.FloatField()
    lon = models.FloatField()
    alt = models.FloatField(default=-1)
    time_recorded = models.DateTimeField(auto_now_add=True)
    timestamp = models.BigIntegerField()
    session = models.ForeignKey("GPS_session")
    acc = models.FloatField(default=-1)
    provider = models.CharField(max_length=50)
    pow_bat = models.IntegerField(default=-1)
    
    def __unicode__(self):
        return "GPS update in %r %r " % (self.lat,self.lon)


class Sensor_update(models.Model):
    """ Sensor update """
    session = models.ForeignKey("GPS_session")
    v1 = models.FloatField(default=0.)
    v2 = models.FloatField(default=0.)
    v3 = models.FloatField(default=0.)
    v4 = models.FloatField(default=0.)
    acc = models.FloatField(default=-1.)
    time_recorded = models.DateTimeField(auto_now_add=True)
    timestamp = models.BigIntegerField()
    sensortype = models.IntegerField()
    sensorname = models.CharField(max_length = 50)
    maxrange = models.FloatField()
    mindelay = models.FloatField()
    res = models.FloatField(default = -1)

    def __unicode__(self):
        return "Sensor update for session %s " % (self.session.user.id)


class ICUB_model(models.Model):
    """ Icub info """
    carrer = models.CharField(max_length =150)
    num = models.CharField(max_length = 20)
    ciutat = models.CharField( max_length = 20)
    cp = models.CharField(max_length = 10)
    email = models.EmailField(max_length=254)
    
