from django.urls import path
from . import views

urlpatterns = [
    path('', views.crear_pago, name='pago'),
    path('nuevo/', views.crear_pago, name='crear_pago'),
    path('editar/<int:pk>/', views.editar_pago, name='editar_pago'),
    path('factura/', views.factura_vista, name='ver_factura'),
    path('factura/descargar/', views.descargar_factura_pdf, name='descargar_factura'),
]