"""
Script para generar datos de prueba (Seed Data)
Ejecutar con: python manage.py shell < datos_prueba.py
"""

import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# =====================
# USUARIOS
# =====================
from usuario.models import Usuario, PerfilTurista, PerfilGuia
from django.contrib.auth import get_user_model

User = get_user_model()

print("Creando usuarios...")

# Crear usuarios regulares
usuarios_data = [
    {'username': 'juanperez', 'first_name': 'Juan', 'last_name': 'Pérez', 'email': 'juan.perez@email.com', 'numero_documento': '12345678', 'telefono': '3001234567', 'residencia': 'Bogotá'},
    {'username': 'mariagonzalez', 'first_name': 'María', 'last_name': 'González', 'email': 'maria.gonzalez@email.com', 'numero_documento': '23456789', 'telefono': '3002345678', 'residencia': 'Medellín'},
    {'username': 'carlosruiz', 'first_name': 'Carlos', 'last_name': 'Ruiz', 'email': 'carlos.ruiz@email.com', 'numero_documento': '34567890', 'telefono': '3003456789', 'residencia': 'Cali'},
    {'username': 'anitalopez', 'first_name': 'Ana', 'last_name': 'López', 'email': 'ana.lopez@email.com', 'numero_documento': '45678901', 'telefono': '3004567890', 'residencia': 'Barranquilla'},
    {'username': 'pedromartinez', 'first_name': 'Pedro', 'last_name': 'Martínez', 'email': 'pedro.martinez@email.com', 'numero_documento': '56789012', 'telefono': '3005678901', 'residencia': 'Cartagena'},
    {'username': 'lauracastro', 'first_name': 'Laura', 'last_name': 'Castro', 'email': 'laura.castro@email.com', 'numero_documento': '67890123', 'telefono': '3006789012', 'residencia': 'Santa Marta'},
    {'username': 'jorgediaz', 'first_name': 'Jorge', 'last_name': 'Díaz', 'email': 'jorge.diaz@email.com', 'numero_documento': '78901234', 'telefono': '3007890123', 'residencia': 'Cusco'},
    {'username': 'sofiagomez', 'first_name': 'Sofía', 'last_name': 'Gómez', 'email': 'sofia.gomez@email.com', 'numero_documento': '89012345', 'telefono': '3008901234', 'residencia': 'Pereira'},
    {'username': 'miguelhernandez', 'first_name': 'Miguel', 'last_name': 'Hernández', 'email': 'miguel.hernandez@email.com', 'numero_documento': '90123456', 'telefono': '3009012345', 'residencia': 'Manizales'},
    {'username': 'camilaramirez', 'first_name': 'Camila', 'last_name': 'Ramírez', 'email': 'camila.ramirez@email.com', 'numero_documento': '01234567', 'telefono': '3000123456', 'residencia': 'Bucaramanga'},
]

usuarios_creados = []
for data in usuarios_data:
    usuario, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'numero_documento': data['numero_documento'],
            'telefono': data['telefono'],
            'residencia': data['residencia'],
            'es_turista': True,
            'is_staff': False,
        }
    )
    if created:
        usuario.set_password('password123')
        usuario.save()
        # Crear perfil de turista
        PerfilTurista.objects.get_or_create(
            usuario=usuario,
            defaults={
                'telefono': data['telefono'],
                'pais_origen': 'Colombia'
            }
        )
    usuarios_creados.append(usuario)

print(f"✓ {len(usuarios_creados)} usuarios creados")

# =====================
# GUIAS
# =====================
from administrador.models import Guia

print("Creando guías...")

