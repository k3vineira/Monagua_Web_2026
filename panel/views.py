from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from reservas.models import Promocion
from reservas.forms import PromocionForm, PromocionEditarForm
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

    total_promociones = Promocion.objects.count()

    context = {
        'total_usuarios':  total_usuarios,
        'total_ventas':    total_ventas,
        'total_reservas':  total_reservas,
        'total_tours':     total_tours,
        'tours_populares': tours_populares,
        'total_promociones': total_promociones,
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
    if request.method != 'POST':
        return redirect('gestion_guias')

    guia_id = request.POST.get('guia_id', '').strip()

    # Recogemos todos los campos del formulario
    campos = {
        'nombre':          request.POST.get('nombre', '').strip(),
        'apellido':        request.POST.get('apellido', '').strip(),
        'correo':          request.POST.get('correo', '').strip(),
        'telefono':        request.POST.get('telefono', '').strip(),
        'documento':       request.POST.get('documento', '').strip() or None,
        'especialidad':    request.POST.get('especialidad', ''),
        'disponibilidad':  request.POST.get('disponibilidad', 'Disponible'),
        'experiencia':     int(request.POST.get('experiencia') or 0),
        'idiomas':         request.POST.get('idiomas', '').strip() or None,
        'certificaciones': request.POST.get('certificaciones', '').strip() or None,
        'notas':           request.POST.get('notas', '').strip() or None,
    }

    try:
        if guia_id:
            # ── EDITAR guía existente ──
            guia = get_object_or_404(Guia, pk=guia_id)
            
            # Verificamos si el correo ya existe en OTRO guía para evitar el error de IntegrityError
            if Guia.objects.exclude(pk=guia_id).filter(correo=campos['correo']).exists():
                return redirect('gestion_guias')

            for attr, valor in campos.items():
                setattr(guia, attr, valor)
            guia.save()
            return redirect('gestion_guias')
            
        else:
            # ── CREAR nuevo guía ──
            # Verificamos si el correo ya existe antes de intentar crear
            if Guia.objects.filter(correo=campos['correo']).exists():
                return redirect('gestion_guias')

            # Asignamos color de avatar automáticamente por rotación
            colores = Guia.COLORES_AVATAR
            total   = Guia.objects.count()
            campos['color_avatar'] = colores[total % len(colores)]

            Guia.objects.create(**campos)
            return redirect('gestion_guias')

    except IntegrityError:
        # En caso de que ocurra un error de duplicidad no controlado
        return redirect('gestion_guias')
    except Exception as e:
        print(f"Error detectado: {e}")
        return redirect('gestion_guias')


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
    return redirect('gestion_guias')


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
    return redirect('gestion_guias')


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

# ══════════════════════════════════════════════
#  GESTIÓN DE PROMOCIONES Y BANNERS
# ══════════════════════════════════════════════
@staff_member_required
def gestion_promociones(request):
    """Lista todas las promociones para que el administrador las gestione."""
    promociones = Promocion.objects.all().order_by('prioridad', '-id')
    form = PromocionForm()
    return render(request, 'promociones_gestion.html', {
        'promociones': promociones,
        'form': form
    })

@staff_member_required
def guardar_promocion(request):
    """Crea o edita una promoción desde el panel de administración."""
    if request.method == 'POST':
        promocion_id = request.POST.get('promocion_id')
        try:
            if promocion_id:
                promocion = get_object_or_404(Promocion, pk=promocion_id)
                form = PromocionEditarForm(request.POST, request.FILES, instance=promocion)
            else:
                form = PromocionForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                # Aquí podrías agregar un mensaje de éxito: messages.success(request, "Guardado correctamente")
                return redirect('gestion_promociones')
            else:
                print(f"Errores en el formulario: {form.errors}")
        except Exception as e:
            print(f"Error al guardar promoción: {e}")
            
    return redirect('gestion_promociones')

@staff_member_required
def eliminar_promocion(request, pk):
    """Elimina una promoción definitivamente."""
    promocion = get_object_or_404(Promocion, pk=pk)
    promocion.delete()
    return redirect('gestion_promociones')

@staff_member_required
def gestion_comentarios(request):
    """Vista para que el administrador gestione los comentarios y reseñas."""
    return render(request, 'panel.html', {'msg': 'Sección de comentarios en desarrollo'})