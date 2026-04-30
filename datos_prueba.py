import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Importar tus modelos (ajusta 'reservas' al nombre real de tu app si es diferente)
from reservas.models import Categoria, Actividades, Paquete

print("Iniciando carga de datos de prueba para Monagua...")

# 1. Crear 5 CATEGORÍAS
cat_datos = [
    {'nombre': 'Ecoturismo', 'descripcion': 'Actividades en contacto con la naturaleza.', 'tipo': 'Naturaleza'},
    {'nombre': 'Cultura', 'descripcion': 'Recorridos históricos y tradiciones locales.', 'tipo': 'Histórico'},
    {'nombre': 'Aventura', 'descripcion': 'Deportes extremos y retos físicos.', 'tipo': 'Deporte'},
    {'nombre': 'Gastronomía', 'descripcion': 'Experiencias culinarias típicas de Mongua.', 'tipo': 'Alimentación'},
    {'nombre': 'Relajación', 'descripcion': 'Espacios para el descanso y bienestar.', 'tipo': 'Bienestar'},
]

for data in cat_datos:
    Categoria.objects.get_or_create(nombre=data['nombre'], defaults=data)

print("- Categorías creadas.")

# 2. Crear 5 ACTIVIDADES (Relacionadas a categorías)
cat_eco = Categoria.objects.get(nombre='Ecoturismo')
cat_cul = Categoria.objects.get(nombre='Cultura')

act_datos = [
    {'nombre': 'Senderismo Páramo de Ocetá', 'descripcion': 'Caminata guiada por el páramo más lindo.', 'duracion': '6 horas', 'nivel_dificultad': 'Alta', 'categoria': cat_eco},
    {'nombre': 'Visita Laguna Negra', 'descripcion': 'Recorrido fotográfico y místico.', 'duracion': '4 horas', 'nivel_dificultad': 'Media', 'categoria': cat_eco},
    {'nombre': 'Taller de Amasijos', 'descripcion': 'Aprende a hacer pan tradicional.', 'duracion': '2 horas', 'nivel_dificultad': 'Baja', 'categoria': cat_cul},
    {'nombre': 'Ruta de las Piedras Caladas', 'descripcion': 'Exploración de formaciones rocosas.', 'duracion': '3 horas', 'nivel_dificultad': 'Media', 'categoria': cat_eco},
    {'nombre': 'Tour Histórico Mongua', 'descripcion': 'Conoce la iglesia y la plaza principal.', 'duracion': '2 horas', 'nivel_dificultad': 'Baja', 'categoria': cat_cul},
]

for data in act_datos:
    Actividades.objects.get_or_create(nombre=data['nombre'], defaults=data)

print("- Actividades creadas.")

# 3. Crear 5 PAQUETES (Relacionando actividades)
acts = Actividades.objects.all()

paquete_datos = [
    {'nombre': 'Aventura Total Ocetá', 'descripcion': 'El paquete más completo para aventureros.', 'precio': 150000},
    {'nombre': 'Mongua Tradicional', 'descripcion': 'Cultura y sabor en un solo día.', 'precio': 85000},
    {'nombre': 'Escape Natural', 'descripcion': 'Lagunas y aire puro.', 'precio': 110000},
    {'nombre': 'Fin de Semana Místico', 'descripcion': 'Páramo, laguna y descanso.', 'precio': 220000},
    {'nombre': 'Expedición Fotográfica', 'descripcion': 'Captura los mejores paisajes de Boyacá.', 'precio': 95000},
]

for i, data in enumerate(paquete_datos):
    paquete, created = Paquete.objects.get_or_create(nombre=data['nombre'], defaults=data)
    if created:
        # Asignar algunas actividades al azar o por índice para el ManyToMany
        paquete.actividades.add(acts[i % len(acts)])
        if i % 2 == 0: # Agregar una segunda actividad a algunos paquetes
            paquete.actividades.add(acts[(i+1) % len(acts)])

print("- Paquetes creados exitosamente.")
print("Proceso finalizado.")