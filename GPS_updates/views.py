# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from GPS_updates.models import GPS_session, User_details
from django.contrib.auth.models import User
from forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http import Http404

from django.contrib.auth.models import User
from tastypie.exceptions import BadRequest
from tastypie import http

from GPS_updates import models
import os
#### Example
superpassword="neymar_crestas"

def index(request):
    return HttpResponse("Hello, world. You're at the experiment index.")

from django.shortcuts import render_to_response

def html_app(request):
    # View code here...
    return render(request, 'GPS_updates/index.html')
    #paths= os.getcwd()
    #return HttpResponse(open(paths+'/others/GPS_updates/index.html').read())
#### My views ####

from django.contrib.auth import authenticate, login

#def stop_all(request):
    #""" Stops all commands, needs to have a super_password parametter and user needs to be super_user"""
    #if request.method == 'POST':
        ## From here it is fucked
        #try: 
            #username = request.POST['username']
            #password = request.POST['password']
        #except KeyError:
            #pass                      
        #user = authenticate(username=username, password=password)
        #if user.is_superuser(): # end all sessions
            #try:
                #super_password = request.POST['super_password']
            #except KeyError:
                #return http.HttpMethodNotAllowed(json.dumps({'response':405,'message':'Must include key password'}), content_type="application/json")            
            #if super_password != superpassword:
                #return http.HttpMethodNotAllowed(json.dumps({'response':405,'message':'Wrong key password'}), content_type="application/json")                        
            #for e in GPS_session.objects.filter(is_active=True):
                #e._stop()
            #for e in User_details.objects.filter(is_active=True): # end all users
                #e.is_active = False
                #e.save()
            #return http.HttpResponse(json.dumps({'response':200,'message':'All has been stopped, users and sessions'}), content_type="application/json") 
        #else:
            #return http.HttpMethodNotAllowed(json.dumps({'response':405,'message':'Must be superuser'}), content_type="application/json")            
    #else:
        #return http.HttpMethodNotAllowed(json.dumps({'response':405,'message':'Only allows POSTS'}), content_type="application/json")
                
def server_works(request):
    return HttpResponse("<html><body>Hi app, the server is running<img src=""></body><html>")

import json

def validate_email(request):
    if request.method != 'GET':
        return http.HttpBadRequest(json.dumps({'response':405,'message':'Only allows GETS'}), content_type="application/json")
    try:
        data = request.GET['email']
    except:
        return http.HttpBadRequest(json.dumps({'response':400,'message':"Can't get email you are looking for!"}),content_type="application/json")
    a = User.objects.filter(email__exact=data)       
    if a:
        return http.HttpResponse(json.dumps({'response':200,'email_exists':1}),content_type="application/json")
    else: 
        return http.HttpResponse(json.dumps({'response':200,'email_exists':0}),content_type="application/json")

def validate_username(request):
    if request.method != 'GET':
        return http.HttpBadRequest(json.dumps({'response':405,'message':'Only allows GETS'}), content_type="application/json")
    try:
        data = request.GET['username']
    except:
        return http.HttpBadRequest(json.dumps({'response':400,'message':"Can't get username you are looking for!"}),content_type="application/json")
    a = User.objects.filter(username__exact=data)       
    if a:
        return http.HttpResponse(json.dumps({'response':200,'user_exists':1}),content_type="application/json")
    else: 
        return http.HttpResponse(json.dumps({'response':200,'user_exists':0}),content_type="application/json")


from django.contrib.auth import authenticate

def validate_user(request):
    if request.method != 'GET':
        return http.HttpBadRequest(json.dumps({'response':405,'message':'Only allows GETS'}), content_type="application/json")
    try:
        user = request.GET['username']
        #passw = request.POST['password']
        passw = user.split(',')[-1]
        user = user.split(',')[0]
    except:
        return http.HttpBadRequest(json.dumps({'response':400,'message':"Can't get username or pass you are looking for!"}),content_type="application/json")
    user = authenticate(username=user, password=passw)
    if user:
        if user.is_active:
            return http.HttpResponse(json.dumps({'response':200,'user_logged_in':1, 'user_active':1}),content_type="application/json")
        else:    
            return http.HttpResponse(json.dumps({'response':200,'user_logged_in':1, 'user_active':0}),content_type="application/json")
    else: 
        return http.HttpResponse(json.dumps({'response':200,'user_logged_in':0}),content_type="application/json")


###################


def ranking(request):
    if request.method != 'GET':
        return http.HttpBadRequest(json.dumps({'response':405,'message':'Only allows GETS'}), content_type="application/json")
    try:
        try:
            a = models.User_details.objects.filter(is_active=False).order_by('total_time')[:15] # get top 15 non active users
            b = [ {'total_time':e.total_time, 'total_length': e.total_length, 'username': e.user.username} for e in a ]
            l = len(b)
        except: # no matching criteria
            b = None
            l = 0
        return http.HttpResponse(json.dumps({'response':200,'total_count':l ,'objects':b}),content_type="application/json")
    except:
        return http.HttpResponse(json.dumps({'response':400,'message':'something went wrong'}),content_type="application/json")


from GPS_updates import get_results as gr
def all_actives(request):
    if request.method != 'GET':
        return http.HttpBadRequest(json.dumps({'response':405,'message':'Only allows GETS'}), content_type="application/json")
    a = models.GPS_session.objects.filter(is_active=True) # we get active sessions
    if a:
        b=[]
        for s in a:
            x=models.GPS_update.objects.filter(session = s).order_by('-timestamp')
            if x:
                b.append(gr.UTM_2_lonlat_single(x[0].lon, x[0].lat)) # last point
        #b =[models.GPS_update.objects.filter(session = s).order_by('-timestamp')[0] for s in a] # last point
        return http.HttpResponse(json.dumps({'response':200,'objects':b}),content_type="application/json")
    else: 
        return http.HttpResponse(json.dumps({'response':400,'message':"No active users"}),content_type="application/json")
   
