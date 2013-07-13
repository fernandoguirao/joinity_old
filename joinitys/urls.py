from django.conf.urls import patterns, url, include

from joinitys import views
urlpatterns = patterns('',
    url(r'^(?P<joinity_id>\d+)/reserva/$', views.crear_reserva, name='crear_reserva'),
    url(r'^(?P<joinity_id>\d+)/reserva/restaurante/$', views.buscar_restaurante, name='buscar_restaurante'),
    url(r'^(?P<joinity_id>\d+)/reserva/hotel/$', views.buscar_hotel, name='buscar_hotel'),
    url(r'^(?P<joinity_id>\d+)/reserva/restaurante/crear/(?P<empresa_id>\d+)/$', views.crear_reserva_restaurante, name='crear_reserva_restaurante'),
    url(r'^(?P<joinity_id>\d+)/reserva/hotel/crear/(?P<empresa_id>\d+)/$', views.crear_reserva_hotel, name='crear_reserva_hoteles'),
    url(r'^(?P<joinity_id>\d+)/reserva/restaurante/(?P<reserva_id>\d+)/$', views.ver_reserva, name='ver_reserva'),
    url(r'^(?P<joinity_id>\d+)/reserva/hotel/(?P<reserva_id>\d+)/$', views.ver_reserva, name='ver_reserva_hotel'),
    url(r'^nuevo_joinity/', include('joinitys.creacion.urls', namespace="creacion")),
    url(r'^ver/(?P<joinity_id>\d+)/$', views.ver, name='ver_joinity'),
    url(r'^(?P<joinity_id>\d+)/$', views.ver, name='ver_joinity2'),
    url(r'^aceptar/(?P<joinity_id>\d+)/$', views.aceptar, name='aceptar_joinity'),
    url(r'^unirse/(?P<joinity_id>\d+)/$', views.unirse, name='unirse_joinity'),
    url(r'^(?P<joinity_id>\d+)/evento/', include('joinitys.eventos.urls', namespace="eventos")),
    url(r'^(?P<joinity_id>\d+)/tarea/', include('joinitys.tareas.urls', namespace="tareas")),
    url(r'^invitar/(?P<joinity_id>\d+)/(?P<usuario_id>\d+)/$', views.invitar_usuario, name='invitar_usuario'),
    url(r'^nombrar_admin/(?P<usuario_joinity_id>\d+)/$', views.nombrar_admin, name='nombrar_admin'),
    url(r'^aceptar_membresia/(?P<usuario_joinity_id>\d+)/$', views.aceptar_membresia, name='aceptar_membresia'),
    url(r'^(?P<joinity_id>\d+)/evento/(?P<evento_id>\d+)/unirse/$', views.unirse_evento, name='unirse_evento'),
    url(r'^filtrar/$', views.filtro, name="filtrar"),
)
