
from django.shortcuts import render

def registro(request):
    return render(request, 'usuarios/registro.html')

def principal(request):
    return render(request, 'usuarios/principal.html')

def login(request):
    return render(request, 'usuarios/login.html')

from django.shortcuts import render, redirect
from .models import Usuario

def registro(request):

    if request.method == 'POST':

        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        tipo_documento = request.POST['tipo_documento']
        numero_documento = request.POST['numero_documento']
        correo = request.POST['correo']
        password = request.POST['password']

        usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            correo=correo,
            password=password
        )

        usuario.save()

        return redirect('/login/')

    return render(request, 'usuarios/registro.html')