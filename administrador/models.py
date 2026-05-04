from django.db import models
from django.conf import settings
from reservas.models import Paquete

# ══════════════════════════════════════════════
#  GUÍA
# ══════════════════════════════════════════════
class Guia(models.Model):
    ESPECIALIDADES = (
        ('Alta Montaña',        'Alta Montaña'),
        ('Flora y Fauna',       'Flora y Fauna'),
        ('Cultura Local',       'Cultura Local'),
        ('Turismo de Aventura', 'Turismo de Aventura'),
        ('Avifauna',            'Avifauna'),
        ('Historia y Patrimonio', 'Historia y Patrimonio'),
    )

    DISPONIBILIDADES = (
        ('Disponible', 'Disponible'),
        ('Ocupado',    'Ocupado'),
    )

    ESTADOS = (
        ('Activo',   'Activo'),
        ('Inactivo', 'Inactivo'),
    )

    COLORES_AVATAR = [
        '#2c6e3c', '#3b82f6', '#f59e0b', '#8b5cf6',
        '#ec4899', '#06b6d4', '#10b981', '#f97316',
    ]

    nombre          = models.CharField(max_length=100, verbose_name="Nombre")
    apellido        = models.CharField(max_length=100, verbose_name="Apellido")
    correo          = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono        = models.CharField(max_length=20, verbose_name="Teléfono")
    documento       = models.CharField(max_length=30, blank=True, null=True, verbose_name="Número de Documento")
    especialidad    = models.CharField(max_length=50, choices=ESPECIALIDADES, verbose_name="Especialidad")
    disponibilidad  = models.CharField(max_length=20, choices=DISPONIBILIDADES, default='Disponible', verbose_name="Disponibilidad")
    experiencia     = models.PositiveIntegerField(default=0, verbose_name="Años de Experiencia")
    idiomas         = models.CharField(max_length=200, blank=True, null=True, verbose_name="Idiomas")
    certificaciones = models.TextField(blank=True, null=True, verbose_name="Certificaciones")
    notas           = models.TextField(blank=True, null=True, verbose_name="Notas Adicionales")
    estado          = models.CharField(max_length=10, choices=ESTADOS, default='Activo', verbose_name="Estado")
    color_avatar    = models.CharField(max_length=10, default='#2c6e3c', verbose_name="Color Avatar")
    fecha_registro  = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    paquete_asignado = models.ForeignKey(
        Paquete, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="guias_del_paquete",
        verbose_name="Asignar Paquete Turístico" 
    )
    class Meta:
        verbose_name = "Guía"
        verbose_name_plural = "Guías"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad}"