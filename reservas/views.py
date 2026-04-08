from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Actividades, Categoria, Paquete, Promocion, Reserva
from .forms import (
    CategoriaForm, CategoriaEditarForm, 
    ActividadesForm, ActividadesEditarForm, 
    PaqueteForm, PaqueteEditarForm, 
    PromocionForm, PromocionEditarForm, 
    ReservaForm, ReservaEditarForm
)

# --- VISTAS GENERALES ---

def blog_view(request):
    """ Muestra la página del blog """
    return render(request, 'blog.html')

def destinos(request):
    """ 
    Función principal para mostrar los paquetes turísticos.
    Filtra por nombre (q) y por precio máximo.
    """
    destinos_list = Paquete.objects.all()

    # Captura de datos del buscador
    busqueda = request.GET.get('q', '').strip()
    precio_max = request.GET.get('precio_max')

    if busqueda:
        destinos_list = destinos_list.filter(nombre__icontains=busqueda)

    if precio_max:
        destinos_list = destinos_list.filter(precio__lte=precio_max)
    
    # Este diccionario {'destinos': destinos_list} es lo que lee el {% for %}
    return render(request, 'destinos.html', {'destinos': destinos_list})

def reservas_view(request):
    """ Detalle de un paquete para el formulario de reserva """
    paquete_id = request.GET.get('paquete_id') 
    paquete_seleccionado = None
    
    if paquete_id:
        paquete_seleccionado = get_object_or_404(Paquete, id=paquete_id)
    
    return render(request, 'reservas.html', {'paquete': paquete_seleccionado})

# --- CRUD DE PAQUETES (MONAGUA) ---

def crear_paquete(request):
    """ Crea un nuevo destino turístico """
    if request.method == 'POST':
        # Importante: request.FILES es necesario para las fotos de los destinos
        form = PaqueteForm(request.POST, request.FILES)
        if form.is_valid():
            paquete = form.save()
            messages.success(request, f"Paquete '{paquete.nombre}' creado correctamente.")
            return redirect('crear_paquete')
        else:
            messages.error(request, "Error al crear el paquete. Verifica los datos.")
    else:
        form = PaqueteForm()
    return render(request, 'paquetes/agregar_paquete.html', {'form': form, 'titulo': 'Crear Nuevo Paquete'})

def editar_paquete(request, pk):
    """ Edita un destino existente """
    paquete = get_object_or_404(Paquete, pk=pk)
    if request.method == 'POST':
        form = PaqueteEditarForm(request.POST, request.FILES, instance=paquete)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos de {paquete.nombre} actualizados.")
            return redirect('crear_paquete')
    else:
        form = PaqueteEditarForm(instance=paquete)
    return render(request, 'paquetes/agregar_paquete.html', {'form': form, 'titulo': f'Editar {paquete.nombre}'})

# --- CRUD DE CATEGORÍAS ---

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f"Categoría '{categoria.nombre}' creada.")
            return redirect('crear_categoria')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/agregar_categoria.html', {'form': form, 'titulo': 'Crear Categoría'})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaEditarForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoría {categoria.nombre} actualizada.")
            return redirect('crear_categoria')
    else:
        form = CategoriaEditarForm(instance=categoria)
    return render(request, 'categorias/agregar_categoria.html', {'form': form, 'titulo': f'Editar {categoria.nombre}'})

# --- CRUD DE ACTIVIDADES ---

def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadesForm(request.POST)
        if form.is_valid():
            actividad = form.save()
            messages.success(request, f"Actividad '{actividad.nombre}' creada.")
            return redirect('crear_actividad')
    else:
        form = ActividadesForm()
    return render(request, 'actividades/agregar_actividad.html', {'form': form, 'titulo': 'Crear Actividad'})

def editar_actividad(request, pk):
    actividad = get_object_or_404(Actividades, pk=pk)
    if request.method == 'POST':
        form = ActividadesEditarForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            messages.success(request, f"Actividad {actividad.nombre} actualizada.")
            return redirect('crear_actividad')
    else:
        form = ActividadesEditarForm(instance=actividad)
    return render(request, 'actividades/agregar_actividad.html', {'form': form, 'titulo': f'Editar {actividad.nombre}'})

# --- CRUD DE RESERVAS ---

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            messages.success(request, f"Reserva para '{reserva.nombre}' creada.")
            return redirect('crear_reserva')
    else:
        form = ReservaForm()
    return render(request, 'reservas/agregar_reserva.html', {'form': form, 'titulo': 'Crear Reserva'})

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaEditarForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, f"Reserva de {reserva.nombre} actualizada.")
            return redirect('crear_reserva')
    else:
        form = ReservaEditarForm(instance=reserva)
    return render(request, 'reservas/agregar_reserva.html', {'form': form, 'titulo': f'Editar Reserva'})
# --- PROMOCIONES ---
def crear_promocion(request):
    if request.method == 'POST':
        form = PromocionForm(request.POST)
        if form.is_valid():
            promocion = form.save()
            messages.success(request, f"Promoción '{promocion.nombre}' creada.")
            return redirect('crear_promocion')
    else:
        form = PromocionForm()
    return render(request, 'promociones/agregar_promocion.html', {'form': form, 'titulo': 'Crear Promoción'})

def editar_promocion(request, pk):
    promocion = get_object_or_404(Promocion, pk=pk)
    if request.method == 'POST':
        form = PromocionEditarForm(request.POST, instance=promocion)
        if form.is_valid():
            form.save()
            messages.success(request, f"Promoción {promocion.nombre} actualizada.")
            return redirect('crear_promocion')
    else:
        form = PromocionEditarForm(instance=promocion)
    return render(request, 'promociones/agregar_promocion.html', {'form': form, 'titulo': f'Editar {promocion.nombre}'})