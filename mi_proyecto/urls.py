from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from panel import views as views_gestion
from . import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')),       # Maneja el home
    path('reservas/', include('reservas.urls')),
    path('usuario/', include('usuario.urls')),
    path('reservas/', include('reservas.urls')),# Maneja destinos, blog y reservas
    
   # Autenticación (Login / Logout)
    # IMPORTANTE: El 'name' debe ser 'login' para que tus templates funcionen
    path('login/', auth_views.LoginView.as_view(template_name='inicio_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # pefil de usuario
    path('perfil/', include('perfil.urls')),
    
    # Recuperación de contraseña (Password Reset)
    path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='recuperar.html'), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
        
  
   path('admin/', admin.site.urls),
    # Cambia la línea 29 por esta:
    path('panel/', views_gestion.dashboard_administrador, name='panel'),


    # Gestión de guías
    path('panel/guias/', views_gestion.gestion_guias, name='gestion_guias'),
    path('panel/guias/guardar/', views_gestion.guias_guardar, name='guias_guardar'),
    path('panel/guias/baja/', views_gestion.guias_baja, name='guias_baja'),
    path('panel/guias/reactivar/', views_gestion.guias_reactivar, name='guias_reactivar'),
]

