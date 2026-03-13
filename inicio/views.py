from django.shortcuts import render

def inicio_inicio(request):
    context={
        'nombre': 'kevin neira',
        'titulo': 'Página de Inicio'
    }
    return render(request, 'index.html', context)