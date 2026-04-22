from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  
from .views import registro_view, login_view

urlpatterns = [
    
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('terminos-y-condiciones/', views.terminos_condiciones, name="terminos"),
    path('perfil/', views.perfil_usuario_view, name='detalles'),
    path('mis-pagos/', views.mis_pagos_view, name='mis_pagos'),
    path('descargar-recibo/<int:reserva_id>/', views.descargar_recibo_view, name='descargar_recibo'),
]