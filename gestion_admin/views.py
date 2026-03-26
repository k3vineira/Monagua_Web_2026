from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from .models import Tour, Reserva

@staff_member_required
def dashboard_administrador(request):
    # 1. Total de usuarios registrados
    total_usuarios = User.objects.count()

    # 2. Total de ventas (Sumamos el campo 'total_pagado' de todas las reservas)
    total_ventas_dict = Reserva.objects.aggregate(Sum('total_pagado'))
    total_ventas = total_ventas_dict['total_pagado__sum'] or 0.00 # Si no hay ventas, devuelve 0

    # 3. Tours más populares (Contamos cuántas reservas tiene cada tour y ordenamos de mayor a menor)
    tours_populares = Tour.objects.annotate(
        numero_reservas=Count('reserva')
    ).order_by('-numero_reservas')[:5] # Traemos solo el Top 5

    # 4. Total de reservas realizadas
    total_reservas = Reserva.objects.count()

    contexto = {
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