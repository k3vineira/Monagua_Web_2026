from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, PerfilTurista  # Importamos tu modelo personalizado

def registro_view(request):
    if request.method == 'POST':
        # 1. Capturamos los datos del POST (Coinciden con los 'name' de tu HTML)
        nombres = request.POST.get('nombres')
        
        print("¡ATENCIÓN: He recibido un POST del formulario!")
        
        apellidos = request.POST.get('apellidos')
        tipo_doc = request.POST.get('tipo_documento')
        num_doc = request.POST.get('numero_documento')
        tel = request.POST.get('telefono')
        residencia = request.POST.get('residencia')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # Validación de campos críticos
        if not correo or not password:
            messages.error(request, "Correo y contraseña son obligatorios.")
            return render(request, 'registro.html')

        # 2. Validación DRY: ¿Ya existe este correo?
        if Usuario.objects.filter(email=correo).exists():
            messages.error(request, "Este correo ya está registrado en Monagua.")
            return render(request, 'registro.html')

        # 3. Creación del Usuario usando el modelo personalizado
        # Usamos create_user para que Django encripte la contraseña automáticamente
        try:
            nuevo_usuario = Usuario.objects.create_user(
                username=correo, # El email será el identificador
                email=correo,
                password=password,
                first_name=nombres,
                last_name=apellidos,
                tipo_documento=tipo_doc,
                numero_documento=num_doc,
                telefono=tel,
                residencia=residencia,
                es_turista=True  # Por defecto entran como turistas
            )

            # 4. Creamos su perfil de turista relacionado (MVT)
            PerfilTurista.objects.create(usuario=nuevo_usuario)

            messages.success(request, f"¡Bienvenido a Monagua, {nombres}! Ya puedes iniciar sesión.")
            return redirect('login')
            
        except Exception as e:
            print(f"ERROR CRÍTICO EN DB: {e}")
            messages.error(request, f"Error: {e}")
            return render(request, 'registro.html')

    # Si es GET, simplemente mostramos el template
    return render(request, 'registro.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')  # Redirige a la página principal
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def terminos_condiciones(request):
    return render(request, 'terminos.html')