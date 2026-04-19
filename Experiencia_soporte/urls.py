from django.urls import path
from . import views

urlpatterns = [
    # Esta ruta ahora es general para el historial del usuario
    path('mis-comentarios/', views.ver_comentarios, name='comentarios'),
]