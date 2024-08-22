# juego/admin.py
from django.contrib import admin
from .models import Jugador, Palabra

admin.site.register(Jugador)
admin.site.register(Palabra)
