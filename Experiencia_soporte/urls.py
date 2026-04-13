from django.urls import path
from . import views

urlpatterns = [
    path('mis-comentarios/', views.lista_comentarios, name='comentarios'),
]