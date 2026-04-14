from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Actividades, Categoria, Paquete, Promocion, Reserva, PQRS, Blog
from .forms import (
    CategoriaForm, CategoriaEditarForm, 
    ActividadesForm, ActividadesEditarForm, 
    PaqueteForm, PaqueteEditarForm, 
    PromocionForm, PromocionEditarForm, 
    ReservaForm, ReservaEditarForm,
    PQRSForm, PQRSEditarForm,
    blogForm, blogEditarForm

)

# --- VISTAS GENERALES ---

def blog_view(request):
    """ Muestra la página principal del blog con las entradas de la BD """
    # Buscamos todos los objetos guardados en el modelo Blog
    posts = Blog.objects.all().order_by('-id') 
    
    # IMPORTANTE: El nombre en el diccionario ('posts') debe ser igual al del for
    return render(request, 'blog.html', {'posts': posts})

def promociones_view(request):
    """ Muestra la página de promociones """
    promociones_list = Promocion.objects.all()
    return render(request, 'promociones.html', {'promociones': promociones_list})

def destinos(request):
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
    return render(request, 'admin/paquetes/agregar_paquete.html', {'form': form, 'titulo': 'Crear Nuevo Paquete'})

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
    return render(request, 'admin/paquetes/agregar_paquete.html', {'form': form, 'titulo': f'Editar {paquete.nombre}'})

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
    return render(request, 'admin/categorias/agregar_categoria.html', {'form': form, 'titulo': 'Crear Categoría'})

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
    return render(request, 'admin/categorias/agregar_categoria.html', {'form': form, 'titulo': f'Editar {categoria.nombre}'})

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
    return render(request, 'admin/actividades/agregar_actividad.html', {'form': form, 'titulo': 'Crear Actividad'})

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
    return render(request, 'admin/actividades/agregar_actividad.html', {'form': form, 'titulo': f'Editar {actividad.nombre}'})

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
    return render(request, 'admin/reservas/agregar_reserva.html', {'form': form, 'titulo': 'Crear Reserva'})

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
    return render(request, 'admin/reservas/agregar_reserva.html', {'form': form, 'titulo': f'Editar Reserva'})
# --- PROMOCIONES ---
def crear_promocion(request):
    if request.method == 'POST':
        # Importante: si usas imágenes en las promociones, agrega request.FILES
        form = PromocionForm(request.POST, request.FILES) 
        if form.is_valid():
            promocion = form.save()
            messages.success(request, f"Promoción '{promocion.nombre}' creada correctamente.")
            return redirect('crear_promocion')
    else:
        form = PromocionForm()

    # Traemos todas las promociones de la base de datos para el carrusel
    todas_las_promociones = Promocion.objects.all() 

    # Renderizamos una sola vez con todos los datos necesarios
    return render(request, 'admin/promociones/agregar_promocion.html', {
        'form': form, 
        'titulo': 'Crear Promoción',
        'promociones': todas_las_promociones
    })

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
    return render(request, 'admin/promociones/agregar_promocion.html', {'form': form, 'titulo': f'Editar {promocion.nombre}'})

def crear_pqrs(request):
    """ Vista para mostrar el formulario de PQRS """
    if request.method == 'POST':
        form = PQRSForm(request.POST)
        if form.is_valid():
            pqrs = form.save()
            messages.success(request, f"PQRS '{pqrs.nombre}' enviada.")
            return redirect('pqrs')
    else:
        form = PQRSForm()
    return render(request, 'pqrs.html', {'form': form, 'titulo': 'Contáctanos - PQRS'})

def editar_pqrs(request, pk):
    pqrs = get_object_or_404(PQRS, pk=pk)
    if request.method == 'POST':
        form = PQRSEditarForm(request.POST, instance=pqrs)
        if form.is_valid():
            form.save()
            messages.success(request, f"PQRS de {pqrs.nombre} actualizada.")
            return redirect('pqrs')
    else:
        form = PQRSEditarForm(instance=pqrs)
    return render(request, 'pqrs.html', {'form': form, 'titulo': f'Editar PQRS de {pqrs.nombre}'})
def crear_blog(request):
    if request.method == 'POST':
        form = blogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            messages.success(request, f"Entrada '{blog.titulo}' publicada con éxito.")
            return redirect('crear_blog') # Redirige a la lista del blog
    else:
        form = blogForm()
    
    return render(request, 'admin/blog/agregar_blog.html', {
        'form': form, 
        'titulo': 'Nueva Entrada de Blog'
    })

def editar_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = blogEditarForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, f"Entrada '{blog.titulo}' actualizada.")
            return redirect('blog_view')
    else:
        form = blogEditarForm(instance=blog)
    
    return render(request, 'admin/blog/agregar_blog.html', {
        'form': form, 
        'titulo': f'Editando: {blog.titulo}'
    })
    
    #--lista de entradas para el admin--
def lista_blog(request):
    # Traemos todo de la base de datos
    blogs = Blog.objects.all() 
    return render(request, 'admin/blog/blog.html', {'blogs': blogs})

def lista_actividades(request):
    # Traemos todo de la base de datos
    actividades = Actividades.objects.all() 
    return render(request, 'admin/actividades/actividades.html', {'actividades': actividades})

def lista_categorias(request):
    # Traemos todo de la base de datos
    categorias = Categoria.objects.all() 
    return render(request, 'admin/categorias/categorias.html', {'categorias': categorias})

def lista_paquetes(request):
    # Traemos todo de la base de datos
    paquetes = Paquete.objects.all() 
    return render(request, 'admin/paquetes/paquetes.html', {'paquetes': paquetes})

def lista_promociones(request):
    # Traemos todo de la base de datos
    promociones = Promocion.objects.all() 
    return render(request, 'admin/promociones/promociones.html', {'promociones': promociones})

def lista_reservas(request):
    # Traemos todo de la base de datos
    reservas = Reserva.objects.all() 
    return render(request, 'admin/reservas/reservas.html', {'reservas': reservas})




    