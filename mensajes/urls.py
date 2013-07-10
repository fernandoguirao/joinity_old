from django.conf.urls import patterns, url
from mensajes import views
urlpatterns = patterns('',
    # url(r'^/escribir/(?P<user_id>\d+)/$', views.ver_perfil, name='ver_perfil'),
    url(r'^$', views.escribir, name='escribir_mensaje'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^inbox/(?P<user_id>\d+)/$', views.chat, name='chat'),
    url(r'^(?P<mensaje_id>\d+)/$', views.ver, name='ver_mensaje'),
)
