from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, PerfilTurista  # Importamos tu modelo personalizado
from django.contrib.auth.decorators import login_required, user_passes_test
from panel.models import Reserva
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from functools import wraps

# ─── DECORADORES DE ROL ───

def es_guia_required(view_func):
    """ Solo permite el acceso a usuarios que tengan es_guia=True """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'es_guia', False):
            return view_func(request, *args, **kwargs)
        messages.error(request, "No tienes permisos de Guía para acceder aquí.")
        return redirect('login')
    return _wrapped_view

def es_turista_required(view_func):
    """ Solo permite el acceso a usuarios que tengan es_turista=True """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'es_turista', False):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Esta sección es exclusiva para Turistas.")
        return redirect('login')
    return _wrapped_view

# ─── VISTAS DE DASHBOARDS ───

@login_required
@es_turista_required
def dashboard_view(request):
    # Pasamos el usuario a la plantilla (aunque Django lo hace por defecto)
    return render(request, 'dashboard.html')

@login_required
@es_guia_required
def dashboard_guia_view(request):
    """ Apartado para que el guía vea sus rutas asignadas """
    return render(request, 'dashboard_guia.html')

@login_required
def perfil_usuario_view(request):
    user = request.user
    if request.method == 'POST':
        # Caso 1: Actualización de Imagen de Perfil
        if 'imagen_perfil' in request.FILES:
            user.imagen_perfil = request.FILES['imagen_perfil']
            user.save()
            messages.success(request, "¡Foto de perfil actualizada correctamente!")
        
        # Caso 2: Actualización de Datos Personales
        elif 'editar_perfil' in request.POST:
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.tipo_documento = request.POST.get('tipo_documento', user.tipo_documento)
            user.telefono = request.POST.get('telefono', user.telefono)
            user.residencia = request.POST.get('residencia', user.residencia)
            user.save()
            messages.success(request, "¡Perfil actualizado con éxito!")
            
        return redirect('detalles')
    return render(request, 'detalles.html')
def registro_view(request):
    if request.method == 'POST':
        # 1. Capturamos los datos del POST (Coinciden con los 'name' de tu HTML)
        nombres = request.POST.get('nombres')
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
                return redirect('inicio_usuario') # Redirige al dashboard personal
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def terminos_condiciones(request):
    return render(request, 'terminos.html')

@login_required
def mis_pagos_view(request):
    """ Muestra el historial de reservas y pagos del usuario """
    pagos = Reserva.objects.filter(usuario=request.user).order_by('-fecha_reserva')
    return render(request, 'mis_pagos.html', {'pagos': pagos})

@login_required
def descargar_recibo_view(request, reserva_id):
    """ Genera un PDF con el detalle del pago utilizando ReportLab """
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Diseño básico del recibo
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "MONAGUA - COMPROBANTE DE PAGO")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Referencia de Reserva: #MON-{reserva.id}")
    p.drawString(100, 755, f"Fecha de Emisión: {reserva.fecha_reserva.strftime('%d/%m/%Y %H:%M')}")
    p.line(100, 745, 500, 745)

    p.drawString(100, 720, f"Cliente: {reserva.usuario.get_full_name() or reserva.usuario.username}")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 680, "RESUMEN DEL TOUR:")
    p.setFont("Helvetica", 12)
    p.drawString(120, 660, f"Tour: {reserva.tour.nombre}")
    p.drawString(120, 645, f"Destino: {reserva.tour.destino}")
    p.drawString(120, 630, f"Estado: {reserva.get_estado_display()}")
    
    p.line(100, 610, 500, 610)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 590, f"VALOR PAGADO: ${reserva.total_pagado}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')