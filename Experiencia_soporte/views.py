from django.shortcuts import render, get_object_or_404
from .models import Resena
from reservas.models import Paquete
from django.db.models import Avg # Importamos Avg para calcular promedios


def ver_comentarios(request, paquete_id):
    # Traemos el tour
    paquete = get_object_or_404(Paquete, id=paquete_id)
    # Traemos sus reseñas
    resenas = paquete.comentarios.all().order_by('-fecha')
    
    # Calculamos el promedio de estrellas
    promedio = resenas.aggregate(Avg('estrellas'))['estrellas__avg']
    promedio = promedio if promedio is not None else 0 # Aseguramos que sea 0 si no hay reseñas
    
    context = {
        'paquete': paquete,
        'resenas': resenas,
        # Calculamos el total de reseñas para el contador del header
        'total_resenas': resenas.count(),
        'promedio': promedio, # Agregamos el promedio al contexto
    }
    return render(request, 'comentarios.html', context)