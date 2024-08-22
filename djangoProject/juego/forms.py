from django import forms
from .models import Jugador, Palabra

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre']

class PalabraForm(forms.ModelForm):
    class Meta:
        model = Palabra
        fields = ['palabra', 'pista']
