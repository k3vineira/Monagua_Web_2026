from django.urls import path
from . import views  

urlpatterns = [
    # Cuando alguien entre a /usuario/login/ se ejecutará la función 'login_view'
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
]