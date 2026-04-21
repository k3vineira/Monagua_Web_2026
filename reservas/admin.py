from django.contrib import admin

# Importamos los modelos que creamos en models.py
from .models import Categoria, Actividades, Paquete, Reserva, Promocion , PQRS, Blog


# Los registramos para que Django los muestre en el panel azul
admin.site.register(Categoria)
admin.site.register(Actividades)
admin.site.register(Paquete)
admin.site.register(Reserva)
admin.site.register(Promocion)  
admin.site.register(PQRS)
admin.site.register(Blog)