guias_data = [
    {'nombre': 'Andrés', 'apellido': 'Camelo', 'correo': 'andres.camelo@monagua.com', 'telefono': '3101111111', 'documento': '11111111', 'especialidad': 'Alta Montaña'},
    {'nombre': 'Carmen', 'apellido': 'Sierra', 'correo': 'carmen.sierra@monagua.com', 'telefono': '3102222222', 'documento': '22222222', 'especialidad': 'Flora y Fauna'},
    {'nombre': 'Roberto', 'apellido': 'Mora', 'correo': 'roberto.mora@monagua.com', 'telefono': '3103333333', 'documento': '33333333', 'especialidad': 'Cultura Local'},
    {'nombre': 'Diana', 'apellido': 'Vega', 'correo': 'diana.vega@monagua.com', 'telefono': '3104444444', 'documento': '44444444', 'especialidad': 'Turismo de Aventura'},
    {'nombre': 'Fernando', 'apellido': 'Lara', 'correo': 'fernando.lara@monagua.com', 'telefono': '3105555555', 'documento': '55555555', 'especialidad': 'Avifauna'},
    {'nombre': 'Gloria', 'apellido': 'Reyes', 'correo': 'gloria.reyes@monagua.com', 'telefono': '3106666666', 'documento': '66666666', 'especialidad': 'Historia y Patrimonio'},
    {'nombre': 'Hugo', 'apellido': 'Navarro', 'correo': 'hugo.navarro@monagua.com', 'telefono': '3107777777', 'documento': '77777777', 'especialidad': 'Alta Montaña'},
    {'nombre': 'Irene', 'apellido': 'Ortega', 'correo': 'irene.ortega@monagua.com', 'telefono': '3108888888', 'documento': '88888888', 'especialidad': 'Flora y Fauna'},
    {'nombre': 'Javier', 'apellido': 'Paredes', 'correo': 'javier.paredes@monagua.com', 'telefono': '3109999999', 'documento': '99999999', 'especialidad': 'Cultura Local'},
    {'nombre': 'Karen', 'apellido': 'Quintana', 'correo': 'karen.quintana@monagua.com', 'telefono': '3100000000', 'documento': '00000000', 'especialidad': 'Turismo de Aventura'},
]

guias_creados = []
for data in guias_data:
    guia, created = Guia.objects.get_or_create(
        correo=data['correo'],
        defaults={
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'telefono': data['telefono'],
            'documento': data['documento'],
            'especialidad': data['especialidad'],
            'disponibilidad': 'Disponible',
            'estado': 'Activo',
        }
    )
    if created:
        # Crear usuario linked al guía
        usuario_guia, _ = User.objects.get_or_create(
            username=f"guia_{data['nombre'].lower()}",
            defaults={
                'first_name': data['nombre'],
                'last_name': data['apellido'],
                'email': data['correo'],
                'es_guia': True,
                'is_staff': False,
            }
        )
        if usuario_guia.password == '':
            usuario_guia.set_password('password123')
            usuario_guia.save()
        # Crear perfil de guía
        PerfilGuia.objects.get_or_create(
            usuario=usuario_guia,
            defaults={
                'licencia_turismo': f"LIC-{data['documento']}",
                'experiencia_años': 5,
                'biografia': f"Guía especializado en {data['especialidad']} con más de 5 años de experiencia en el sector turístico de Boyacá."
            }
        )
    guias_creados.append(guia)

print(f"✓ {len(guias_creados)} guías creados")

# =====================
# TOURS
# =====================
from administrador.models import Tour

print("Creando tours...")

