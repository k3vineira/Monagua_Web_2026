
from django.shortcuts import render

# perfil/views.py
from django.shortcuts import render

def ver_pago(request):
    # Por ahora solo retornamos un render simple
    # Asegúrate de tener el template creado después
    return render(request, 'pago/pago.html')