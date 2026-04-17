from django.urls import path
from . import views

urlpatterns = [
    path('mis-comentarios/<int:paquete_id>/', views.ver_comentarios, name='comentarios'),
]