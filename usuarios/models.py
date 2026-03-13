from django.db import models

class Usuario(models.Model):

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.IntegerField()

    correo = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nombres

