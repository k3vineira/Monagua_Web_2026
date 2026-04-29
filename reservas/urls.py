from django.urls import path
from . import views 

urlpatterns = [
    path('destinos/', views.destinos, name='destinos'), 
    path('blog/', views.blog_view, name='blog'),
    path('reservar/', views.reservas_view, name='reservas'),
    path('promociones/', views.promociones_view, name='promociones'),

    path('confirmar-reserva/<int:paquete_id>/', views.guardar_reserva, name='guardar_reserva'),
   
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('actividades/editar/<int:pk>/', views.editar_actividad, name='editar_actividad'),
    path('actividades/eliminar/<int:pk>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('promociones/crear/', views.crear_promocion, name='crear_promocion'),
    path('promociones/editar/<int:pk>/', views.editar_promocion, name='editar_promocion'),
    path('promociones/eliminar/<int:pk>/', views.eliminar_promocion, name='eliminar_promocion'),
    path('paquetes/crear/', views.crear_paquete, name='crear_paquete'),
    path('paquetes/editar/<int:pk>/', views.editar_paquete, name='editar_paquete'),
    path('paquetes/eliminar/<int:pk>/', views.eliminar_paquete, name='eliminar_paquete'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
    path('reservas/eliminar/<int:pk>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('pqrs/crear/', views.crear_pqrs, name='crear_pqrs'),
    path('pqrs/editar/<int:pk>/', views.editar_pqrs, name='editar_pqrs'),
    path('pqrs/eliminar/<int:pk>/', views.eliminar_pqrs, name='eliminar_pqrs'),
    path('blog/crear/', views.crear_blog, name='crear_blog'),
    path('blog/editar/<int:pk>/', views.editar_blog, name='editar_blog'),
    path('blog/eliminar/<int:pk>/', views.eliminar_blog, name='eliminar_blog'),
    
    
    path('admin/blog/', views.lista_blog, name='admin_blog'),
    path('admin/actividades/', views.lista_actividades, name='admin_actividades'),
    path('admin/categorias/', views.lista_categorias, name='admin_categorias'),
    path('admin/paquetes/', views.lista_paquetes, name='admin_paquetes'),
    path('admin/promociones/', views.lista_promociones, name='admin_promociones'),
    path('admin/reservas/', views.lista_reservas, name='admin_reservas'),
    path('admin/pqrs/', views.lista_pqrs, name='lista_pqrs'),
   
    path('nosotros/', views.nosotros, name='nosotros'),
]