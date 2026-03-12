from django.contrib import admin
from django.urls import path
from usuarios.views import registro, principal, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registro),
    path('principal/', principal),
    path('login/', login),
]