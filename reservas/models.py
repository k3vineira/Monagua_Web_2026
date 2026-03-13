from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Categoría')
    descripcion = models.TextField(verbose_name='Descripción')
    tipo = models.CharField(max_length=50, verbose_name='Tipo de Categoría')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Actividades(models.Model):
    NIVEL_CHOICES = [
        ('Extrema', 'Extrema'),
        ('Aventurera', 'Aventurera'),
        ('Pacífica', 'Pacífica'),
    ]
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Actividad')
    descripcion = models.TextField(verbose_name='Descripción')
    duracion = models.CharField(max_length=50, verbose_name='Duración')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    nivel_dificultad = models.CharField(max_length=10, choices=NIVEL_CHOICES, verbose_name='Nivel de Dificultad')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='actividades', verbose_name='Categoría')

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Paquete')
    descripcion = models.TextField(verbose_name='Descripción')
    actividades = models.ManyToManyField(Actividades, related_name='paquetes', verbose_name='Actividades Incluidas')

    class Meta:
        verbose_name = 'Paquete'
        verbose_name_plural = 'Paquetes'

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Promoción')
    descripcion = models.TextField(verbose_name='Descripción de la Oferta')
    porcentaje_descuento = models.PositiveIntegerField(verbose_name='Porcentaje de Descuento (%)')
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de Finalización')
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='promociones', verbose_name='Paquete en Oferta')
    activo = models.BooleanField(default=True, verbose_name='¿Está Activa?')

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje_descuento}% desc.)"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    ]
    nombre_cliente = models.CharField(max_length=150, verbose_name='Nombre del Cliente')
    fecha = models.DateField(verbose_name='Fecha de Reserva')
    numero_personas = models.PositiveIntegerField(verbose_name='Número de Personas')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name='Estado')
    paquete = models.ForeignKey(Paquete, on_delete=models.PROTECT, verbose_name='Paquete Reservado')
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto Total')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"Reserva {self.id} - {self.nombre_cliente}"