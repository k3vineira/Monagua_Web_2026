from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')),       # Maneja el home
    path('reservas/', include('reservas.urls')),
    path('usuario/', include('usuario.urls')),

]
