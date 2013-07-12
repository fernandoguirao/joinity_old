from django.conf.urls import patterns, url

from joinitys import views
urlpatterns = patterns('',
    url(r'^nuevo_joinity/$', views.nuevo_joinity, name='nuevo_joinity'),
    url(r'^(?P<joinity_id>\d+)/reserva/$', views.crear_reserva, name='crear_reserva'),
    url(r'^(?P<joinity_id>\d+)/reserva/restaurante/$', views.buscar_restaurante, name='buscar_restaurante'),
    url(r'^(?P<joinity_id>\d+)/reserva/hotel/$', views.buscar_hotel, name='buscar_hotel'),
    url(r'^(?P<joinity_id>\d+)/reserva/restaurante/crear/(?P<empresa_id>\d+)/$', views.crear_reserva_restaurante, name='crear_reserva_restaurante'),
    url(r'^(?P<joinity_id>\d+)/reserva/hotel/crear/(?P<empresa_id>\d+)/$', views.crear_reserva_hotel, name='crear_reserva_hoteles'),
    url(r'^(?P<joinity_id>\d+)/reserva/restaurante/(?P<reserva_id>\d+)/$', views.ver_reserva, name='ver_reserva'),
    url(r'^(?P<joinity_id>\d+)/reserva/hotel/(?P<reserva_id>\d+)/$', views.ver_reserva, name='ver_reserva_hotel'),
    url(r'^nuevo_joinity/family/$', views.nuevo_family, name='nuevo_family'),
    url(r'^nuevo_joinity/family/2/(?P<joinity_id>\d+)/$', views.crear_2, name='nuevo_family_2'),
    url(r'^nuevo_joinity/family/3/(?P<joinity_id>\d+)/$', views.crear_3, name='nuevo_family_3'),
    url(r'^nuevo_joinity/aficiones/$', views.nuevo_aficiones, name='nuevo_aficiones'),
    url(r'^nuevo_joinity/aficiones/2/(?P<joinity_id>\d+)/$', views.crear_2, name='nuevo_aficiones_2'),
    url(r'^nuevo_joinity/aficiones/3/(?P<joinity_id>\d+)/$', views.crear_3, name='nuevo_aficiones_3'),
    url(r'^nuevo_joinity/compras/$', views.nuevo_compras, name='nuevo_compras'),
    url(r'^nuevo_joinity/compras/2/(?P<joinity_id>\d+)/$', views.crear_2, name='nuevo_compras_2'),
    url(r'^nuevo_joinity/compras/3/(?P<joinity_id>\d+)/$', views.crear_3, name='nuevo_compras_3'),
    url(r'^ver/(?P<joinity_id>\d+)/$', views.ver, name='ver_joinity'),
    url(r'^(?P<joinity_id>\d+)/$', views.ver, name='ver_joinity2'),
    url(r'^aceptar/(?P<joinity_id>\d+)/$', views.aceptar, name='aceptar_joinity'),
    url(r'^unirse/(?P<joinity_id>\d+)/$', views.unirse, name='unirse_joinity'),
    url(r'^(?P<joinity_id>\d+)/evento/(?P<evento_id>\d+)/$', views.ver_evento, name='ver_evento'),
    url(r'^(?P<joinity_id>\d+)/tarea/(?P<tarea_id>\d+)/$', views.ver_tarea, name='ver_tarea'),
    url(r'^(?P<joinity_id>\d+)/evento/crear/$', views.crear_evento, name='crear_evento'),
    url(r'^(?P<joinity_id>\d+)/evento/crear/2/(?P<evento_id>\d+)$', views.crear_evento_2, name='crear_evento_2'),
    url(r'^(?P<joinity_id>\d+)/evento/invitar/(?P<evento_id>\d+)/(?P<usuario_id>\d+)/$', views.invitar_evento, name='invitar_evento'),
    url(r'^(?P<joinity_id>\d+)/evento/invitar/(?P<evento_id>\d+)/all/$', views.invitar_todos_evento, name='invitar_todos_evento'),
    url(r'^(?P<joinity_id>\d+)/evento/crear/3/(?P<evento_id>\d+)$', views.crear_evento_3, name='crear_evento_3'),
    url(r'^(?P<joinity_id>\d+)/tarea/crear/$', views.crear_tarea, name='crear_tarea'),
    url(r'^(?P<joinity_id>\d+)/tarea/crear/sub/(?P<tarea_id>\d+)$', views.crear_subtarea, name='crear_subtarea'),
    url(r'^(?P<joinity_id>\d+)/tarea/crear/2/(?P<tarea_id>\d+)$', views.crear_tarea_2, name='crear_tarea_2'),
    url(r'^(?P<joinity_id>\d+)/tarea/invitar/(?P<tarea_id>\d+)/(?P<usuario_id>\d+)/$', views.invitar_tarea, name='invitar_tarea'),
    url(r'^(?P<joinity_id>\d+)/tarea/invitar/(?P<tarea_id>\d+)/all/$', views.invitar_todos_tarea, name='invitar_todos_tarea'),
    url(r'^(?P<joinity_id>\d+)/tarea/crear/3/(?P<tarea_id>\d+)$', views.crear_tarea_3, name='crear_tarea_3'),
    url(r'^invitar/(?P<joinity_id>\d+)/(?P<usuario_id>\d+)/$', views.invitar_usuario, name='invitar_usuario'),
    url(r'^nombrar_admin/(?P<usuario_joinity_id>\d+)/$', views.nombrar_admin, name='nombrar_admin'),
    url(r'^aceptar_membresia/(?P<usuario_joinity_id>\d+)/$', views.aceptar_membresia, name='aceptar_membresia'),
    url(r'^(?P<joinity_id>\d+)/evento/(?P<evento_id>\d+)/unirse/$', views.unirse_evento, name='unirse_evento'),
    url(r'^filtrar/$', views.filtro, name="filtrar"),
)
