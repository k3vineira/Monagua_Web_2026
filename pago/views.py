from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pago
from .forms import PagoForm, PagoEditarForm


#pagos
def crear_pago(request):
    if request.method == 'POST':

        form = PagoForm(request.POST, request.FILES) 
        if form.is_valid():
            pago = form.save()
            messages.success(request, f"Pago de {pago.nombre_cliente} creado correctamente.")
            return redirect('pago') 
        else:
            messages.error(request, "Error al crear el pago. Por favor verifica los datos.")
    else:
        form = PagoForm()

    context = {
        'form': form,
        'titulo': 'Crear Nuevo Pago',
    }
    return render(request, 'pago.html', context)

def editar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)

    if request.method == 'POST':
        form = PagoEditarForm(request.POST, request.FILES, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {pago.nombre_cliente} actualizados correctamente.")
            return redirect('crear_pago')
        else:
            messages.error(request, "Error al actualizar. Revisa los campos marcados en rojo.")
    else:
        form = PagoEditarForm(instance=pago)

    context = {
        'form': form,
        'titulo': f'Editar a {pago.nombre_cliente}',
    }
    return render(request, 'pago.html', context)