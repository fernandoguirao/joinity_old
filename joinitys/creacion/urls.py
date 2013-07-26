from django.conf.urls import patterns, url

from joinitys.creacion import views
urlpatterns = patterns('',
    url(r'^$', views.nuevo_joinity, name='nuevo_joinity'),
    url(r'^family/$', views.nuevo_family, name='nuevo_family'),
    url(r'^family/2/(?P<joinity_id>\d+)/$', views.crear_2, name='nuevo_family_2'),
    url(r'^family/3/(?P<joinity_id>\d+)/$', views.crear_3, name='nuevo_family_3'),
    url(r'^aficiones/$', views.nuevo_aficiones, name='nuevo_aficiones'),
    url(r'^aficiones/2/(?P<joinity_id>\d+)/$', views.crear_2, name='nuevo_aficiones_2'),
    url(r'^aficiones/3/(?P<joinity_id>\d+)/$', views.crear_3, name='nuevo_aficiones_3'),
    url(r'^compras/$', views.nuevo_compras, name='nuevo_compras'),
    url(r'^compras/2/(?P<joinity_id>\d+)/$', views.crear_2, name='nuevo_compras_2'),
    url(r'^compras/3/(?P<joinity_id>\d+)/$', views.crear_3, name='nuevo_compras_3'),
    url(r'^(?P<joinity_id>\d+)/$', views.editar, name='editar_joinity'),
)
