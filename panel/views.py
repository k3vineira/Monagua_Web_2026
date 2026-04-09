from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from .models import Tour, Reserva

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
    }
def dashboard_administrador(request):
    
    # 1. Creas el diccionario 'context' con los datos que tu HTML necesita
    context = {
        'total_ventas': 12500.50,       # Dato de prueba
        'total_usuarios': 342,          # Dato de prueba
        'total_reservas': 89,           # Dato de prueba
        'tours_populares': [            # Lista de prueba para tu tabla
            {'nombre': 'Tour Guatapé', 'precio': 120.00, 'numero_reservas': 45},
            {'nombre': 'City Tour Medellín', 'precio': 50.00, 'numero_reservas': 30},
        ]
    }

    # 2. Ahora sí puedes pasar 'context' al render sin que dé error
    return render(request, 'panel.html', context)# <--- Aquí ocurre el error porque 'context' no existe