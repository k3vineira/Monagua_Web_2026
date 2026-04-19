from django import forms
from .models import Resena

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['paquete', 'estrellas', 'contenido']
        labels = {
            'paquete': 'Selecciona el Tour',
            'estrellas': 'Calificación (1 a 5)',
            'contenido': 'Tu experiencia',
        }
        widgets = {
            'paquete': forms.Select(attrs={'class': 'form-select'}),
            'estrellas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos qué tal te pareció la ruta...'}),
        }