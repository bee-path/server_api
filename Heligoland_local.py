import os

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     'beepath_development',      				# Or path to database file if using sqlite3.
        'USER':     'apuratep',		               				# Not used with sqlite3.
        'PASSWORD': '',                  	 					# Not used with sqlite3.
        'HOST': 	'localhost',								# Set to empty string for localhost. Not used with sqlite3.
        'PORT': 	'',                      					# Set to empty string for default. Not used with sqlite3.
    }
}

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))



MEDIA_ROOT = PROJECT_PATH + '/media/'

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/'
)

STATIC_ROOT = PROJECT_PATH + '/static/'
