from django.conf.urls import patterns, url
from brands import views
urlpatterns = patterns('',
    url(r'^(?P<id_brand>\d+)/$', views.ver, name='ver_brand'),
    url(r'^(?P<id_brand>\d+)/joinity/(?P<joinity_id>\d+)$', views.ver, name='ver_brand_joinity'),
    url(r'^(?P<id_brand>\d+)/editar/$', views.editar, name='editar'),

)
