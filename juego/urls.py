from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('agregar-palabra/', views.agregar_palabra, name='agregar_palabra'),
    path('empezar-juego/', views.empezar_juego, name='empezar_juego'),
    path('jugar/<int:jugador_id>/', views.jugar, name='jugar'),
    path('tabla-puntuaciones/', views.tabla_puntuaciones, name='tabla_puntuaciones'),
    path('fin_juego/<int:jugador_id>/', views.fin_juego, name='fin_juego'),
]
