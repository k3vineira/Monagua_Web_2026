from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import  Pago

class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

class PagoEditarForm(ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'