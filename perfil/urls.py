# perfil/urls.py
from django.urls import path
from . import views

app_name = 'perfil' # Namespace para evitar conflictos

urlpatterns = [
    # Ejemplo: ruta para ver el perfil
    path('ver/', views.ver_perfil, name='ver_perfil'),
]