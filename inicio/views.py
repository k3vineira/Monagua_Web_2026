from django.shortcuts import render

def IndexView(request):
    context={
        'nombre': 'kevin neira',
        'titulo': 'Página de Inicio'
    }
    return render(request, 'index.html', context)