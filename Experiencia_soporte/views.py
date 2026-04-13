from django.shortcuts import render

def lista_comentarios(request):
    return render(request, 'comentarios.html')