tours_data = [
    {'nombre': 'Tour Laguna de Tota', 'destino': 'Aquitania, Boyacá', 'duracion_dias': 1, 'precio': 150000, 'descripcion': 'Visita a la laguna más grande de Colombia'},
    {'nombre': 'Ruta del Sol', 'destino': 'Villa de Leyva', 'duracion_dias': 2, 'precio': 350000, 'descripcion': 'Recorrido por el pueblo patrimonio de Colombia'},
    {'nombre': 'Aventura en el Cañón', 'destino': 'Cañón del Chicamocha', 'duracion_dias': 1, 'precio': 180000, 'descripcion': 'Experiencia de aventura en el cañón'},
    {'nombre': 'Cultura Muisca', 'destino': 'Sogamoso', 'duracion_dias': 1, 'precio': 120000, 'descripcion': 'Tour cultural por la historia muisca'},
    {'nombre': 'Avistamiento de Aves', 'destino': 'Páramo de Oceta', 'duracion_dias': 1, 'precio': 200000, 'descripcion': 'Observación de aves en el páramo'},
    {'nombre': 'Turismo de Montaña', 'destino': 'Sierra Nevada del Cocuy', 'duracion_dias': 3, 'precio': 550000, 'descripcion': 'Expedición a los picos más altos'},
    {'nombre': 'Experiencia Rural', 'destino': 'Tota, Boyacá', 'duracion_dias': 2, 'precio': 280000, 'descripcion': 'Inmersión en la vida rural boyacense'},
    {'nombre': 'Tour Histórico', 'destino': 'Tunja', 'duracion_dias': 1, 'precio': 100000, 'descripcion': 'Recorrido por la capital histórica'},
    {'nombre': 'Ecoturismo', 'destino': 'Páramo de Pisba', 'duracion_dias': 2, 'precio': 320000, 'descripcion': 'Exploración de ecosistemas de páramo'},
    {'nombre': 'Aventura Acuática', 'destino': 'Lago Sochagota', 'duracion_dias': 1, 'precio': 160000, 'descripcion': 'Actividades acuáticas en el lago'},
]

tours_creados = []
for i, data in enumerate(tours_data):
    tour, created = Tour.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'destino': data['destino'],
            'duracion_dias': data['duracion_dias'],
            'precio': Decimal(str(data['precio'])),
            'descripcion': data['descripcion'],
            'guia': guias_creados[i] if i < len(guias_creados) else None,
        }
    )
    tours_creados.append(tour)

print(f"✓ {len(tours_creados)} tours creados")

# =====================
# RESERVAS (Administrador)
# =====================
from administrador.models import Reserva as ReservaAdmin

print("Creando reservas (admin)...")

reservas_admin_data = [
    {'usuario': usuarios_creados[0], 'tour': tours_creados[0], 'cantidad_personas': 2, 'total_pagado': Decimal('300000'), 'estado': 'CONFIRMADA'},
    {'usuario': usuarios_creados[1], 'tour': tours_creados[1], 'cantidad_personas': 4, 'total_pagado': Decimal('1400000'), 'estado': 'CONFIRMADA'},
    {'usuario': usuarios_creados[2], 'tour': tours_creados[2], 'cantidad_personas': 1, 'total_pagado': Decimal('180000'), 'estado': 'PENDIENTE'},
    {'usuario': usuarios_creados[3], 'tour': tours_creados[3], 'cantidad_personas': 3, 'total_pagado': Decimal('360000'), 'estado': 'CONFIRMADA'},
    {'usuario': usuarios_creados[4], 'tour': tours_creados[4], 'cantidad_personas': 2, 'total_pagado': Decimal('400000'), 'estado': 'CANCELADA'},
    {'usuario': usuarios_creados[5], 'tour': tours_creados[5], 'cantidad_personas': 5, 'total_pagado': Decimal('2750000'), 'estado': 'CONFIRMADA'},
    {'usuario': usuarios_creados[6], 'tour': tours_creados[6], 'cantidad_personas': 2, 'total_pagado': Decimal('560000'), 'estado': 'PENDIENTE'},
    {'usuario': usuarios_creados[7], 'tour': tours_creados[7], 'cantidad_personas': 1, 'total_pagado': Decimal('100000'), 'estado': 'CONFIRMADA'},
    {'usuario': usuarios_creados[8], 'tour': tours_creados[8], 'cantidad_personas': 4, 'total_pagado': Decimal('1280000'), 'estado': 'CONFIRMADA'},
    {'usuario': usuarios_creados[9], 'tour': tours_creados[9], 'cantidad_personas': 2, 'total_pagado': Decimal('320000'), 'estado': 'PENDIENTE'},
]

for data in reservas_admin_data:
    ReservaAdmin.objects.get_or_create(
        usuario=data['usuario'],
        tour=data['tour'],
        cantidad_personas=data['cantidad_personas'],
        defaults={
            'total_pagado': data['total_pagado'],
            'estado': data['estado'],
        }
    )

