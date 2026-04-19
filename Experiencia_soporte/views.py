from django.shortcuts import render

def ver_comentarios(request, paquete_id=None):
    """
    Si paquete_id existe, filtramos por tour.
    Si no existe (llamada desde el navbar), mostramos los del usuario logueado.
    """
    # Por ahora solo renderizamos el template como tienes configurado
    return render(request, 'comentarios.html')