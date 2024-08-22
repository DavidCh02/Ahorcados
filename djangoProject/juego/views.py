from django.shortcuts import render, redirect, get_object_or_404
from .models import Jugador, Palabra
from .forms import JugadorForm, PalabraForm
import random

def inicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:  # Verifica que el nombre no esté vacío
            jugador, created = Jugador.objects.get_or_create(nombre=nombre)  # Crea o obtiene el jugador
            return redirect('jugar', jugador_id=jugador.id)  # Redirige al jugador a la vista de juego

    puntuaciones = Jugador.objects.all().order_by('-puntuacion')
    return render(request, 'juego/inicio.html', {'puntuaciones': puntuaciones})
def agregar_palabra(request):
    if request.method == 'POST':
        form = PalabraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = PalabraForm()
    return render(request, 'juego/agregar_palabra.html', {'form': form})

def empezar_juego(request):
    if request.method == 'POST':
        form = JugadorForm(request.POST)
        if form.is_valid():
            jugador = form.save()
            return redirect('jugar', jugador_id=jugador.id)
    else:
        form = JugadorForm()
    return render(request, 'juego/empezar_juego.html', {'form': form})

def jugar(request, jugador_id):
    global mensaje_error
    jugador = get_object_or_404(Jugador, id=jugador_id)
    palabras = list(Palabra.objects.all())
    puntuaciones = Jugador.objects.all().order_by('-puntuacion')  # Obtener puntuaciones

    # Almacena la palabra actual en la sesión
    if 'palabra_actual' not in request.session:
        palabra_obj = random.choice(palabras)
        request.session['palabra_actual'] = palabra_obj.palabra.upper()
        request.session['pista'] = palabra_obj.pista
        request.session['intentos'] = 6
        request.session['letras_adivinadas'] = ''
        request.session['pista_mostrada'] = False
        request.session['letras_incorrectas'] = []

    palabra = request.session['palabra_actual']
    pista = request.session['pista']
    intentos = request.session['intentos']
    letras_adivinadas = request.session['letras_adivinadas']
    letras_incorrectas = request.session['letras_incorrectas']
    pista_mostrada = request.session['pista_mostrada']

    if request.method == 'POST':
        if 'letra' in request.POST:
            letra = request.POST.get('letra').upper()

            if letra in letras_adivinadas or letra in letras_incorrectas:
                mensaje_error = "Ya has intentado con la letra '{}'.".format(letra)
            else:
                if letra not in palabra:
                    intentos -= 1
                    letras_incorrectas.append(letra)
                else:
                    letras_adivinadas += letra

                palabra_oculta = ''.join([letra if letra in letras_adivinadas else '_' for letra in palabra])

                if '_' not in palabra_oculta:
                    jugador.puntuacion += 100 if not pista_mostrada else 50
                    jugador.save()
                    del request.session['palabra_actual']
                    del request.session['pista']
                    del request.session['intentos']
                    del request.session['letras_adivinadas']
                    del request.session['pista_mostrada']
                    del request.session['letras_incorrectas']
                    return redirect('jugar', jugador_id=jugador.id)

                request.session['intentos'] = intentos
                request.session['letras_adivinadas'] = letras_adivinadas
                request.session['letras_incorrectas'] = letras_incorrectas

                if intentos <= 0:
                    del request.session['palabra_actual']
                    return render(request, 'juego/fin_juego.html', {
                        'jugador': jugador,
                        'puntuaciones': puntuaciones,
                    })

        if 'usar_pista' in request.POST:
            pista_mostrada = True
            request.session['pista_mostrada'] = True

    palabra_oculta = ''.join([letra if letra in letras_adivinadas else '_' for letra in palabra])

    return render(request, 'juego/jugar.html', {
        'jugador': jugador,
        'palabra_oculta': palabra_oculta,
        'pista': pista,
        'intentos': intentos,
        'letras_adivinadas': letras_adivinadas,
        'letras_incorrectas': letras_incorrectas,
        'puntuacion': jugador.puntuacion,
        'pista_mostrada': pista_mostrada,
        'puntuaciones': puntuaciones,  # Agregar puntuaciones al contexto
        'mensaje_error': mensaje_error if 'mensaje_error' in locals() else '',
    })


def tabla_puntuaciones(request):
    jugadores = Jugador.objects.order_by('-puntuacion')
    return render(request, 'juego/tabla_puntuaciones.html', {'jugadores': jugadores})


from django.shortcuts import render, redirect
from .models import Jugador


def fin_juego(request, jugador_id):
    # Obtén el jugador
    jugador = Jugador.objects.get(id=jugador_id)

    # Asegúrate de que el modelo Jugador tiene un atributo para la puntuación
    puntuacion = jugador.puntuacion
    # Aquí debes establecer la lógica para obtener la palabra oculta
    palabra_oculta = request.session.get('palabra_oculta', 'palabra no encontrada')  # Reemplaza con tu lógica real

    # Obtén todas las puntuaciones de los jugadores
    puntuaciones = Jugador.objects.all().order_by('-puntuacion')  # Ordenar por puntuación

    return render(request, 'juego/fin_juego.html', {
        'jugador': jugador,
        'puntuacion': puntuacion,
        'palabra_oculta': palabra_oculta,
        'puntuaciones': puntuaciones
    })