print("✓ 10 reservas (admin) creadas")

# =====================
# CATEGORÍAS
# =====================
from reservas.models import Categoria

print("Creando categorías...")

categorias_data = [
    {'nombre': 'Aventura', 'descripcion': 'Actividades de adrenalina y riesgo controlado', 'tipo': 'Deportes'},
    {'nombre': 'Cultura', 'descripcion': 'Experiencias culturales e históricas', 'tipo': 'Turismo'},
    {'nombre': 'Naturaleza', 'descripcion': 'Observación de flora y fauna', 'tipo': 'Ecoturismo'},
    {'nombre': 'Gastronomía', 'descripcion': 'Experiencias culinarias locales', 'tipo': 'Turismo'},
    {'nombre': 'Relax', 'descripcion': 'Actividades para descansar y relajarse', 'tipo': 'Bienestar'},
    {'nombre': 'Deportes', 'descripcion': 'Actividades deportivas al aire libre', 'tipo': 'Deportes'},
    {'nombre': 'Educativo', 'descripcion': 'Aprendizaje y capacitación', 'tipo': 'Educación'},
    {'nombre': 'Festivo', 'descripcion': 'Eventos y festividades locales', 'tipo': 'Cultura'},
    {'nombre': 'Religioso', 'descripcion': 'Turismo religioso y espiritual', 'tipo': 'Cultura'},
    {'nombre': 'Rural', 'descripcion': 'Experiencias en entornos rurales', 'tipo': 'Ecoturismo'},
]

categorias_creadas = []
for data in categorias_data:
    cat, created = Categoria.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'descripcion': data['descripcion'],
            'tipo': data['tipo'],
        }
    )
    categorias_creadas.append(cat)

print(f"✓ {len(categorias_creadas)} categorías creadas")

# =====================
# ACTIVIDADES
# =====================
from reservas.models import Actividades

print("Creando actividades...")

actividades_data = [
    {'nombre': 'Senderismo', 'descripcion': 'Caminata por senderos naturales', 'duracion': '4 horas', 'nivel_dificultad': 'Media', 'categoria': categorias_creadas[0]},
    {'nombre': 'Rafting', 'descripcion': 'Navegación en río con rápidos', 'duracion': '3 horas', 'nivel_dificultad': 'Alta', 'categoria': categorias_creadas[0]},
    {'nombre': 'Tour Guiado', 'descripcion': 'Recorrido con guía local', 'duracion': '2 horas', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[1]},
    {'nombre': 'Observación de Aves', 'descripcion': 'Avistamiento de especies locales', 'duracion': '5 horas', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[2]},
    {'nombre': 'Cata de Quesos', 'descripcion': 'Degustación de productos lácteos locales', 'duracion': '2 horas', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[3]},
    {'nombre': 'Baño Termal', 'descripcion': 'Relax en aguas termales', 'duracion': '3 horas', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[4]},
    {'nombre': 'Ciclismo', 'descripcion': 'Ruta en bicicleta por el campo', 'duracion': '4 horas', 'nivel_dificultad': 'Media', 'categoria': categorias_creadas[5]},
    {'nombre': 'Taller de Artesanía', 'descripcion': 'Aprende técnicas artesanales', 'duracion': '3 horas', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[6]},
    {'nombre': 'Festival Local', 'descripcion': 'Participa en festividades tradicionales', 'duracion': '1 día', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[7]},
    {'nombre': 'Visita a Iglesia', 'descripcion': 'Recorrido por iglesias históricas', 'duracion': '2 horas', 'nivel_dificultad': 'Baja', 'categoria': categorias_creadas[8]},
]

actividades_creadas = []
for data in actividades_data:
    act, created = Actividades.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'descripcion': data['descripcion'],
            'duracion': data['duracion'],
            'nivel_dificultad': data['nivel_dificultad'],
            'categoria': data['categoria'],
        }
    )
    actividades_creadas.append(act)

