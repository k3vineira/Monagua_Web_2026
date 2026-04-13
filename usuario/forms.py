from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    ROL_CHOICES = [
        ('turista', 'Turista'),
        ('guia', 'Guía turístico'),
    ]

    rol = forms.ChoiceField(choices=ROL_CHOICES, widget=forms.RadioSelect)
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')