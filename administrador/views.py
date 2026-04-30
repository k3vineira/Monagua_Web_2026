# views.py administrador

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from reservas.models import Promocion
from reservas.forms import PromocionForm, PromocionEditarForm
from .models import Tour, Reserva, Guia
from .forms import GuiaForm
from .models import Paquete

User = get_user_model()


# ══════════════════════════════════════════════
#  DASHBOARD ADMINISTRADOR
# ══════════════════════════════════════════════
def dashboard_administrador(request):

    # Total usuarios registrados
    total_usuarios = User.objects.count()

    # Total ventas
    total_ventas = Reserva.objects.aggregate(
        t=Sum('total_pagado')
    )['t'] or 0.00

    # Total reservas
    total_reservas = Reserva.objects.count()

    # Total tours
    total_tours = Tour.objects.count()

    # Top 5 tours más populares
    tours_populares = Tour.objects.annotate(
        numero_reservas=Count('reservas')
    ).order_by('-numero_reservas')[:5]

    total_promociones = Promocion.objects.count()

    context = {
        'total_usuarios': total_usuarios,
        'total_ventas': total_ventas,
        'total_reservas': total_reservas,
        'total_tours': total_tours,
        'tours_populares': tours_populares,
        'total_promociones': total_promociones,
    }

    return render(request, 'index-admin.html', context)


# ══════════════════════════════════════════════
#  GESTIÓN DE GUÍAS — LISTA
# ══════════════════════════════════════════════
@login_required
def gestion_guias(request):
    # 1. Obtener los datos base desde los modelos
    guias = Guia.objects.all()
    paquetes = Paquete.objects.all()
    form = GuiaForm()

    # 2. Construir el contexto con los contadores y el formulario
    context = {
        'guias': guias,
        'paquetes': paquetes,
        'form': form,
        'total_guias': guias.count(),
        'total_guias_activos': guias.filter(estado='Activo').count(),
        'total_guias_inactivos': guias.filter(estado='Inactivo').count(),
        
        # Este contador filtra los guías que ya tienen un paquete de Mongua asignado
        'guias_asignados': guias.exclude(paquete_asignado__isnull=True).count(),
    }

    # 3. Renderizar hacia el archivo que estás usando
    return render(request, 'index-guias.html', context)


# ══════════════════════════════════════════════
#  GUARDAR GUÍA (Crear o Editar)
# ══════════════════════════════════════════════
@login_required
def guias_guardar(request):

    print("--- INICIANDO PROCESO DE GUARDAR GUÍA ---")

    if request.method != 'POST':
        return redirect('gestion_usuarios')

    guia_id = request.POST.get('guia_id', '').strip()

    # Manejo seguro del número
    exp_str = request.POST.get('experiencia', '').strip()
    exp_val = int(exp_str) if exp_str.isdigit() else 0

    campos = {
        'nombre': request.POST.get('nombre', '').strip(),
        'apellido': request.POST.get('apellido', '').strip(),
        'correo': request.POST.get('correo', '').strip(),
        'telefono': request.POST.get('telefono', '').strip(),
        'documento': request.POST.get('documento', '').strip() or None,
        'especialidad': request.POST.get('especialidad', ''),
        'disponibilidad': request.POST.get('disponibilidad', 'Disponible'),
        'experiencia': exp_val,
        'idiomas': request.POST.get('idiomas', '').strip() or None,
        'certificaciones': request.POST.get('certificaciones', '').strip() or None,
        'notas': request.POST.get('notas', '').strip() or None,
    }

    print("DATOS CAPTURADOS:", campos)

    try:

        if guia_id:
            # ── EDITAR ──
            guia = get_object_or_404(Guia, pk=guia_id)

            if Guia.objects.exclude(pk=guia_id).filter(correo=campos['correo']).exists():
                return redirect(reverse('gestion_usuarios') + '?msg=error_correo')

            for attr, valor in campos.items():
                setattr(guia, attr, valor)

            guia.save()
            return redirect(reverse('gestion_usuarios') + '?msg=editado')

        else:
            # ── CREAR ──

            if Guia.objects.filter(correo=campos['correo']).exists():
                return redirect(reverse('gestion_usuarios') + '?msg=error_correo')

            colores = Guia.COLORES_AVATAR
            total = Guia.objects.count()

            campos['color_avatar'] = colores[total % len(colores)]

            Guia.objects.create(**campos)

            return redirect(reverse('gestion_usuarios') + '?msg=creado')

    except IntegrityError:
        return redirect(reverse('gestion_usuarios') + '?msg=error_bd')

    except Exception as e:
        print(f"Error detectado: {e}")
        return redirect(reverse('gestion_usuarios') + '?msg=error_bd')