print(f"✓ {len(actividades_creadas)} actividades creadas")

# =====================
# PAQUETES
# =====================
from reservas.models import Paquete

print("Creando paquetes...")

paquetes_data = [
    {'nombre': 'Aventura Total', 'descripcion': 'Paquete completo de aventura con múltiples actividades', 'precio': 450000},
    {'nombre': 'Escapada Romántica', 'descripcion': 'Fin de semana en pareja con actividades relax', 'precio': 380000},
    {'nombre': 'Exploración Cultural', 'descripcion': 'Inmersión en la cultura local boyacense', 'precio': 320000},
    {'nombre': 'Ecoturismo Extremo', 'descripcion': 'Para amantes de la naturaleza y aventura', 'precio': 520000},
    {'nombre': 'Familia Diversión', 'descripcion': 'Actividades para toda la familia', 'precio': 280000},
    {'nombre': 'Wellness Retreat', 'descripcion': 'Relax y bienestar en entornos naturales', 'precio': 350000},
    {'nombre': 'Aventura Acuática', 'descripcion': 'Actividades acuáticas emocionantes', 'precio': 400000},
    {'nombre': 'Tour Gastronómico', 'descripcion': 'Experiencia culinaria auténtica', 'precio': 250000},
    {'nombre': 'Aventura Rural', 'descripcion': 'Vive como un本地 en el campo', 'precio': 220000},
    {'nombre': 'Expedición de Montaña', 'descripcion': 'Para los más aventureros', 'precio': 600000},
]

paquetes_creados = []
for i, data in enumerate(paquetes_data):
    paquete, created = Paquete.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'descripcion': data['descripcion'],
            'precio': data['precio'],
        }
    )
    if created:
        # Agregar actividades al paquete
        for j in range(min(3, len(actividades_creadas))):
            paquete.actividades.add(actividades_creadas[(i + j) % len(actividades_creadas)])
    paquetes_creados.append(paquete)

print(f"✓ {len(paquetes_creados)} paquetes creados")

# =====================
# RESERVAS (Reservas app)
# =====================
from reservas.models import Reserva

print("Creando reservas...")

reservas_data = [
    {'usuario': usuarios_creados[0], 'paquete': paquetes_creados[0], 'fecha': date.today() + timedelta(days=5), 'numero_personas': 2},
    {'usuario': usuarios_creados[1], 'paquete': paquetes_creados[1], 'fecha': date.today() + timedelta(days=10), 'numero_personas': 2},
    {'usuario': usuarios_creados[2], 'paquete': paquetes_creados[2], 'fecha': date.today() + timedelta(days=7), 'numero_personas': 4},
    {'usuario': usuarios_creados[3], 'paquete': paquetes_creados[3], 'fecha': date.today() + timedelta(days=15), 'numero_personas': 3},
    {'usuario': usuarios_creados[4], 'paquete': paquetes_creados[4], 'fecha': date.today() + timedelta(days=3), 'numero_personas': 5},
    {'usuario': usuarios_creados[5], 'paquete': paquetes_creados[5], 'fecha': date.today() + timedelta(days=20), 'numero_personas': 2},
    {'usuario': usuarios_creados[6], 'paquete': paquetes_creados[6], 'fecha': date.today() + timedelta(days=8), 'numero_personas': 4},
    {'usuario': usuarios_creados[7], 'paquete': paquetes_creados[7], 'fecha': date.today() + timedelta(days=12), 'numero_personas': 2},
    {'usuario': usuarios_creados[8], 'paquete': paquetes_creados[8], 'fecha': date.today() + timedelta(days=6), 'numero_personas': 3},
    {'usuario': usuarios_creados[9], 'paquete': paquetes_creados[9], 'fecha': date.today() + timedelta(days=25), 'numero_personas': 2},
]

for data in reservas_data:
    Reserva.objects.get_or_create(
        usuario=data['usuario'],
        paquete=data['paquete'],
        fecha=data['fecha'],
        numero_personas=data['numero_personas'],
    )

