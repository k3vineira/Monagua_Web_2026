# perfil/urls.py
from django.urls import path
from . import views

app_name = 'pago' # Namespace para evitar conflictos

urlpatterns = [
    # Ejemplo: ruta para ver el perfil
    path('pago/', views.ver_pago, name='ver_pago'),
]