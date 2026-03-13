from django.urls import path
from . import views

urlpatterns = [
    # Esta ruta cargará la vista que creamos en el paso 1
    path('registro/', views.vista_registro, name='registro'),
]