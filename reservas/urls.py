from django.urls import path
from . import views 

urlpatterns = [
    path('destinos/', views.destinos_view, name='destinos'),
    path('blog/', views.blog_view, name='blog'),
    path('crear/', views.crear_reserva, name='ir_a_reservas'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('actividades/crear/', views.crear_actividad, name='crear_actividad'),
    path('promociones/crear/', views.crear_promocion, name='crear_promocion'),
    path('paquetes/crear/', views.crear_paquete, name='crear_paquete'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva')
    
]