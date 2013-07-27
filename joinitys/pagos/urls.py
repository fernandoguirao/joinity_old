from django.conf.urls import patterns, url

from joinitys.pagos import views
urlpatterns = patterns('',
    url(r'^crear/', views.crear, name='crear_pagos'),
    url(r'(?P<pago_id>\d+)/cancelar/$', views.cancelar, name='cancelar_pago'),
)
