from django.contrib import admin
from django.urls import path

from inicio.views import *

urlpatterns = [
    path('', IndexView, name='IndexView'),
]