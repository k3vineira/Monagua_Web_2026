from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from gestion_admin import views as views_gestion
from . import views

urlpatterns = [
    # 1. Administración (Siempre es mejor dejarlo de primero)
    path('admin/', admin.site.urls), 
    # 2. Aplicaciones principales
    path('', include('inicio.urls')),                # Home / Inicio
    path('reservas/', include('reservas.urls')),     # Destinos, blog y reservas (Solo una vez)
    path('usuario/', include('usuario.urls')),       # Registro y gestión de usuarios
    path('pago/', include('pago.urls')),             # Pasarela de pagos
    path('perfil/', include('perfil.urls')),         # Perfil del usuario logueado
    
    # 3. Autenticación (Login / Logout)
    path('login/', auth_views.LoginView.as_view(template_name='inicio_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # 4. Recuperación de contraseña
    path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='recuperar.html'), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
    
    # 5. Dashboard Administrativo personalizado
    path('gestion-admin/', views_gestion.dashboard_administrador, name='gestion_admin'),
]

# Configuración para archivos multimedia (Imágenes de destinos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)