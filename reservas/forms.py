from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Categoria, Actividades, Paquete, Promocion, Reserva

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class CategoriaEditarForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ActividadesForm(ModelForm):

    class Meta:
        model = Actividades
        fields = ['categoria', 'nombre', 'descripcion', 'duracion', 'nivel_dificultad']
class ActividadesEditarForm(ModelForm):
    class Meta:
        model = Actividades
        fields = '__all__'


class PaqueteForm(ModelForm):

    class Meta:
        model = Paquete
        fields = '__all__'
class PaqueteEditarForm(ModelForm):
    class Meta:
        model = Paquete
        fields = '__all__'
        
        
class PromocionForm(ModelForm):

    class Meta:
        model = Promocion
        fields = '__all__'        
class PromocionEditarForm(ModelForm):
    class Meta:
        model = Promocion
        fields = '__all__'


class ReservaForm(ModelForm):

    class Meta:
        model = Reserva
        fields = '__all__'   
class ReservaEditarForm(ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'    
    

        
        
        
