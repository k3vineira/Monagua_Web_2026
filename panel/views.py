from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from .models import Tour, Reserva, Guia
import random

User = get_user_model()


@staff_member_required
def dashboard_administrador(request):
    total_usuarios = User.objects.count()

    total_ventas_dict = Reserva.objects.aggregate(Sum('total_pagado'))
    total_ventas = total_ventas_dict['total_pagado__sum'] or 0.00

    tours_populares = Tour.objects.annotate(
        numero_reservas=Count('reservas')
    ).order_by('-numero_reservas')[:5]

    total_reservas = Reserva.objects.count()
    total_tours = Tour.objects.count()

    context = {
        'total_usuarios': total_usuarios,
        'total_ventas': total_ventas,
        'tours_populares': tours_populares,
        'total_reservas': total_reservas,
        'total_tours': total_tours,
    }
    return render(request, 'panel.html', context)


@staff_member_required
def gestion_guias(request):
    guias = Guia.objects.all()

    total_guias = guias.count()
    total_guias_activos = guias.filter(estado='Activo').count()
    total_guias_inactivos = guias.filter(estado='Inactivo').count()
    # Guías asignados: los que tienen disponibilidad "Ocupado" y están activos
    guias_asignados = guias.filter(estado='Activo', disponibilidad='Ocupado').count()

    context = {
        'guias': guias,
        'total_guias': total_guias,
        'total_guias_activos': total_guias_activos,
        'total_guias_inactivos': total_guias_inactivos,
        'guias_asignados': guias_asignados,
    }
    return render(request, 'guias.html', context)


@staff_member_required
def guias_guardar(request):
    if request.method == 'POST':
        guia_id = request.POST.get('guia_id')
        colores = ['#2c6e3c', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f97316']

        datos = {
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
            # Editar existente
            guia = get_object_or_404(Guia, id=guia_id)
            for campo, valor in datos.items():
                setattr(guia, campo, valor)
            guia.save()
            return redirect('/panel/guias/?msg=editado')
        else:
            # Crear nuevo
            datos['color_avatar'] = random.choice(colores)
            Guia.objects.create(**datos)
            return redirect('/panel/guias/?msg=creado')

    return redirect('/panel/guias/')


@staff_member_required
def guias_baja(request):
    if request.method == 'POST':
        guia_id = request.POST.get('guia_id')
        guia = get_object_or_404(Guia, id=guia_id)
        guia.estado = 'Inactivo'
        guia.disponibilidad = 'Ocupado'  # ya no disponible para asignación
        guia.save()
        return redirect('/panel/guias/?msg=baja')
    return redirect('/panel/guias/')


@staff_member_required
def guias_reactivar(request):
    if request.method == 'POST':
        guia_id = request.POST.get('guia_id')
        guia = get_object_or_404(Guia, id=guia_id)
        guia.estado = 'Activo'
        guia.disponibilidad = 'Disponible'
        guia.save()
        return redirect('/panel/guias/?msg=reactivado')
    return redirect('/panel/guias/')