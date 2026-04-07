from django.db import models
from django.conf import settings
# Esta es la línea que faltaba:
from django.contrib.auth.models import User 

class Tour(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Tour")
    destino = models.CharField(max_length=150, default="Sogamoso, Boyacá", verbose_name="Lugar de Destino")
    duracion_dias = models.PositiveIntegerField(default=1, verbose_name="Duración (Días)")
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio Base")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del recorrido")

    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    def __str__(self):
        return f"{self.nombre} - {self.destino}"


class Reserva(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente de Pago'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    )

    # Ahora 'User' ya funcionará porque lo importamos arriba
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservas")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reservas")
    
    fecha_reserva = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Reserva")
    cantidad_personas = models.PositiveIntegerField(default=1, verbose_name="Número de Personas")
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Pagado")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva de {self.usuario.username} - {self.tour.nombre}"