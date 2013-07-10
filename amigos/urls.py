from django.conf.urls import patterns, url
from amigos import views
urlpatterns = patterns('',
    url(r'^$', views.lista_amigos, name='lista_amigos'),
    url(r'^invitar/$', views.invitar, name='invitar_amigos'),
    url(r'^aceptar/(?P<amigo_id>\d+)/$', views.aceptar, name='aceptar_amigo'),
    url(r'^invitar/(?P<amigo_id>\d+)/$', views.invitar_usuario, name='invitar_amigo'),

)
