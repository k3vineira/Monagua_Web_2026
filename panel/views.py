from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from .models import Tour, Reserva
from .models import Tour, Reserva, Guia

User = get_user_model()

@staff_member_required
def dashboard_administrador(request):
    # 1. Total de usuarios registrados
    total_usuarios = User.objects.count()

    # 2. Total de ventas (Sumamos el campo 'total_pagado' de todas las reservas)
    total_ventas_dict = Reserva.objects.aggregate(Sum('total_pagado'))
    total_ventas = total_ventas_dict['total_pagado__sum'] or 0.00 # Si no hay ventas, devuelve 0

    # 3. Tours más populares (Contamos cuántas reservas tiene cada tour y ordenamos de mayor a menor)
    tours_populares = Tour.objects.annotate(
        numero_reservas=Count('reservas')
    ).order_by('-numero_reservas')[:5] # Traemos solo el Top 5

    # 4. Total de reservas realizadas
    total_reservas = Reserva.objects.count()

    contexto = {
        'total_usuarios': total_usuarios,
        'total_ventas': total_ventas,
        'tours_populares': tours_populares,
        'total_reservas': total_reservas,
    }
    return render(request, 'panel.html', contexto)

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
    # logic to save guides
    return render(request, 'guias.html')

@staff_member_required
def guias_baja(request):
    # logic to deactivate guides
    return render(request, 'guias.html')

@staff_member_required
def guias_reactivar(request):
    # logic to reactivate guides
    return render(request, 'guias.html')