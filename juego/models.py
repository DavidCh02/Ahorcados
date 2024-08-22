from django.db import models

class Jugador(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    puntuacion = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Palabra(models.Model):
    palabra = models.CharField(max_length=100, unique=True)
    pista = models.CharField(max_length=200)

    def __str__(self):
        return self.palabra
