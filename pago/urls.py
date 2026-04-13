# perfil/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
  path('', views.crear_pago, name='pago'),
]