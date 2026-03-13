# mi_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')), # Conecta las URLs de tu app
    path('usuarios/', include('usuarios.urls')), # Conecta las URLs de la app usuarios
]