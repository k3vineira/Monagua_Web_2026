from django.urls import path
from . import views  
from .views import registro_view

urlpatterns = [
    # Cuando alguien entre a /usuario/login/ se ejecutará la función 'login_view'
    path('login/', views.login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('terminos-y-condiciones/', views.terminos_condiciones, name="terminos"),
]