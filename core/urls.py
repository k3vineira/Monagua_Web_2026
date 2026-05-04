from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from administrador import views as views_gestion
from usuario.views import *
from Experiencia_soporte import views as soporte_views
from . import views


urlpatterns = [

    # 1. Admin de Django
    path('admin/', admin.site.urls),

    # Dashboard usuario
    path('inicio-usuario/', views.inicio, name='inicio_usuario'),

    # Apps
    path('', include('inicio.urls')),
    path('reservas/', include('reservas.urls')),
    path('usuario/', include('usuario.urls')),
    path('Experiencia_soporte/', include('Experiencia_soporte.urls')),
    path('tour/<int:paquete_id>/resenas/', soporte_views.ver_comentarios, name='ver_resenas'),
    path('pago/', include('pago.urls')),

    # 🔥 SOLUCIÓN AQUÍ
    path('terminos/', TemplateView.as_view(template_name='terminos.html'), name='terminos'),

    # Autenticación
    path('registro/', registro_view, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='inicio_sesion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Admin
    path('gestion-admin/', views_gestion.dashboard_administrador, name='gestion_admin'),
    path('administrador/', views_gestion.dashboard_administrador, name='administrador'),

    # Guía
    path('inicio-guia/', dashboard_guia_view, name='inicio_guia'),

    # Recuperación contraseña
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

    # Gestión de guías
    path('administrador/guias/', views_gestion.gestion_guias, name='gestion_guias'),
    path('administrador/guias/guardar/', views_gestion.guias_guardar, name='guias_guardar'),
    path('administrador/guias/baja/', views_gestion.guias_baja, name='guias_baja'),
    path('administrador/guias/reactivar/', views_gestion.guias_reactivar, name='guias_reactivar'),
    path('administrador/guias/detalle/<int:guia_id>/', views_gestion.guia_detalle_json, name='guia_detalle_json'),

    # Promociones
    path('administrador/promociones/', views_gestion.gestion_promociones, name='gestion_promociones'),
    path('administrador/promociones/guardar/', views_gestion.guardar_promocion, name='guardar_promocion'),
    path('administrador/promociones/eliminar/<int:pk>/', views_gestion.eliminar_promocion, name='eliminar_promocion'),

    # Comentarios
    path('administrador/comentarios/', views_gestion.gestion_comentarios, name='gestion_comentarios'),

    # Reportes
    path('administrador/reportes/', views_gestion.gestion_reportes, name='gestion_reportes'),
    path('administrador/reportes/guardar/', views_gestion.reportes_guardar, name='reportes_guardar'),
    path('administrador/reportes/detalle/<int:pk>/', views_gestion.reportes_detalle_json, name='reportes_detalle_json'),
    path('administrador/reportes/resolver/', views_gestion.reportes_resolver, name='reportes_resolver'),
    path('administrador/reportes/eliminar/', views_gestion.reportes_eliminar, name='reportes_eliminar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)