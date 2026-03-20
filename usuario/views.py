from django.shortcuts import render

def login_view(request):
    # Django buscará automáticamente en la carpeta 'templates'
    return render(request, 'inicio_sesion.html')
