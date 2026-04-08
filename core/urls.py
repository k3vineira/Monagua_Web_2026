from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from gestion_admin import views as views_gestion
from . import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')),       # Maneja el home
    path('usuario/', include('usuario.urls')),
    path('reservas/', include('reservas.urls')), # Eliminada duplicidad
   path('pago/', include('pago.urls')),
    
    # pefil de usuario
    path('perfil/', include('perfil.urls')),
    
    # Recuperación de contraseña (Password Reset)
    path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='recuperar.html'), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
    
    path('gestion-admin/', views_gestion.dashboard_administrador, name='gestion_admin'),
]
# Agrega esto al final para que cargue las fotos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)