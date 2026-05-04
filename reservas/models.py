from django.db import models
from django.conf import settings

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Categoría')
    descripcion = models.TextField(verbose_name='Descripción')
    tipo = models.CharField(max_length=50, verbose_name='Tipo de Categoría')
    estado = models.BooleanField(default=True, verbose_name='¿Está Activa?')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Actividades(models.Model):
    NIVEL_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Actividad')
    descripcion = models.TextField(verbose_name='Descripción')
    duracion = models.CharField(max_length=50, verbose_name='Duración')
    nivel_dificultad = models.CharField(max_length=10, choices=NIVEL_CHOICES, verbose_name='Nivel de Dificultad')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='actividades', verbose_name='Categoría')
    estado = models.BooleanField(default=True, verbose_name='¿Está Activa?')
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    imagen = models.ImageField(upload_to='destinos/', null=True, blank=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Paquete')
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.IntegerField(verbose_name='Precio Total')
    actividades = models.ManyToManyField(Actividades, related_name='paquetes', verbose_name='Actividades Incluidas')
    estado = models.BooleanField(default=True, verbose_name='¿Está Activo?')
    class Meta:
        verbose_name = 'Paquete'
        verbose_name_plural = 'Paquetes'

    def __str__(self):
        return self.nombre


class Promocion(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Promoción')
    descripcion = models.TextField(verbose_name='Descripción de la Oferta', null=True, blank=True)
    imagen = models.ImageField(upload_to='promociones/', null=True, blank=True, verbose_name='Imagen del Banner')
    enlace = models.URLField(max_length=500, null=True, blank=True, verbose_name='Enlace (URL)')
    porcentaje_descuento = models.PositiveIntegerField(verbose_name='Porcentaje de Descuento (%)', default=0)
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio', null=True, blank=True)
    fecha_fin = models.DateField(verbose_name='Fecha de Finalización', null=True, blank=True)
    paquete = models.ForeignKey(Paquete, on_delete=models.SET_NULL, null=True, blank=True, related_name='promociones', verbose_name='Paquete en Oferta')
    prioridad = models.PositiveIntegerField(verbose_name='Prioridad/Orden', default=0, help_text='Menor número aparece primero')
    solo_usuarios = models.BooleanField(default=False, verbose_name='Solo usuarios registrados')
    activo = models.BooleanField(default=True, verbose_name='¿Está Activa?')

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje_descuento}% desc.)"

class Reserva(models.Model):
    # Relación con el usuario (Cliente)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reservas_realizadas', 
        verbose_name='Cliente'
    )
    
    paquete = models.ForeignKey(Paquete, on_delete=models.PROTECT, verbose_name='Paquete Reservado')
    fecha = models.DateField(verbose_name='Fecha de Reserva')
    numero_personas = models.PositiveIntegerField(verbose_name='Número de Personas')
    
    # Monto total (se calculará automáticamente)
    monto_total = models.IntegerField(verbose_name='Monto Total', editable=False)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def save(self, *args, **kwargs):
        if self.paquete and self.numero_personas:
            self.monto_total = self.paquete.precio * self.numero_personas
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.get_full_name()} ({self.paquete.nombre})"
    

class PQRS(models.Model):
     TIPO_CHOICES = [
        ('Peticion', 'Petición'),
        ('Queja', 'Queja'),
        ('Reclamo', 'Reclamo'),
        ('Sugerencia', 'Sugerencia'),
     ] 
     nombre_solicitante = models.CharField(max_length=150, verbose_name='Nombre del Solicitante')
     documento = models.CharField(max_length=20, verbose_name='Número de Documento')
     email = models.EmailField(verbose_name='Correo Electrónico')
     tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de PQRS')
     asunto = models.CharField(max_length=200, verbose_name='Asunto')
     descripcion = models.TextField(verbose_name='Descripción')
     evidencia = models.FileField(upload_to='pqrs/', null=True, blank=True, verbose_name='Adjuntar Evidencia')
     respuesta = models.TextField(null=True, blank=True)
     
    
     class Meta:
        verbose_name = 'PQRS'
        verbose_name_plural = 'PQRS'

     def __str__(self):
        return f"{self.tipo} - {self.nombre_solicitante}"
    
class Blog(models.Model):
        titulo = models.CharField(max_length=200, verbose_name='Título del Blog')
        contenido = models.TextField(verbose_name='Contenido del Blog')
        imagen_destacada = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name='Imagen Destacada')
        estado = models.BooleanField(default=True, verbose_name='¿Está Activo?')
        class Meta:
            verbose_name = 'Blog'
            verbose_name_plural = 'Blogs'

        def __str__(self):
            return self.titulo
    