1. RUN SERVER
=======

Para incializar el servidor: 
python manage.py runserver
localhost:8000

2. SOBRE EL DATE-PICKER
====================
La estructura a copiar/pegar es la siguiente:

<div class="control-group">
  <div class="input-prepend input-datepicker">
    <button type="button" class="btn"><span class="fui-calendar"></span></button>
    <input type="text" class="span2" value="14 March, 2013" id="datepicker-01">
  </div>
</div>

El enlace a la documentación del date-pick de jquery-ui es http://api.jqueryui.com/datepicker/

3. INSTRUCCIONES PARA QUE FUNCIONE AJAX
=======================================

a. Instalamos el paquete de python dajaxice. Podemos descargarlo de: https://github.com/jorgebastida/django-dajaxice y los instalamos como cualquier paquete normal de python.

b. En nuestro proyecto de joinity sustituimos el archivo joinity/settings.py por este (cambiando las rutas de mi ordenador a las tuyas): https://www.dropbox.com/s/xqrmeovbbgnl30h/settings.py

c. En nuestro proyecto de joinity sustituimos el archivo jonity/urls.py por este: https://www.dropbox.com/s/xqrmeovbbgnl30h/settings.py

d. En cualquier app instalada de joinity creamos un nuevo archivo .py con los datos que tengamos que pasar por ajax. Un ejemplo (lo que se pasa es lo que está en el interior de la string. Yo he usado texto plano pero obviamente podemos pasar cualquier tipo de datos):

from django.utils import simplejson

def sayhello(request):
    return simplejson.dumps({'message':'Este mensaje esta en el servidor y funciona'})
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def sayhello(request):
    return simplejson.dumps({'message':'Este mensaje esta en el servidor y funciona'})

e. Fase final: los templates.
  
  e.1. Editamos el head del html y añadimos:

    -Antes de abrir la etiqueta html:
      {% load dajaxice_templatetags %}
      
    -Antes de cerrar la etiqueta head:
      {% dajaxice_js_import %}
      
  e.2. Donde queramos cargar el contenido ajax, sólo hay que llamarlo a través de una función de javascript, de este modo (de hecho, hazlo así cargándolo en un alert y ya me encargo yo de cargarlo en el html como tendría que ser):
  
    <button onclick="Dajaxice.example.sayhello(my_js_callback);" class="btn btn-big" style="margin:200px;">Quiero ver Ajax en acción</button>

  e.3. En el archivo de funciones de javascript (esto ya lo hago yo) añadimos esto:
    function my_js_callback(data){
      alert(data.message);
    }



3. ARCHIVO SETTINGS DE FERNANDO
============================

# Django settings for joinity project.
# -*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOCALHOST = True
ADMINS = (
     ('Girien', 'antoniespinosa@me.com'),
)

MANAGERS = ADMINS
if LOCALHOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'joinity',  # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'joinity',
            'PASSWORD': 'C4s10p34',
            'HOST': 'bueninvento.net',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '3306',  # Set to empty string for default.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'joinity',  # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'joinity',
            'PASSWORD': 'C4s10p34',
            'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '3306',  # Set to empty string for default.
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ES'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
if LOCALHOST:
    MEDIA_ROOT = '/Volumes/Macintosh HD/Users/fguirao/Dropbox/Bueninvento/Proyectos/Joinity/Taller/App/media/'
else:
    MEDIA_ROOT = '/var/www/vhosts/bueninvento.net/proyectos/django/prueba1/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
if LOCALHOST:
    STATIC_ROOT = '/Volumes/Macintosh HD/Users/fguirao/Dropbox/Bueninvento/Proyectos/Joinity/Taller/App/'
else:
    STATIC_ROOT = '/Volumes/Macintosh HD/Users/fguirao/Dropbox/Bueninvento/Proyectos/Joinity/Taller/App/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
if LOCALHOST:
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        '/Volumes/Macintosh HD/Users/fguirao/Dropbox/Bueninvento/Proyectos/Joinity/Taller/App/static/',
    )
else:
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        '/var/www/vhosts/bueninvento.net/proyectos/django/prueba1/static/',
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0_w-suhuj+janxkz95hjmiigvw9f&h$22c+*!3g-fofik#7wg1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
AUTH_PROFILE_MODULE = 'login.Usuarios'
DECIMAL_SEPARATOR = ','

ROOT_URLCONF = 'joinity.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'joinity.wsgi.application'

if LOCALHOST:
    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        '/Volumes/Macintosh HD/Users/fguirao/Dropbox/Bueninvento/Proyectos/Joinity/Taller/App/templates',
    )
else:
    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        '/var/www/vhosts/bueninvento.net/proyectos/django/prueba1/templates/',
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paypal.standard.ipn',
    'pagos',
    'usuario',
    'mensajes',
    'amigos',
    'django.contrib.admin',
    'categorias',
    'mathfilters',
    'joinitys',
    'reservas',
)


PAYPAL_RECEIVER_EMAIL = "girienmorfindel@gmail.com"

if LOCALHOST:
    SITE_NAME = 'http://81.37.96.173/'
else:
    SITE_NAME = 'http://prueba1.bueninvento.net/'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}