import os
import django
import sys

# 1. Configurar el entorno de Django
# Reemplaza 'monagua' por el nombre exacto de la carpeta donde está tu settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import call_command

def generar_json_utf8():
    try:
        # 2. Abrir el archivo forzando la codificación UTF-8
        with open('usuarios.json', 'w', encoding='utf-8') as f:
            # 3. Ejecutar el comando dumpdata redirigiendo la salida al archivo
            call_command('dumpdata', 'usuario.Usuario', indent=2, stdout=f)
        
        print("✅ ÉXITO: 'usuarios.json' creado correctamente con codificación UTF-8 pura.")
        print("Ahora puedes subirlo a GitHub para que Render lo reconozca.")
    except Exception as e:
        print(f"❌ ERROR: No se pudo generar el archivo. Detalle: {e}")

if __name__ == "__main__":
    generar_json_utf8()