from django.conf.urls import patterns, url

from joinitys.eventos import views
urlpatterns = patterns('',
    url(r'^(?P<evento_id>\d+)/$', views.ver, name='ver_evento'),
    url(r'^crear/$', views.crear, name='crear_evento'),
    url(r'^crear/2/(?P<evento_id>\d+)$', views.crear_2, name='crear_evento_2'),
    url(r'^crear/3/(?P<evento_id>\d+)$', views.crear_3, name='crear_evento_3'),
    url(r'^invitar/(?P<evento_id>\d+)/(?P<usuario_id>\d+)/$', views.invitar, name='invitar_evento'),
    url(r'^invitar/(?P<evento_id>\d+)/all/$', views.invitar_todos, name='invitar_todos_evento'),
    
)
