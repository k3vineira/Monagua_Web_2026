from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from panel import views as views_gestion
from usuario import views as views_usuario
from . import views
 
urlpatterns = [
    # 1. Admin de Django
    path('admin/', admin.site.urls),

    # Dashboard de usuario logueado (desde core/views.py)
    path('inicio-usuario/', views.inicio, name='inicio_usuario'),
    
    # 2. Tus aplicaciones
    path('', include('inicio.urls')),
    path('reservas/', include('reservas.urls')), # <--- Esto conecta con el código de arriba
    path('usuario/', include('usuario.urls')),
    path('Experiencia_soporte/', include('Experiencia_soporte.urls')),
    path('pago/', include('pago.urls')),
    
    # 3. Autenticación y Gestión
    path('login/', auth_views.LoginView.as_view(template_name='inicio_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('gestion-admin/', views_gestion.dashboard_administrador, name='gestion_admin'),
    
    # Dashboard de Guía
    path('inicio-guia/', views_usuario.dashboard_guia_view, name='inicio_guia'),
    
    # 4. Recuperación de contraseña
    path('recuperar-password/', auth_views.PasswordResetView.as_view(template_name='recuperar.html'), name='password_reset'),
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('recuperar/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
        
  

    # Cambia la línea 29 por esta:
    path('panel/', views_gestion.dashboard_administrador, name='panel'),


    # Gestión de guías
    path('panel/guias/', views_gestion.gestion_guias, name='gestion_guias'),
    path('panel/guias/guardar/', views_gestion.guias_guardar, name='guias_guardar'),
    path('panel/guias/baja/', views_gestion.guias_baja, name='guias_baja'),
    path('panel/guias/reactivar/', views_gestion.guias_reactivar, name='guias_reactivar'),
    # Agrega esta línea junto a las demás rutas de guías:
    path('panel/guias/detalle/<int:guia_id>/', views_gestion.guia_detalle_json, name='guia_detalle_json'),
]

# Servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
