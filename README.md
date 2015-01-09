Beepath API module
========================================================================

Copyright 2013 Oleguer Sagarra. All rights reserved. Code under License GPLv3.
______________________________________________________________________________________


## Contents of the package

The present package contains the minimal code to develop an API with REST capabilities residing on a DJANGO server. The API is made based on the [tastypie project](http://tastypieapi.org/).
Such server supports the Bee-path application used in the experiments on Festa de la Ciència 2013. For more details see the [project webpage](http://bee-path.net/).

Check the DOCS for dependencies and a quick-cheat-sheet on how to query the API.

## Installation 


## Installation

To install the server, proceed as follows.

1. Install all the dependencies:
	pip, python, django, tastypie using *easy_install* or *pip*.
	(optional if you don't have oracle, mysql or postgres, install mysql (I recommend using [XAMPP](http://sourceforge.net/projects/xampp/))
	install python bindings for the chosen database (recommended py-mysql).
2. Create a directory where to store the django project, untar the provided files.
3. Change the name of the file Heligoland_local.py to  xxx.py and change xxx by the name of your computer (the name appearing on the terminal before the @)
4. Edit xxx.py with proper settings: Choose your database and set your path to host. Also edit the templates location, static files and so on (see django docs)
5. Run :

```
    $ python manage.py syncdb 
```

6. You are ready to fire up the server (runs by default on the port localhost:8000): 
```
    $ python manage.py runserver
```

## Usage

The present app **GPS_updates** implements a [Restful API](https://en.wikipedia.org/wiki/Representational_state_transfer) based on [tastypie](http://tastypieapi.org/).
As such, the protocol needs to be used in a *passive* way, that means that the API is based on resources rather that on actions, and hence onñy the basic HTTP operations are allowed.

To see more on HTTP actions check [wikipedia](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods).
The only allowed type of data is [JSON format](http://www.json.org/), needs to be indicated in HTTP headers, which include the type (JSON) and method used (GET, POST...).

To interact with the api you can use whatever you like, for instance cURL. See the [tastypie docs](http://django-tastypie.readthedocs.org/en/latest/interacting.html) or [Python Requests](http://docs.python-requests.org/en/latest/) for instance.

## Database structure description

The basic models used can be found in GPS_updates/models.py but can be summarized as follows:

The required fields upon POST (creation) are marked as (r).

### Outer level: User_details  (Django Model) and User (Django.db internal model). Accesible through GET command (only user list).
##### User is a own django instance and contains (other fields described in django docs):
	1. Api_key (unique): Unique key for interacting with user, created on creation of user. (not implemented)
	2. (r)Username -> string. Unique in database
	3. (r)Pass
	4. (r)Email : Copies from username. Needs to be a valid instance and be unique in database.

##### User_details: Accessible by all identified users (without sensitive fields). Is created at the same time of user creation, but can be modified using PATCH if user changes options. GET requests are always allowed, PATCH requests only allowed on own user (user needs to be identified). POST updates not allowed.
	1. (r)User --> Foreign keys that "points" to User
	2. phone_os: char (android, iphone, blackberry...)
	3. update_rate: int. Indetifies time between batch GPS updates.
	4. sessions_n : Int. Number of sessions
	5. is_active : Boolean. Indicates user has an active session
	6. total_time: Int. Total time spent by user (do not computes current session)
	7. total_length: Field. Total distance by user (metters)
    Filtering allowed:            
	    'user': ALL_WITH_RELATIONS,
            'is_active': ALL,
            'total_time': ALL, # for rankings
            'total_length': ALL, # for rankings
            'alone' : ALL,
            'gender' : ALL,
            'age': ALL

##### Target: Defines a target (what users are supposed to find). Accessible by all identified users. Only allows GET
	1. (r)Lat: Float
	2. (r)Lon: Float
	3. ID: Primary key (automatically generated)
	4. alt: Float (default -1 if not info)

### Mid level (related with users):
#### GPS_session: Indicates a GPS session by the user. Only accessible by individual users fully identified. To be created, user needs to be inactive. Supports GET/PATCH/POST
	1. (r)User : Same as FK of user_details.
	2. is_active: Boolean, determines if session is active.
	3. is_interrupted: Boolean, determines if session has been interrupted --> 
	is_finished: Boolean, determines if session has been finished -> If session is finished, no more allowed GPS posts on that session.
	4. targets_found: Integer. Number of unique targets found in this session
	5. targets_list: Character. Ordered list of found target in the form: target_id1,target_id2,target_id3.... Gets automatically updated if a new target is found
	6. total_time: Integer.Session level total time spent. Computed when session is finished.
	7. total_length: Float. Idem as time.
	8. updates_n: Total number of updates for this sessions. Computed when session is finished.
	9. date_start: Datetime django field. Time of session start, automatically generated upon each "POST".
	10. date_stop: Time of session stop. Automatically generated upon each "PUT/PATCH".
### Inner level (related with user-sessions): Only allow POST and GET methods. All POSTS are blocked if the user and the session are not active, and the session does not need to be specified, as long as there is at least one active session.
#### Found_target: Indicates target found by the user. It's position IS NOT validated by the api. Only accepts "POSTS" if user_is_active and session_is_active. 
	1. time_found: Datetime django field of registration time of target in the server. Automatically generated.
	2. classment: Integer. Position in which target has been found. Automatically generated
	3. (r)target: Foreign key pointing to Target collection.
	4. (r)session: Foreign key pointing to Session collection.
	
#### GPS_update: A single GPS update. Normally should be added in batch inserts every "update_rate" seconds defined by user. Accepts "GET" and "POST".
	1. (r)lat: Float
	2. (r)lon: Float
	3. time_recorded: Automatically generated upon each POST.
	4. (r)timestamp: integer UNIX time.
	5. (r)session id
	6. alt: float
	7. (r)acc: float
	8. (r)provider: char (indicates network or GPS provider)
	9. pow_bat: integer (battery level percentage)

#### Sensor_update: A single sensor update. Should also be added in batch inserts. Accepts GET and POST. --> only if phone is android
  (In principle we shall only keep TYPE_LINEAR_ACCELERATION	TYPE_ORIENTATION) // Check android DOCS http://developer.android.com/reference/android/hardware/Sensor.html
	1. (r)session id
	2. v1,v2,v3,v4 : 4 float fields from sensor
	3. acc: float
	4. (r)timestamp: integer UNIX time
	5. (r)sensorname: char
	6. (r)sensortype: integer
	7. (r)maxrange: float
	8. (r)mindelay: float
	9. (r)res: float

## Authentification
The authentication is through a unique apikey/user pair. The apikey and user need to be included in the HTTP headers. Not implemebnted.
For the moment authentication is made through Basic Auth (see wikipedia for more info). Only needs user and pass in HTTP header.

```
POST /credentials
> Content-Type: application/json
{
	"username": <username>, 
	"password": <password> 
}
< 201
< Content-Type: application/json
{
    "created": "2013-06-01T18:04:00.650984",
    "id": 33,
    "key": "be6ed78160592cf4b1a37992b292c65d04c53e48",
    "password": "josep",
    "resource_uri": "/api/v1/credentials/33/",
    "username": "josep"
}
```


## Actions and resources

Although the API does not have defined actions "per se", this section indicate how to perform the "typical" operations. The resources are described in /GPS_updates/api/resources.py
See for more detais: [Tastypie docs - Interacting](http://django-tastypie.readthedocs.org/en/latest/interacting.html).

### User_login resource: (base URL: http://server:port/api/v1/user_login/). Allows POST
  1. User creation :
	Issue a POST command to the api with fields "username" and "password" and "email".
		If the username or email exists, raises Integrity Error
		Else: Creates user and sends API key to client. Also CREATES User_details
		No authentication is applied.
  2. Retrieval of API key of existing user: --> Not implemented
	Issue a GET command to the api with "username", "password" in header.
		In this case, the authentication protocol is BasiAtuh. If the identification succeeds, sends API key to client.
		Else raises 401 error


### User_details resource:  (base URL: http://server:port/api/v1/user_details/). Allows PATCH/GET
  1. Retrieval of user information / rankings:
	Issue a GET command to the api with fields "username", "pass" in header.
	Allows filtering over user, is_active, total_time, total_length.
  2. Update of user_options:
	Issue a PATCH command to the api with apropiate user fields and update User_details fields such as update_rate or age or gender. Warning! Patch is only defined on concrete objects, so to patch something the address would be: http://server:port/api/v1/user_details/id/ where "id" is the user_detail number id (which you can get using a GET command, and which you should store).

### GPS_session resource: (base URL: http://server:port/api/v1/session/): Allows GET/POST/PATCH
  1. Session creation: Issue a POST command to the api with apropiate user/key in header. Automatically sets user_Details.is_active to false.
  	IMPORTANT: IT returns a JSON pointing to the address of the resource in the field "resource_uri", alternatively, also gives the unique session identifier in field "id".
  2. Session pause or session stop: Issue a PATCH command with apropiate user fields and "GPS_session.is_interrupted = True" (pause) or "_is_finished=True" (stop) or "is_active=True" (restart). If "GPS_session.is_finished=True" computes statistics and blocks further PATCH commands.
PATCHES are not allowed if user is not active or ask for incoherent stuff (pausing already paused sessions for instance).



### Target resource: (base URL: http://server:port/api/v1/target/): Allows GET
  1. Get targets: Just a GET command with apropiate authentification.


Note: To send bulk updates, see [here](http://django-tastypie.readthedocs.org/en/latest/resources.html#patch-list).


### GPS_update resource: (base URL: http://server:port/api/v1/update/): Allows POST and GET
  1. Get all user updates: GET command with apropiate header + appropiate filtering. Permits session filtering
  2. Post new update: POST command with apropiate header. Required field: lat, lon, timestamp. Needs a unique sessoin active and user to be active.
  3. Post new updates in batch insert: PATCH update (see tastypie docs). Not implemented.

### Found_target resource: (base URL: http://server:port/api/v1/found_target/)
  1. Get targets: Just a GET command with apropriate authentication. Allows filtering over session with all relations.
  2. Register new target: Just a POST command with apropiate authentication. Checks internally if target has already been found in this session. Required field: target_id.


### Sensor_update: (Base URL: http://server:port/api/v1/sensor_update/): Allows only  POST
  1. Post new sensor update: Just a POST command with apropriate authentication. (Cannot be accessed from the api via GET commands).


### Other actions (not from the api)

### Validate_email: returns a json file with a result 0 or 1 in "email_exists". Issue a GET command to http://whatvereserver/GPS_updats/validate_email/?email=email_to_check
### Validate_user: returns a json file with a result 0 or 1 in "email_exists". Issue a GET command to http://whatvereserver/GPS_updats/validate_username/?username=username_to_check


## Error codes:
	Returns the usual HTTP errors 400, 500, 200....	


## License

Copyright 2013 Oleguer Sagarra (osagarra@ub.edu)
Code under License GPLv3.
All rights reserved. 


## Disclaimer

The software is provided as it is, with absolutely NO WARRANTY. If you detect any bugs, please let us know.

