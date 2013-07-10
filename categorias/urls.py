from django.conf.urls import patterns, url
from categorias import views
urlpatterns = patterns('',
    # url(r'^$', views.lista_amigos, name='lista_amigos'),
    # url(r'^invitar/$', views.invitar, name='invitar_amigos'),
    url(r'^nuevo_interes/$', views.nuevo_interes, name='crea_interese'),
    url(r'^nueva_compra/$', views.nueva_compra, name='crea_interes_compra'),

)
