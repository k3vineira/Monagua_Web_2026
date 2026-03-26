from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    # Django buscará automáticamente en la carpeta 'templates'
    return render(request, 'inicio_sesion.html')
def registro_view(request):
    if request.method == 'POST':
        # 1. Capturar los datos que vienen del formulario HTML
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        tipo_documento = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # 2. Validar que el usuario no exista ya en la base de datos
        if User.objects.filter(email=correo).exists():
            # Opcional: Puedes enviar un mensaje de error al frontend
            messages.error(request, 'Este correo ya está registrado.')
            return redirect('registro') # Nombre de la ruta de esta misma página

        # 3. Crear el usuario en el sistema de autenticación de Django
        # Nota: Django exige un 'username'. Como tu formulario no lo pide, usamos el correo.
        usuario = User.objects.create_user(
            username=correo,
            email=correo,
            password=password,
            first_name=nombres,
            last_name=apellidos
        )
        messages.success(request, 'Cuenta creada exitosamente. ¡Bienvenido a Monagua!')
        return redirect('login') # Cambia 'login' por el nombre de tu ruta de inicio de sesión

    # Si el método es GET (simplemente entró a la página), mostramos el formulario
    return render(request, 'registro.html') # Asegúrate de poner la ruta correcta de tu template
def terminos_condiciones(request):
    return render(request, 'terminos.html')