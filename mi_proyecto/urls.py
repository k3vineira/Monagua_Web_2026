# mi_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', include('inicio.urls')), # Conecta las URLs de tu app
]