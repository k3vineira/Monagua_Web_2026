from django.db import models

class Pago(models.Model):
    # Opciones para la verificación
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente de Verificación'),
        ('aprobado', 'Pago Válido'),
        ('rechazado', 'Pago Rechazado'),
    ]
    comprobante = models.ImageField(upload_to='comprobantes_pagos/', verbose_name='Imagen del Comprobante')
    nombre_cliente = models.CharField(max_length=100, verbose_name='Nombre del Cliente')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PAGO,default='pendiente',verbose_name='Estado de Verificación')

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago de {self.nombre_cliente} - {self.estado}"