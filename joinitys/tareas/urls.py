from django.conf.urls import patterns, url
from views import ver, crear, crear_subtarea, crear_2, crear_3, invitar, invitar_todos
urlpatterns = patterns('',
    url(r'^(?P<tarea_id>\d+)/$', ver, name='ver_tarea'),
    url(r'^crear/$', crear, name='crear_tarea'),
    url(r'^crear/sub/(?P<tarea_id>\d+)$', crear_subtarea, name='crear_subtarea'),
    url(r'^crear/2/(?P<tarea_id>\d+)$', crear_2, name='crear_tarea_2'),
    url(r'^crear/3/(?P<tarea_id>\d+)$', crear_3, name='crear_tarea_3'),
    url(r'^invitar/(?P<tarea_id>\d+)/(?P<usuario_id>\d+)/$', invitar, name='invitar_tarea'),
    url(r'^invitar/(?P<tarea_id>\d+)/all/$', invitar_todos, name='invitar_todos_tarea'),
)