from django.conf.urls import patterns, include, url
from usuario import views as login_views
from joinitys import views as joinitys_views
from django.contrib import admin
from django.conf.urls.static import static
from joinity import settings
from reservas import views as reservas_views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', joinitys_views.index, name="Inicio"),
    url(r'^login/', login_views.login_user, name="login"),
    url(r'^accounts/login/', login_views.login_user, name="login"),
    url(r'^logout/', login_views.logout_user, name="logout"),
    url(r'^pagos/', include('pagos.urls', namespace="pagos")),
    url(r'^joinity/', include('joinitys.urls', namespace="joinitys")),
    url(r'^email/', login_views.mandarmail, name="emailmandar"),
    url(r'^usuario/', include('usuario.urls', namespace="usuario")),
    url(r'^mensaje/', include('mensajes.urls', namespace="mensajes")),
    url(r'^amigo/', include('amigos.urls', namespace="amigos")),
    url(r'^categorias/', include('categorias.urls', namespace="categorias")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^empresa/editar/(?P<empresa_id>\d+)/$', reservas_views.editar_reserva, name="editar_empresa"),
    url(r'^empresa/seguir/(?P<empresa_id>\d+)/$', reservas_views.seguir_empresa, name="seguir_empresa"),
    url(r'^empresa/(?P<empresa_id>\d+)/$', reservas_views.ver_empresa, name="ver_empresa"),
    url(r'^reserva/confirmar/(?P<reserva_id>\d+)/$', joinitys_views.confirmar, name="confirmar_reserva"),
    url(r'^reserva/aprobar/(?P<reserva_id>\d+)/$', joinitys_views.aprobar, name="aprobar_reserva"),
    url(r'^mis_joinitys/$', joinitys_views.mis_joinitys, name='mis_joinitys'),
    url(r'^mis_tareas/$', joinitys_views.mis_tareas, name='mis_tareas'),
    url(r'^mis_eventos/$', joinitys_views.mis_eventos, name='mis_eventos'),


)
urlpatterns += patterns('',
    (r'^ipn/', include('paypal.standard.ipn.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += patterns('',
        (r'%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), 
            'django.views.static.serve',
            {'document_root' : settings.STATIC_ROOT }),)