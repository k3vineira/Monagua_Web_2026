# urls.py administrador 

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from administrador import views as views_gestion
from usuario.views import * 
from Experiencia_soporte import views as soporte_views
from . import views

 
urlpatterns = [

    # 1. Admin de Django
    path('admin/', admin.site.urls),

    # Dashboard de usuario logueado (desde core/views.py)
    path('inicio-usuario/', views.inicio, name='inicio_usuario'),

    
    # 2. Tus aplicaciones
    path('', include('inicio.urls')),
    path('reservas/', include('reservas.urls')),
    path('usuario/', include('usuario.urls')),
    path('Experiencia_soporte/', include('Experiencia_soporte.urls')),
    path('tour/<int:paquete_id>/resenas/', soporte_views.ver_comentarios, name='ver_resenas'),
    path('pago/', include('pago.urls')),


    # 3. Autenticación y Gestión
    # path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='inicio_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('gestion-admin/', views_gestion.dashboard_administrador, name='gestion_admin'),

    
    # Dashboard de Guía
    path('inicio-guia/', dashboard_guia_view, name='inicio_guia'),


    # 4. Recuperación de contraseña
    path('recuperar-contraseña/', auth_views.PasswordResetView.as_view(
        template_name='recuperar.html'
    ), name='password_reset'),

    path('recuperar-contraseña/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='contraseña_reset_enviado.html'
    ), name='password_reset_done'),

    path('recuperar-contraseña/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='contraseña_reset_form.html'
    ), name='password_reset_confirm'),

    path('recuperar-contraseña/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='contraseña_reset_guardar.html'
    ), name='password_reset_complete'),


    # ═══════════════════════════════════════
    # PANEL ADMINISTRADOR
    # ═══════════════════════════════════════

    path('administrador/', views_gestion.dashboard_administrador, name='administrador'),


    # Gestión de guías
    path('administrador/guias/', views_gestion.gestion_guias, name='gestion_guias'),
    path('administrador/guias/guardar/', views_gestion.guias_guardar, name='guias_guardar'),
    path('administrador/guias/baja/', views_gestion.guias_baja, name='guias_baja'),
    path('administrador/guias/reactivar/', views_gestion.guias_reactivar, name='guias_reactivar'),
    path('administrador/guias/detalle/<int:guia_id>/', views_gestion.guia_detalle_json, name='guia_detalle_json'),


    # Gestión de Promociones (Banners)
    path('administrador/promociones/', views_gestion.gestion_promociones, name='gestion_promociones'),
    path('administrador/promociones/guardar/', views_gestion.guardar_promocion, name='guardar_promocion'),
    path('administrador/promociones/eliminar/<int:pk>/', views_gestion.eliminar_promocion, name='eliminar_promocion'),


    # Gestión de comentarios
    path('administrador/comentarios/', views_gestion.gestion_comentarios, name='gestion_comentarios'),

]


# Servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)