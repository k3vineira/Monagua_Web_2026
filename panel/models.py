from django.db import models
from django.conf import settings

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

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reservas")
    fecha_reserva = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Reserva")
    cantidad_personas = models.PositiveIntegerField(default=1, verbose_name="Número de Personas")
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Pagado")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"Reserva de {self.usuario} - {self.tour.nombre}"


class Guia(models.Model):
    ESPECIALIDADES = (
        ('Alta Montaña', 'Alta Montaña'),
        ('Flora y Fauna', 'Flora y Fauna'),
        ('Cultura Local', 'Cultura Local'),
        ('Turismo de Aventura', 'Turismo de Aventura'),
        ('Avifauna', 'Avifauna'),
        ('Historia y Patrimonio', 'Historia y Patrimonio'),
    )

    DISPONIBILIDADES = (
        ('Disponible', 'Disponible'),
        ('Ocupado', 'Ocupado'),
    )

    ESTADOS = (
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    )

    COLORES_AVATAR = [
        '#2c6e3c', '#3b82f6', '#f59e0b', '#8b5cf6',
        '#ec4899', '#06b6d4', '#10b981', '#f97316',
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    documento = models.CharField(max_length=30, blank=True, null=True, verbose_name="Número de Documento")
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDADES, verbose_name="Especialidad")
    disponibilidad = models.CharField(max_length=20, choices=DISPONIBILIDADES, default='Disponible', verbose_name="Disponibilidad")
    experiencia = models.PositiveIntegerField(default=0, verbose_name="Años de Experiencia")
    idiomas = models.CharField(max_length=200, blank=True, null=True, verbose_name="Idiomas")
    certificaciones = models.TextField(blank=True, null=True, verbose_name="Certificaciones")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas Adicionales")
    estado = models.CharField(max_length=10, choices=ESTADOS, default='Activo', verbose_name="Estado")
    color_avatar = models.CharField(max_length=10, default='#2c6e3c', verbose_name="Color Avatar")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Guía"
        verbose_name_plural = "Guías"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad}"

    def num_tours(self):
        # Cuando tengas una relación Tour → Guia, ajusta el related_name aquí
        return 0