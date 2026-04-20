from django.db import models
from django.conf import settings
from reservas.models import Paquete 

class Resena(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='comentarios')
    
    contenido = models.TextField(max_length=500)
    estrellas = models.PositiveIntegerField(default=5) # 1 a 5
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} en {self.paquete.nombre}"