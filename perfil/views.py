
from django.shortcuts import render

# perfil/views.py
from django.shortcuts import render

def ver_perfil(request):
    # Por ahora solo retornamos un render simple
    # Asegúrate de tener el template creado después
    return render(request, 'perfil/detalles.html')