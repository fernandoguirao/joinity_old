from django.conf.urls import patterns, url, include

from joinitys import views
urlpatterns = patterns('',
    url(r'^(?P<evento_id>\d+)/$', views.ver_evento, name='ver_evento'),
)