print("✓ 10 reservas creadas")

# =====================
# PROMOCIONES
# =====================
from reservas.models import Promocion

print("Creando promociones...")

promociones_data = [
    {'nombre': 'Descuento de Temporada', 'descripcion': '20% de descuento en tours de aventura', 'porcentaje_descuento': 20, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=30), 'paquete': paquetes_creados[0], 'prioridad': 1, 'activo': True},
    {'nombre': 'Promo Parejas', 'descripcion': '30% para parejas en escape romántico', 'porcentaje_descuento': 30, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=14), 'paquete': paquetes_creados[1], 'prioridad': 2, 'activo': True},
    {'nombre': 'Niños Gratis', 'descripcion': 'Niños menores de 10 años no pagan', 'porcentaje_descuento': 100, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=60), 'paquete': paquetes_creados[4], 'prioridad': 3, 'activo': True},
    {'nombre': 'Early Bird', 'descripcion': '15% de descuento por reserva anticipada', 'porcentaje_descuento': 15, 'fecha_inicio': date.today() - timedelta(days=5), 'fecha_fin': date.today() + timedelta(days=90), 'paquete': paquetes_creados[2], 'prioridad': 4, 'activo': True},
    {'nombre': 'Black Friday', 'descripcion': 'Gran descuento en ecoturismo', 'porcentaje_descuento': 40, 'fecha_inicio': date.today() - timedelta(days=10), 'fecha_fin': date.today() + timedelta(days=5), 'paquete': paquetes_creados[3], 'prioridad': 5, 'activo': False},
    {'nombre': 'Descuento Grupal', 'descripcion': '25% para grupos de más de 5 personas', 'porcentaje_descuento': 25, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=45), 'paquete': paquetes_creados[5], 'prioridad': 6, 'activo': True},
    {'nombre': 'Semana Santa', 'descripcion': 'Ofertas especiales para Semana Santa', 'porcentaje_descuento': 35, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=20), 'paquete': paquetes_creados[6], 'prioridad': 7, 'activo': True},
    {'nombre': 'Turista Local', 'descripcion': '10% para residentes de Boyacá', 'porcentaje_descuento': 10, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=180), 'paquete': paquetes_creados[7], 'prioridad': 8, 'activo': True},
    {'nombre': 'Bienvenida', 'descripcion': '15% de descuento para nuevos usuarios', 'porcentaje_descuento': 15, 'fecha_inicio': date.today(), 'fecha_fin': None, 'paquete': paquetes_creados[8], 'prioridad': 9, 'activo': True},
    {'nombre': 'VIP', 'descripcion': '20% para usuarios frecuentes', 'porcentaje_descuento': 20, 'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=365), 'paquete': paquetes_creados[9], 'prioridad': 10, 'activo': True},
]

for data in promociones_data:
    Promocion.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'descripcion': data['descripcion'],
            'porcentaje_descuento': data['porcentaje_descuento'],
            'fecha_inicio': data['fecha_inicio'],
            'fecha_fin': data['fecha_fin'],
            'paquete': data['paquete'],
            'prioridad': data['prioridad'],
            'activo': data['activo'],
        }
    )

print("✓ 10 promociones creadas")

# =====================
# PQRS
# =====================
from reservas.models import PQRS

print("Creando PQRS...")

