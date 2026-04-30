from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse # Importar reverse para construir URLs
from .models import Usuario, PerfilTurista
from django.contrib.auth.decorators import login_required, user_passes_test # user_passes_test para control de acceso
from administrador.models import Reserva, Guia # Importar el modelo Guia para el contexto de index-guias.html
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
    """ Dashboard principal para el turista con resumen de actividad """
    reservas_count = Reserva.objects.filter(usuario=request.user).count()
    return render(request, 'dashboard.html', {'reservas_count': reservas_count})

@login_required
@es_guia_required
def dashboard_guia_view(request):
    """ Apartado para que el guía vea sus rutas asignadas """
    return render(request, 'dashboard_guia.html')

# ─── VISTAS DE GESTIÓN DE USUARIOS Y ROLES (ADMIN) ───

@login_required
@user_passes_test(lambda u: u.is_staff) # Solo miembros del staff (administradores) pueden acceder
def gestion_usuarios_view(request):
    """
    Muestra una lista de todos los usuarios registrados para que el administrador
    pueda gestionar sus roles, especialmente el de 'Guía Turístico'.
    También proporciona el contexto necesario para la sección de gestión de guías existente.
    """
    # Datos para la sección de gestión de guías existente (de index-guias.html)
    todas_las_guias = Guia.objects.all()
    total_guias = todas_las_guias.count()
    total_guias_activos = todas_las_guias.filter(estado='Activo').count()
    total_guias_inactivos = todas_las_guias.filter(estado='Inactivo').count()
    guias_asignados = todas_las_guias.filter(disponibilidad='Ocupado', estado='Activo').count()

    # Datos para la nueva sección de gestión de usuarios
    all_users = Usuario.objects.all().order_by('-is_staff', 'username')

    context = {
        # Enviamos solo los guías activos para la tabla principal
        'guias': todas_las_guias.filter(estado='Activo'), 
        'total_guias': total_guias,
        'total_guias_activos': total_guias_activos,
        'total_guias_inactivos': total_guias_inactivos,
        'guias_asignados': guias_asignados,
        'all_users': all_users,
        'total_users': all_users.count(),
    }
    return render(request, 'index-guias.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff) # Solo miembros del staff (administradores) pueden acceder
def asignar_rol_guia(request, user_id):
    """
    Asigna o revoca el rol de 'Guía Turístico' a un usuario.
    """
    user_to_update = get_object_or_404(Usuario, id=user_id)

    if request.method == 'POST':
        user_to_update.es_guia = not user_to_update.es_guia # Alternar el estado
        user_to_update.save()

        if user_to_update.es_guia:
            # Si se convierte en guía, creamos el perfil en el modelo Guia para que aparezca en la tabla superior
            guia_perfil, created = Guia.objects.get_or_create(
                correo=user_to_update.email,
                defaults={
                    'nombre': user_to_update.first_name or user_to_update.username,
                    'apellido': user_to_update.last_name or "",
                    'telefono': user_to_update.telefono or "Sin teléfono",
                    'especialidad': 'Por asignar',
                    'estado': 'Activo',
                    'disponibilidad': 'Disponible'
                }
            )
            # Si el perfil ya existía (estaba inactivo), lo reactivamos
            if not created:
                guia_perfil.estado = 'Activo'
                guia_perfil.disponibilidad = 'Disponible'
                guia_perfil.save()
                
        else:
            # Opcional: Si se revoca, podemos marcar al guía como Inactivo
            Guia.objects.filter(correo=user_to_update.email).update(estado='Inactivo')

        messages.success(request, f"El rol de guía para {user_to_update.get_full_name() or user_to_update.username} ha sido actualizado.")
        return redirect(f"{reverse('gestion_usuarios')}?msg=rol_asignado") # Redirigir con un parámetro para el toast
    
    messages.error(request, "Método no permitido para esta acción.")
    return redirect('gestion_usuarios')

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

            messages.success(request, f"¡Registro realizado con éxito! Bienvenido(a), {nombres}. Ya puedes iniciar sesión.")
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

def logout_view(request):
    """ Finaliza la sesión del usuario y lo redirige al login """
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!")
    return redirect('/')

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