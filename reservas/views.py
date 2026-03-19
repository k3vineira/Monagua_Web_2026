from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Actividades, Categoria, Paquete, Promocion, Reserva
from .forms import CategoriaForm, CategoriaEditarForm, ActividadesForm, ActividadesEditarForm, PaqueteForm, PaqueteEditarForm, PromocionForm, PromocionEditarForm, ReservaForm, ReservaEditarForm

def destinos_view(request):
    return render(request, 'destinos.html')

def blog_view(request):
    return render(request, 'blog.html')


def reservas_view(request): 
    return render(request,'reservas.html') 


#categorias
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f"Categoría '{categoria.nombre}' creada correctamente.")
            return redirect('categorias:inicio_categoria')
        else:
            messages.error(request, "Error al crear la categoría. Por favor verifica los datos.")
    else:
        form = CategoriaForm()

    context = {
        'form': form,
        'titulo': 'Crear Nueva Categoría',
    
    }
    return render(request, 'categorias/agregar_categoria.html', context)


def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaEditarForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {categoria.nombre} actualizados correctamente.")
            return redirect('categorias:inicio_categoria')
        else:
            messages.error(request, "Error al actualizar. Revisa los campos marcados en rojo.")
    else:
        form = CategoriaEditarForm(instance=categoria)

    context = {
        'form': form,
        'titulo': f'Editar a {categoria.nombre}',
    
    }
    return render(request, 'categorias/agregar_categoria.html', context)

#actividades
def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadesForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f"Actividad '{actividad.nombre}' creada correctamente.")
            return redirect('actividades:inicio_actividad')
        else:
            messages.error(request, "Error al crear la actividad. Por favor verifica los datos.")
    else:
        form = ActividadesForm()

    context = {
        'form': form,
        'titulo': 'Crear Nueva Actividad',
  
    }
    return render(request, 'actividades/agregar_actividad.html', context)
def editar_actividad(request, pk):
    actividad = get_object_or_404(Actividades, pk=pk)

    if request.method == 'POST':
        form = ActividadesEditarForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {actividad.nombre} actualizados correctamente.")
            return redirect('actividades:inicio_actividad')
        else:
            messages.error(request, "Error al actualizar. Revisa los campos marcados en rojo.")
    else:
        form = ActividadesEditarForm(instance=actividad)

    context = {
        'form': form,
        'titulo': f'Editar a {actividad.nombre}',
     
    }
    return render(request, 'actividades/agregar_actividad.html', context)

#paquetes
def crear_paquete(request):
    if request.method == 'POST':
        form = PaqueteForm(request.POST)
        if form.is_valid():
            paquete = form.save()
            messages.success(request, f"Paquete '{paquete.nombre}' creado correctamente.")
            return redirect('paquetes:inicio_paquete')
        else:
            messages.error(request, "Error al crear el paquete. Por favor verifica los datos.")
    else:
        form = PaqueteForm()

    context = {
        'form': form,
        'titulo': 'Crear Nuevo Paquete',
     
    }
    return render(request, 'paquetes/agregar_paquete.html', context)
def editar_paquete(request, pk):
    paquete = get_object_or_404(Paquete, pk=pk)

    if request.method == 'POST':
        form = PaqueteEditarForm(request.POST, instance=paquete)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {paquete.nombre} actualizados correctamente.")
            return redirect('paquetes:inicio_paquete')
        else:
            messages.error(request, "Error al actualizar. Revisa los campos marcados en rojo.")
    else:
        form = PaqueteEditarForm(instance=paquete)

    context = {
        'form': form,
        'titulo': f'Editar a {paquete.nombre}',
    }
    return render(request, 'paquetes/agregar_paquete.html', context)

#promociones
def crear_promocion(request):
    if request.method == 'POST':
        form = PromocionForm(request.POST)
        if form.is_valid():
            promocion = form.save()
            messages.success(request, f"Promoción '{promocion.nombre}' creada correctamente.")
            return redirect('promociones:inicio_promocion')
        else:
            messages.error(request, "Error al crear la promoción. Por favor verifica los datos.")
    else:
        form = PromocionForm()

    context = {
        'form': form,
        'titulo': 'Crear Nueva Promoción',
    }
    return render(request, 'promociones/agregar_promocion.html', context)

def editar_promocion(request, pk):
    promocion = get_object_or_404(Promocion, pk=pk)

    if request.method == 'POST':
        form = PromocionEditarForm(request.POST, instance=promocion)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {promocion.nombre} actualizados correctamente.")
            return redirect('promociones:inicio_promocion')
        else:
            messages.error(request, "Error al actualizar. Revisa los campos marcados en rojo.")
    else:
        form = PromocionEditarForm(instance=promocion)

    context = {
        'form': form,
        'titulo': f'Editar a {promocion.nombre}',
    }
    return render(request, 'promociones/agregar_promocion.html', context)
#reservas
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            messages.success(request, f"Reserva para '{reserva.nombre}' creada correctamente.")
            return redirect('reservas:inicio_reserva')
        else:
            messages.error(request, "Error al crear la reserva. Por favor verifica los datos.")
    else:
        form = ReservaForm()

    context = {
        'form': form,
        'titulo': 'Crear Nueva Reserva',
    }
    return render(request, 'reservas/agregar_reserva.html', context)

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        form = ReservaEditarForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {reserva.nombre} actualizados correctamente.")
            return redirect('reservas:inicio_reserva')
        else:
            messages.error(request, "Error al actualizar. Revisa los campos marcados en rojo.")
    else:
        form = ReservaEditarForm(instance=reserva)

    context = {
        'form': form,
        'titulo': f'Editar a {reserva.nombre}',
    }
    return render(request, 'reservas/agregar_reserva.html', context)
