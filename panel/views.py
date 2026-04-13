from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
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

    if guia_id:
        # ── EDITAR guía existente ──
        guia = get_object_or_404(Guia, pk=guia_id)
        for attr, valor in campos.items():
            setattr(guia, attr, valor)
        guia.save()
        return redirect('/panel/guias/?msg=editado')
    else:
        # ── CREAR nuevo guía ──
        # Asignamos color de avatar automáticamente por rotación
        colores = Guia.COLORES_AVATAR
        total   = Guia.objects.count()
        campos['color_avatar'] = colores[total % len(colores)]

        Guia.objects.create(**campos)
        return redirect('/panel/guias/?msg=creado')


# ══════════════════════════════════════════════
#  DAR DE BAJA (Inactivo)
# ══════════════════════════════════════════════
@staff_member_required
def guias_baja(request):
    if request.method == 'POST':
        guia = get_object_or_404(Guia, pk=request.POST.get('guia_id'))
        guia.estado        = 'Inactivo'
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
        guia.estado        = 'Activo'
        guia.disponibilidad = 'Disponible'
        guia.save()
    return redirect('/panel/guias/?msg=reactivado')