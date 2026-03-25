from django.db import models
from django.contrib.auth.models import User

class Tour(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Asegúrate de que haya una coma aquí
    # ... otros campos (destino, duración, etc.)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)

# En la clase Reserva (Línea 16)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2) # Y otra coma aquí

    def __str__(self):
        return f"Reserva de {self.usuario.username} - {self.tour.nombre}"