pqrs_data = [
    {'nombre_solicitante': 'Juan Pérez', 'documento': '12345678', 'email': 'juan.perez@email.com', 'tipo': 'Peticion', 'asunto': 'Información sobre tours', 'descripcion': 'Quisiera más información sobre los tours de aventura'},
    {'nombre_solicitante': 'María González', 'documento': '23456789', 'email': 'maria.gonzalez@email.com', 'tipo': 'Queja', 'asunto': 'Mal servicio en tour', 'descripcion': 'El guía no llegó a tiempo al punto de encuentro'},
    {'nombre_solicitante': 'Carlos Ruiz', 'documento': '34567890', 'email': 'carlos.ruiz@email.com', 'tipo': 'Reclamo', 'asunto': 'Tour diferente al publicado', 'descripcion': 'El tour no era como se mostraba en la página'},
    {'nombre_solicitante': 'Ana López', 'documento': '45678901', 'email': 'ana.lopez@email.com', 'tipo': 'Sugerencia', 'asunto': 'Más opciones vegetarianas', 'descripcion': 'Sugiero incluir opciones de comida vegetariana'},
    {'nombre_solicitante': 'Pedro Martínez', 'documento': '56789012', 'email': 'pedro.martinez@email.com', 'tipo': 'Peticion', 'asunto': 'Reserva grupal', 'descripcion': 'Necesito información para reserva de 20 personas'},
    {'nombre_solicitante': 'Laura Castro', 'documento': '67890123', 'email': 'laura.castro@email.com', 'tipo': 'Queja', 'asunto': 'Problema con pago', 'descripcion': 'El pago no se procesó correctamente'},
    {'nombre_solicitante': 'Jorge Díaz', 'documento': '78901234', 'email': 'jorge.diaz@email.com', 'tipo': 'Reclamo', 'asunto': 'Objeto perdido', 'descripcion': 'Dejé una chaqueta en el bus del tour'},
    {'nombre_solicitante': 'Sofía Gómez', 'documento': '89012345', 'email': 'sofia.gomez@email.com', 'tipo': 'Sugerencia', 'asunto': 'Mejorar horarios', 'descripcion': 'Sugiero ampliar horarios de tours los fines de semana'},
    {'nombre_solicitante': 'Miguel Hernández', 'documento': '90123456', 'email': 'miguel.hernandez@email.com', 'tipo': 'Peticion', 'asunto': 'Certificado de asistencia', 'descripcion': 'Necesito certificado de asistencia al tour'},
    {'nombre_solicitante': 'Camila Ramírez', 'documento': '01234567', 'email': 'camila.ramirez@email.com', 'tipo': 'Queja', 'asunto': 'Mal trato', 'descripcion': 'El personal de atención fue descortés'},
]

for data in pqrs_data:
    PQRS.objects.get_or_create(
        nombre_solicitante=data['nombre_solicitante'],
        documento=data['documento'],
        defaults={
            'email': data['email'],
            'tipo': data['tipo'],
            'asunto': data['asunto'],
            'descripcion': data['descripcion'],
        }
    )

print("✓ 10 PQRS creados")

# =====================
# BLOGS
# =====================
from reservas.models import Blog

print("Creando blogs...")

blogs_data = [
    {'titulo': '10 Lugares Imperdibles en Boyacá', 'contenido': 'Boyacá es un departamento lleno de historia, naturaleza y cultura. En este artículo te mostramos los 10 lugares que no puedes perderte en tu próxima visita.'},
    {'titulo': 'Guía para Principiantes en Senderismo', 'contenido': '¿Planeas hacer senderismo por primera vez? Esta guía te ayudará a prepararte adecuadamente para tu aventura en la montaña.'},
    {'titulo': 'Historia de los Muiscas', 'contenido': 'Los Muiscas fueron una de las civilizaciones más importantes de Colombia. Descubre su historia, tradiciones y legado cultural.'},
    {'titulo': 'Mejor Época para Visitar el Páramo', 'contenido': 'El páramo de Oceta es uno de los ecosistemas más únicos del mundo. Aprende cuándo es la mejor época para visitarlo.'},
    {'titulo': 'Gastronomía Boyacense: Platos Típicos', 'contenido': 'La cocina boyacense es rica y variada. Descubre los platos típicos que debes probar durante tu visita.'},
    {'titulo': 'Cómo Prepararte para el Rafting', 'contenido': 'El rafting es una actividad emocionante pero requiere preparación. Sigue estos consejos para una experiencia segura.'},
    {'titulo': 'Avistamiento de Aves en Colombia', 'contenido': 'Colombia es el país con más especies de aves del mundo. Aprende dónde y cómo observar estas maravillas naturales.'},
    {'titulo': 'Turismo Sostenible en Boyacá', 'contenido': 'El turismo sostenible es fundamental para preservar nuestros recursos. Descubre cómo viajar de manera responsable.'},
    {'titulo': 'Leyendas y Mitos de la Sierra', 'contenido': 'La Sierra Nevada del Cocuy está llena de leyendas神秘的. Comparte estas historias fascinantes de la región.'},
    {'titulo': 'Consejos para Fotografía de Paisajes', 'contenido': 'Los paisajes de Boyacá son perfectos para la fotografía. Aprende técnicas para capturar imágenes impresionantes.'},
]

