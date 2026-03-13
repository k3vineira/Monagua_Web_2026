# mi_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')), # Conecta las URLs de tu app
    path('admin/', admin.site.urls),
    # Aquí conectamos las URLs de tu app usuarios
    path('usuarios/', include('usuarios.urls')), 
    # (Aquí seguramente ya tienes la ruta de tu app inicio)
]