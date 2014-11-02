import os

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     'beepath_server',      				# Or path to database file if using sqlite3.
        'USER':     'root',		               				# Not used with sqlite3.
        'PASSWORD': '',                  	 					# Not used with sqlite3.
        'HOST': 	'/Applications/xampp/xamppfiles/var/mysql/mysql.sock',								# Set to empty string for localhost. Not used with sqlite3.
        'PORT': 	'',                      					# Set to empty string for default. Not used with sqlite3.
    }
}

