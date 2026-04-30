from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('gestion-usuarios/', views.gestion_usuarios_view, name='gestion_usuarios'),
    path('asignar-rol-guia/<int:user_id>/', views.asignar_rol_guia, name='asignar_rol_guia'),
    path('perfil/', views.perfil_usuario_view, name='detalles'),
    path('logout/', views.logout_view, name='logout_usuario'),
]