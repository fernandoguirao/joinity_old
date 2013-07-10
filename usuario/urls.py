from django.conf.urls import patterns, url
from usuario import views
urlpatterns = patterns('',
    url(r'^(?P<user_id>\d+)/$', views.ver_perfil, name='ver_perfil'),
    url(r'^$', views.mi_perfil, name='mi_perfil'),
    url(r'^buscar/$', views.busqueda, name='busqueda_usuarios'),
    url(r'^registro/', views.registro, name="registro"),
    url(r'^editar/', views.editar_perfil, name="editar"),
)
