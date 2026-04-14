from django.urls import path
from . import views 

urlpatterns = [
    path('destinos/', views.destinos, name='destinos'), 
    path('blog/', views.blog_view, name='blog'),
    path('reservar/', views.reservas_view, name='reservas'),
    path('promociones/', views.promociones_view, name='promociones'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('promociones/crear/', views.crear_promocion, name='crear_promocion'),
    path('paquetes/crear/', views.crear_paquete, name='crear_paquete'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('pqrs/crear/', views.crear_pqrs, name='crear_pqrs'),
    path('blog/crear/', views.crear_blog, name='crear_blog'),
    
    path('admin/blog/', views.lista_blog, name='admin_blog'),
    path('admin/actividades/', views.lista_actividades, name='admin_actividades'),
    path('admin/categorias/', views.lista_categorias, name='admin_categorias'),
    path('admin/paquetes/', views.lista_paquetes, name='admin_paquetes'),
    path('admin/promociones/', views.lista_promociones, name='admin_promociones'),
    path('admin/reservas/', views.lista_reservas, name='admin_reservas'),
]