# ══════════════════════════════════════════════
#  DAR DE BAJA
# ══════════════════════════════════════════════
@login_required
def guias_baja(request):

    if request.method == 'POST':

        guia = get_object_or_404(
            Guia,
            pk=request.POST.get('guia_id')
        )

        guia.estado = 'Inactivo'
        guia.disponibilidad = 'Ocupado'
        guia.save()

    return redirect(reverse('gestion_usuarios') + '?msg=baja')


# ══════════════════════════════════════════════
#  REACTIVAR GUÍA
# ══════════════════════════════════════════════
@login_required
def guias_reactivar(request):

    if request.method == 'POST':

        guia = get_object_or_404(
            Guia,
            pk=request.POST.get('guia_id')
        )

        guia.estado = 'Activo'
        guia.disponibilidad = 'Disponible'
        guia.save()

    return redirect(reverse('gestion_usuarios') + '?msg=reactivado')


# ══════════════════════════════════════════════
#  DETALLE DE GUÍA (JSON)
# ══════════════════════════════════════════════
@login_required
def guia_detalle_json(request, guia_id):

    guia = get_object_or_404(Guia, pk=guia_id)

    return JsonResponse({
        'id': guia.id,
        'nombre': guia.nombre,
        'apellido': guia.apellido,
        'correo': guia.correo,
        'telefono': guia.telefono,
        'documento': guia.documento or '',
        'especialidad': guia.especialidad,
        'disponibilidad': guia.disponibilidad,
        'experiencia': guia.experiencia,
        'idiomas': guia.idiomas or '',
        'certificaciones': guia.certificaciones or '',
        'notas': guia.notas or '',
        'estado': guia.estado,
    })


# ══════════════════════════════════════════════
#  GESTIÓN DE PROMOCIONES
#══════════════════════════════════════════════
@login_required
def gestion_promociones(request):

    promociones = Promocion.objects.all().order_by(
        'prioridad',
        '-id'
    )

    form = PromocionForm()

    return render(
        request,
        'promociones_gestion.html',
        {
            'promociones': promociones,
            'form': form
        }
    )


@login_required
def guardar_promocion(request):

    if request.method == 'POST':

        promocion_id = request.POST.get('promocion_id')

        try:

            if promocion_id:

                promocion = get_object_or_404(
                    Promocion,
                    pk=promocion_id
                )

                form = PromocionEditarForm(
                    request.POST,
                    request.FILES,
                    instance=promocion
                )

            else:

                form = PromocionForm(
                    request.POST,
                    request.FILES
                )

            if form.is_valid():

                form.save()
                return redirect('gestion_promociones')

            else:

                print("Errores del formulario:", form.errors)

        except Exception as e:

            print(f"Error al guardar promoción: {e}")

    return redirect('gestion_promociones')


@login_required
def eliminar_promocion(request, pk):

    promocion = get_object_or_404(
        Promocion,
        pk=pk
    )

    promocion.delete()

    return redirect('gestion_promociones')


# ══════════════════════════════════════════════
#  GESTIÓN DE COMENTARIOS
# ══════════════════════════════════════════════
@login_required
def gestion_comentarios(request):

    return render(
        request,
        'administrador',
        {'msg': 'Sección de comentarios en desarrollo'}
    )
    # ══════════════════════════════════════════════════════════════════
# VISTAS DE REPORTES DE GUÍAS
# Agrega estas funciones a tu archivo administrador/views.py
# ══════════════════════════════════════════════════════════════════

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Importa tus modelos según como los tengas definidos.
# Ajusta el nombre del modelo y los campos según tu models.py
# Ejemplo: from administrador.models import ReporteGuia, Guia, Tour
# from .models import ReporteGuia, Guia, Tour


# ── 1. Listado de reportes (index-reporte.html) ────────────────
@login_required
def gestion_reportes(request):
    """
    Muestra la página principal de reportes.
    Renderiza: index-reporte.html
    Extiende:  base-reporte.html
    """
    # Descomenta y ajusta cuando tengas el modelo ReporteGuia
    # reportes        = ReporteGuia.objects.select_related('guia', 'tour').order_by('-fecha_creacion')
    # guias_activos   = Guia.objects.filter(estado='Activo').order_by('nombre')
    # tours           = Tour.objects.filter(activo=True).order_by('nombre')
    # total_resueltos  = reportes.filter(estado='Resuelto').count()
    # total_pendientes = reportes.filter(estado='Pendiente').count()
    # total_en_proceso = reportes.filter(estado='En proceso').count()
    # total_reportes   = reportes.count()

    context = {
        # 'reportes':         reportes,
        # 'guias_activos':    guias_activos,
        # 'tours':            tours,
        # 'total_resueltos':  total_resueltos,
        # 'total_pendientes': total_pendientes,
        # 'total_en_proceso': total_en_proceso,
        # 'total_reportes':   total_reportes,

        # Valores por defecto mientras creas el modelo
        'reportes':         [],
        'guias_activos':    [],
        'tours':            [],
        'total_resueltos':  0,
        'total_pendientes': 0,
        'total_en_proceso': 0,
        'total_reportes':   0,
    }
    return render(request, 'index-reporte.html', context)


