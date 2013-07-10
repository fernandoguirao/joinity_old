import os, sys
sys.path.append('/var/www/vhosts/bueninvento.net/proyectos/django/prueba1')
os.environ['DJANGO_SETTINGS_MODULE'] = 'joinity.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
