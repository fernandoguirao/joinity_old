from django.conf.urls import patterns, url

from joinitys.pagos import views
urlpatterns = patterns('',
    url(r'^paypal/$', 'pagos.views.paypal', name='paypal'),
    url(r'^crear/', views.crear, name='crear_pagos'),
    url(r'^pagar/(?P<pago_id>\d+)/$', views.pagar, name='pagar'),
    url(r'^confirmado/', views.confirmado, name='confirmado'),
)
