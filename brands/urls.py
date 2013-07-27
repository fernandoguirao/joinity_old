from django.conf.urls import patterns, url
from brands import views
urlpatterns = patterns('',
    url(r'^(?P<nombre_brand>\d+)/$', views.ver, name='ver_brand'),
    url(r'^$', views.ver, name='ver'),

)