for data in blogs_data:
    Blog.objects.get_or_create(
        titulo=data['titulo'],
        defaults={
            'contenido': data['contenido'],
        }
    )

print("✓ 10 blogs creados")

# =====================
# RESEÑAS
# =====================
from Experiencia_soporte.models import Resena

print("Creando reseñas...")

resenas_data = [
    {'usuario': usuarios_creados[0], 'paquete': paquetes_creados[0], 'contenido': 'Excelente experiencia, el guía muy profesional.', 'estrellas': 5},
    {'usuario': usuarios_creados[1], 'paquete': paquetes_creados[1], 'contenido': 'Muy romántico, la pareja disfrutó mucho.', 'estrellas': 5},
    {'usuario': usuarios_creados[2], 'paquete': paquetes_creados[2], 'contenido': 'Aprendí mucho sobre la cultura local.', 'estrellas': 4},
    {'usuario': usuarios_creados[3], 'paquete': paquetes_creados[3], 'contenido': 'Increíble naturaleza, muy recomendado.', 'estrellas': 5},
    {'usuario': usuarios_creados[4], 'paquete': paquetes_creados[4], 'contenido': 'Los niños lo pasaron genial.', 'estrellas': 4},
    {'usuario': usuarios_creados[5], 'paquete': paquetes_creados[5], 'contenido': 'Perfecto para descansar y relajarse.', 'estrellas': 5},
    {'usuario': usuarios_creados[6], 'paquete': paquetes_creados[6], 'contenido': 'Muy divertido, repetiría.', 'estrellas': 4},
    {'usuario': usuarios_creados[7], 'paquete': paquetes_creados[7], 'contenido': 'La comida deliciosa, muy auténtico.', 'estrellas': 5},
    {'usuario': usuarios_creados[8], 'paquete': paquetes_creados[8], 'contenido': 'Experiencia única en el campo.', 'estrellas': 5},
    {'usuario': usuarios_creados[9], 'paquete': paquetes_creados[9], 'contenido': 'Para verdaderos aventureros.', 'estrellas': 4},
]

for data in resenas_data:
    Resena.objects.get_or_create(
        usuario=data['usuario'],
        paquete=data['paquete'],
        defaults={
            'contenido': data['contenido'],
            'estrellas': data['estrellas'],
        }
    )

print("✓ 10 reseñas creadas")

# =====================
# PAGOS
# =====================
from pago.models import Pago

print("Creando pagos...")

# Nota: Pago requiere un campo 'comprobante' que es ImageField
# Para datos de prueba, necesitamos manejar esto de forma especial
# Por ahora crearemos registros sin imagen o saltaremos este paso

print("⚠️ Los pagos requieren imágenes de comprobantes - omitiendo en seed data")

print("\n" + "="*50)
print("✓ Seed Data completado exitosamente!")
print("="*50)
print(f"  - Usuarios: {len(usuarios_creados)}")
print(f"  - Guías: {len(guias_creados)}")
print(f"  - Tours: {len(tours_creados)}")
print(f"  - Reservas (admin): 10")
print(f"  - Categorías: {len(categorias_creadas)}")
print(f"  - Actividades: {len(actividades_creadas)}")
print(f"  - Paquetes: {len(paquetes_creados)}")
print(f"  - Reservas: 10")
print(f"  - Promociones: 10")
print(f"  - PQRS: 10")
print(f"  - Blogs: 10")
print(f"  - Reseñas: 10")
print("="*50)