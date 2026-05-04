from django import forms
from .models import Guia, Paquete

class GuiaForm(forms.ModelForm):
    class Meta:
        model = Guia
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'especialidad', 'paquete_asignado']
        widgets = {
            # Esto le da el diseño bonito de Bootstrap al selector
            'paquete_asignado': forms.Select(attrs={'class': 'form-control'}),
        }
        