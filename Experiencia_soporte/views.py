from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resena
from .forms import ResenaForm
from reservas.models import Paquete

@login_required
def ver_comentarios(request, paquete_id=None):
    paquete = None
    if paquete_id:
        paquete = get_object_or_404(Paquete, id=paquete_id)

    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.usuario = request.user
            if paquete:
                resena.paquete = paquete
            resena.save()
            messages.success(request, "¡Gracias! Tu reseña ha sido publicada con éxito.")
            return redirect('comentarios')
    else:
        initial_data = {}
        if paquete:
            initial_data['paquete'] = paquete
        form = ResenaForm(initial=initial_data)

    if paquete:
        comentarios = Resena.objects.filter(paquete=paquete).order_by('-fecha')
        titulo_pagina = f"Comentarios de {paquete.nombre}"
    else:
        comentarios = Resena.objects.filter(usuario=request.user).order_by('-fecha')
        titulo_pagina = "Mis Comentarios"

    context = {'form': form, 'comentarios': comentarios, 'titulo_pagina': titulo_pagina, 'paquete_especifico': paquete}
    return render(request, 'comentarios.html', context)