# ── 2. Guardar nuevo reporte (POST desde modal) ────────────────
@login_required
@require_POST
def reportes_guardar(request):
    """
    Recibe el formulario del modal 'Nuevo Reporte' y guarda en BD.
    Redirige a /administrador/reportes/?msg=creado  (éxito)
           o a /administrador/reportes/?msg=error_bd (error)
    """
    try:
        guia_id         = request.POST.get('guia_id')
        tipo            = request.POST.get('tipo')
        prioridad       = request.POST.get('prioridad', 'Media')
        descripcion     = request.POST.get('descripcion')
        acciones_tomadas= request.POST.get('acciones_tomadas', '')
        fecha_incidente = request.POST.get('fecha_incidente') or None
        tour_id         = request.POST.get('tour_id') or None

        # Descomenta cuando tengas el modelo:
        # ReporteGuia.objects.create(
        #     guia_id         = guia_id,
        #     tipo            = tipo,
        #     prioridad       = prioridad,
        #     descripcion     = descripcion,
        #     acciones_tomadas= acciones_tomadas,
        #     fecha_incidente = fecha_incidente,
        #     tour_id         = tour_id,
        #     estado          = 'Pendiente',
        # )

        return redirect('/administrador/reportes/?msg=creado')

    except Exception as e:
        print('Error al guardar reporte:', e)
        return redirect('/administrador/reportes/?msg=error_bd')


# ── 3. Detalle de reporte en JSON (para el modal de detalle) ───
@login_required
def reportes_detalle_json(request, pk):
    """
    Devuelve los datos de un reporte en formato JSON.
    Es llamado por el fetch() de JavaScript en index-reporte.html
    """
    # Descomenta cuando tengas el modelo:
    # reporte = get_object_or_404(ReporteGuia, pk=pk)
    # data = {
    #     'id':              reporte.id,
    #     'guia_nombre':     f'{reporte.guia.nombre} {reporte.guia.apellido}',
    #     'tipo':            reporte.tipo,
    #     'estado':          reporte.estado,
    #     'prioridad':       reporte.prioridad,
    #     'descripcion':     reporte.descripcion,
    #     'acciones_tomadas':reporte.acciones_tomadas or '',
    #     'tour_nombre':     reporte.tour.nombre if reporte.tour else '',
    #     'fecha_creacion':  reporte.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
    # }
    # return JsonResponse(data)

    # Respuesta de ejemplo mientras creas el modelo
    return JsonResponse({
        'id':               pk,
        'guia_nombre':      'Guía de ejemplo',
        'tipo':             'Comentario general',
        'estado':           'Pendiente',
        'prioridad':        'Media',
        'descripcion':      'Descripción de ejemplo.',
        'acciones_tomadas': '',
        'tour_nombre':      '',
        'fecha_creacion':   '01/01/2026 10:00',
    })


# ── 4. Marcar reporte como Resuelto ───────────────────────────
@login_required
@require_POST
def reportes_resolver(request):
    """
    Cambia el estado de un reporte a 'Resuelto'.
    Redirige a /administrador/reportes/?msg=resuelto
    """
    reporte_id = request.POST.get('reporte_id')
    try:
        # Descomenta cuando tengas el modelo:
        # reporte = get_object_or_404(ReporteGuia, pk=reporte_id)
        # reporte.estado = 'Resuelto'
        # reporte.save()
        return redirect('/administrador/reportes/?msg=resuelto')
    except Exception as e:
        print('Error al resolver reporte:', e)
        return redirect('/administrador/reportes/?msg=error_bd')


# ── 5. Eliminar reporte ────────────────────────────────────────
@login_required
@require_POST
def reportes_eliminar(request):
    """
    Elimina un reporte de la base de datos.
    Redirige a /administrador/reportes/?msg=eliminado
    """
    reporte_id = request.POST.get('reporte_id')
    try:
        # Descomenta cuando tengas el modelo:
        # reporte = get_object_or_404(ReporteGuia, pk=reporte_id)
        # reporte.delete()
        return redirect('/administrador/reportes/?msg=eliminado')
    except Exception as e:
        print('Error al eliminar reporte:', e)
        return redirect('/administrador/reportes/?msg=error_bd')