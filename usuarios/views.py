from django.shortcuts import render

def registro(request):
    return render(request, 'usuarios/registro.html')

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

from django.shortcuts import render

def vista_registro(request):
    # Aquí le decimos qué archivo HTML debe cargar
    return render(request, 'usuarios/registro.html')