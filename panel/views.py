from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Tour, Reserva, Guia

User = get_user_model()


# ══════════════════════════════════════════════
#  DASHBOARD ADMINISTRADOR
# ══════════════════════════════════════════════
@staff_member_required
def dashboard_administrador(request):

    # Total usuarios registrados
    total_usuarios = User.objects.count()

    # Total ventas (suma de total_pagado en todas las reservas)
    total_ventas = Reserva.objects.aggregate(
        t=Sum('total_pagado')
    )['t'] or 0.00

    # Total reservas
    total_reservas = Reserva.objects.count()

    # Total tours activos (todos los tours, ya que no tienes campo activo/inactivo en Tour)
    total_tours = Tour.objects.count()

    # Top 5 tours más populares con número de reservas
    tours_populares = Tour.objects.annotate(
        numero_reservas=Count('reservas')
    ).order_by('-numero_reservas')[:5]

    context = {
        'total_usuarios':  total_usuarios,
        'total_ventas':    total_ventas,
        'total_reservas':  total_reservas,
        'total_tours':     total_tours,
        'tours_populares': tours_populares,
    }
    return render(request, 'panel.html', context)


# ══════════════════════════════════════════════
#  GESTIÓN DE GUÍAS — LISTA
# ══════════════════════════════════════════════
@staff_member_required
def gestion_guias(request):
    guias = Guia.objects.all()

    context = {
        'guias':                 guias,
        'total_guias':           guias.count(),
        'total_guias_activos':   guias.filter(estado='Activo').count(),
        'total_guias_inactivos': guias.filter(estado='Inactivo').count(),
        'guias_asignados':       guias.filter(estado='Activo', disponibilidad='Ocupado').count(),
    }
    return render(request, 'guias.html', context)


# ══════════════════════════════════════════════
#  GUARDAR GUÍA (Crear o Editar)
# ══════════════════════════════════════════════
@staff_member_required
def guias_guardar(request):
    print("--- INICIANDO PROCESO DE GUARDAR GUÍA ---") # Rastreador 1
    
    if request.method != 'POST':
        return redirect('gestion_guias')

    guia_id = request.POST.get('guia_id', '').strip()

    # CORRECCIÓN VITAL: Manejo seguro del campo número
    exp_str = request.POST.get('experiencia', '').strip()
    exp_val = int(exp_str) if exp_str.isdigit() else 0

    # Recogemos todos los campos del formulario
    campos = {
        'nombre':          request.POST.get('nombre', '').strip(),
        'apellido':        request.POST.get('apellido', '').strip(),
        'correo':          request.POST.get('correo', '').strip(),
        'telefono':        request.POST.get('telefono', '').strip(),
        'documento':       request.POST.get('documento', '').strip() or None,
        'especialidad':    request.POST.get('especialidad', ''),
        'disponibilidad':  request.POST.get('disponibilidad', 'Disponible'),
        'experiencia':     exp_val, # Usamos la variable segura
        'idiomas':         request.POST.get('idiomas', '').strip() or None,
        'certificaciones': request.POST.get('certificaciones', '').strip() or None,
        'notas':           request.POST.get('notas', '').strip() or None,
    }

    print("DATOS CAPTURADOS DEL HTML:", campos) # Rastreador 2

    try:
        if guia_id:
            # ── EDITAR guía existente ──
            guia = get_object_or_404(Guia, pk=guia_id)
            
            # Verificamos si el correo ya existe en OTRO guía
            if Guia.objects.exclude(pk=guia_id).filter(correo=campos['correo']).exists():
                print("ERROR: Correo duplicado al editar")
                return redirect('/panel/guias/?msg=error_correo')

            for attr, valor in campos.items():
                setattr(guia, attr, valor)
            guia.save()
            print("¡GUÍA ACTUALIZADO CON ÉXITO EN LA BD!")
            return redirect('/panel/guias/?msg=editado')
            
        else:
            # ── CREAR nuevo guía ──
            # Verificamos si el correo ya existe antes de intentar crear
            if Guia.objects.filter(correo=campos['correo']).exists():
                print("ERROR: Correo duplicado al crear nuevo")
                return redirect('/panel/guias/?msg=error_correo')

            # Asignamos color de avatar automáticamente por rotación
            colores = Guia.COLORES_AVATAR
            total   = Guia.objects.count()
            campos['color_avatar'] = colores[total % len(colores)]

            nuevo_guia = Guia.objects.create(**campos)
            print(f"¡GUÍA CREADO CON ÉXITO! ID asignado: {nuevo_guia.id}") # Rastreador 3
            return redirect('/panel/guias/?msg=creado')

    except IntegrityError as e:
        print(f"!!! ERROR DE INTEGRIDAD EN LA BD !!!: {e}")
        return redirect('/panel/guias/?msg=error_bd')
    except Exception as e:
        print(f"!!! ERROR FATAL AL GUARDAR EN LA BD !!!: {e}")
        return redirect('/panel/guias/?msg=error_bd')


# ══════════════════════════════════════════════
#  DAR DE BAJA (Inactivo)
# ══════════════════════════════════════════════
@staff_member_required
def guias_baja(request):
    if request.method == 'POST':
        guia = get_object_or_404(Guia, pk=request.POST.get('guia_id'))
        guia.estado         = 'Inactivo'
        guia.disponibilidad = 'Ocupado'   # ya no está disponible
        guia.save()
    return redirect('/panel/guias/?msg=baja')


# ══════════════════════════════════════════════
#  REACTIVAR GUÍA
# ══════════════════════════════════════════════
@staff_member_required
def guias_reactivar(request):
    if request.method == 'POST':
        guia = get_object_or_404(Guia, pk=request.POST.get('guia_id'))
        guia.estado         = 'Activo'
        guia.disponibilidad = 'Disponible'
        guia.save()
    return redirect('/panel/guias/?msg=reactivado')


# ══════════════════════════════════════════════
#  DETALLE DE GUÍA (JSON para modal de edición)
# ══════════════════════════════════════════════
@staff_member_required
def guia_detalle_json(request, guia_id):
    """Devuelve los datos de un guía en JSON para pre-rellenar el modal de edición."""
    guia = get_object_or_404(Guia, pk=guia_id)
    return JsonResponse({
        'id':              guia.id,
        'nombre':          guia.nombre,
        'apellido':        guia.apellido,
        'correo':          guia.correo,
        'telefono':        guia.telefono,
        'documento':       guia.documento or '',
        'especialidad':    guia.especialidad,
        'disponibilidad':  guia.disponibilidad,
        'experiencia':     guia.experiencia,
        'idiomas':         guia.idiomas or '',
        'certificaciones': guia.certificaciones or '',
        'notas':           guia.notas or '',
        'estado':          guia.estado,
    })