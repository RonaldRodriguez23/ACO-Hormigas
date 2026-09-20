import pygame
import random
import math


# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO = 1200
ALTO = 750
FPS = 60

NUM_HORMIGAS = 30

ALPHA = 1.0
BETA = 2.0

EVAPORACION = 0.5
Q = 100.0

ITERACION_OBSTACULO = 5


# ============================================================
# COLORES
# ============================================================

FONDO = (18, 22, 30)
BLANCO = (240, 240, 240)
GRIS = (130, 135, 145)
VERDE = (50, 220, 120)
ROJO = (240, 70, 70)
AZUL = (70, 140, 240)
AMARILLO = (245, 200, 60)
MORADO = (180, 100, 240)
NARANJA = (255, 140, 50)
CIAN = (60, 220, 220)


# ============================================================
# NODOS
# ============================================================

NODOS = {
    "A": (150, 380),
    "B": (380, 180),
    "C": (470, 380),
    "D": (700, 560),
    "E": (1000, 380)
}

ORIGEN = "A"
DESTINO = "E"


# ============================================================
# GRAFO
# ============================================================

GRAFO_BASE = {

    "A": {
        "B": 4,
        "C": 2,
        "D": 7
    },

    "B": {
        "A": 4,
        "C": 5,
        "E": 6
    },

    "C": {
        "A": 2,
        "B": 5,
        "D": 3,
        "E": 4
    },

    "D": {
        "A": 7,
        "C": 3,
        "E": 2
    },

    "E": {
        "B": 6,
        "C": 4,
        "D": 2
    }
}

GRAFO = {}


# ============================================================
# ESTADO DE LA SIMULACIÓN
# ============================================================

obstaculo_activo = False

mensaje_entorno = "ENTORNO: NORMAL"

pausado = False

mejor_ruta_historica = None
mejor_distancia_historica = float("inf")

mejor_ruta_antes_obstaculo = None
mejor_distancia_antes_obstaculo = float("inf")

iteracion_obstaculo = None
iteracion_adaptacion = None

adaptacion_completada = False


# ============================================================
# FEROMONAS
# ============================================================

feromonas = {}


def inicializar_feromonas():

    global feromonas

    feromonas = {}

    for origen in GRAFO:

        for destino in GRAFO[origen]:

            conexion = tuple(
                sorted((origen, destino))
            )

            feromonas[conexion] = 1.0


# ============================================================
# FEROMONA
# ============================================================

def obtener_feromona(origen, destino):

    conexion = tuple(
        sorted((origen, destino))
    )

    return feromonas.get(
        conexion,
        0.01
    )


# ============================================================
# SELECCIÓN DEL SIGUIENTE NODO
# ============================================================

def seleccionar_siguiente(actual, visitados):

    candidatos = []
    valores = []

    for vecino, distancia in GRAFO[actual].items():

        if vecino in visitados:
            continue

        tau = obtener_feromona(
            actual,
            vecino
        )

        eta = 1 / distancia

        valor = (
            tau ** ALPHA
        ) * (
            eta ** BETA
        )

        candidatos.append(vecino)
        valores.append(valor)

    if not candidatos:

        return None

    suma = sum(valores)

    if suma <= 0:

        return random.choice(candidatos)

    probabilidades = [
        valor / suma
        for valor in valores
    ]

    aleatorio = random.random()

    acumulado = 0

    for i, probabilidad in enumerate(probabilidades):

        acumulado += probabilidad

        if aleatorio <= acumulado:

            return candidatos[i]

    return candidatos[-1]


# ============================================================
# HORMIGA
# ============================================================

class Hormiga:

    def __init__(self):

        self.ruta = [ORIGEN]

        self.visitados = {ORIGEN}

        self.actual = ORIGEN

        self.siguiente = None

        self.x, self.y = NODOS[ORIGEN]

        self.velocidad = random.uniform(
            1.5,
            2.8
        )

        self.distancia = 0

        self.finalizada = False

        self.elegir_siguiente()


    def elegir_siguiente(self):

        if self.actual == DESTINO:

            self.finalizada = True

            return

        siguiente = seleccionar_siguiente(
            self.actual,
            self.visitados
        )

        if siguiente is None:

            self.finalizada = True

            return

        self.siguiente = siguiente


    def actualizar(self):

        if self.finalizada:

            return

        destino_x, destino_y = NODOS[
            self.siguiente
        ]

        dx = destino_x - self.x
        dy = destino_y - self.y

        distancia_visual = math.sqrt(
            dx * dx + dy * dy
        )

        if distancia_visual <= self.velocidad:

            self.x = destino_x
            self.y = destino_y

            distancia_arista = GRAFO[
                self.actual
            ][
                self.siguiente
            ]

            self.distancia += distancia_arista

            self.actual = self.siguiente

            self.ruta.append(
                self.actual
            )

            self.visitados.add(
                self.actual
            )

            if self.actual == DESTINO:

                self.finalizada = True

            else:

                self.elegir_siguiente()

        else:

            self.x += (
                dx / distancia_visual
            ) * self.velocidad

            self.y += (
                dy / distancia_visual
            ) * self.velocidad


# ============================================================
# ACTIVAR OBSTÁCULO
# ============================================================

def activar_obstaculo(iteracion):

    global GRAFO
    global obstaculo_activo
    global mensaje_entorno
    global iteracion_obstaculo
    global mejor_ruta_antes_obstaculo
    global mejor_distancia_antes_obstaculo

    if obstaculo_activo:

        return

    obstaculo_activo = True

    iteracion_obstaculo = iteracion

    mejor_ruta_antes_obstaculo = (
        mejor_ruta_historica.copy()
        if mejor_ruta_historica
        else None
    )

    mejor_distancia_antes_obstaculo = (
        mejor_distancia_historica
    )

    mensaje_entorno = (
        "OBSTÁCULO DETECTADO - REPLANIFICANDO"
    )

    # Bloqueamos C -> E

    if "E" in GRAFO["C"]:

        del GRAFO["C"]["E"]

    if "C" in GRAFO["E"]:

        del GRAFO["E"]["C"]


# ============================================================
# ACTUALIZAR MEJOR RESULTADO
# ============================================================

def actualizar_mejor_resultado(hormigas, iteracion):

    global mejor_ruta_historica
    global mejor_distancia_historica

    global iteracion_adaptacion
    global adaptacion_completada
    global mensaje_entorno

    rutas_validas = []

    for hormiga in hormigas:

        if not hormiga.finalizada:
            continue

        if hormiga.actual != DESTINO:
            continue

        if hormiga.distancia <= 0:
            continue

        rutas_validas.append(
            (
                hormiga.ruta.copy(),
                hormiga.distancia
            )
        )

    if not rutas_validas:

        return

    mejor_actual = min(
        rutas_validas,
        key=lambda x: x[1]
    )

    ruta_actual, distancia_actual = mejor_actual

    # Mejor resultado histórico general

    if distancia_actual < mejor_distancia_historica:

        mejor_distancia_historica = (
            distancia_actual
        )

        mejor_ruta_historica = (
            ruta_actual.copy()
        )

    # Comprobar adaptación

    if (
        obstaculo_activo
        and not adaptacion_completada
    ):

        ruta_anterior = (
            mejor_ruta_antes_obstaculo
        )

        if (
            ruta_anterior is not None
            and ruta_actual != ruta_anterior
        ):

            adaptacion_completada = True

            iteracion_adaptacion = iteracion

            mensaje_entorno = (
                "ADAPTACIÓN COMPLETADA - NUEVA RUTA"
            )


# ============================================================
# DISTANCIA PROMEDIO
# ============================================================

def obtener_promedio(hormigas):

    distancias = [

        hormiga.distancia

        for hormiga in hormigas

        if hormiga.finalizada
        and hormiga.distancia > 0

    ]

    if not distancias:

        return 0.0

    return sum(distancias) / len(distancias)


# ============================================================
# EVAPORACIÓN
# ============================================================

def evaporar_feromonas():

    for conexion in feromonas:

        feromonas[conexion] *= (
            1 - EVAPORACION
        )

        feromonas[conexion] = max(
            feromonas[conexion],
            0.05
        )


# ============================================================
# DEPÓSITO DE FEROMONA
# ============================================================

def depositar_feromonas(hormigas):

    for hormiga in hormigas:

        if not hormiga.finalizada:
            continue

        if hormiga.distancia <= 0:
            continue

        cantidad = (
            Q / hormiga.distancia
        )

        for i in range(
            len(hormiga.ruta) - 1
        ):

            origen = hormiga.ruta[i]

            destino = hormiga.ruta[i + 1]

            conexion = tuple(
                sorted(
                    (
                        origen,
                        destino
                    )
                )
            )

            if conexion in feromonas:

                feromonas[conexion] += cantidad


# ============================================================
# DIBUJAR CONEXIONES
# ============================================================

def dibujar_conexiones(pantalla):

    conexiones_dibujadas = set()

    for origen in GRAFO:

        for destino in GRAFO[origen]:

            conexion = tuple(
                sorted(
                    (
                        origen,
                        destino
                    )
                )
            )

            if conexion in conexiones_dibujadas:
                continue

            conexiones_dibujadas.add(
                conexion
            )

            x1, y1 = NODOS[origen]

            x2, y2 = NODOS[destino]

            nivel = obtener_feromona(
                origen,
                destino
            )

            grosor = min(
                2 + int(nivel / 20),
                12
            )

            color = (
                min(
                    80 + int(nivel * 2),
                    240
                ),
                70,
                180
            )

            pygame.draw.line(
                pantalla,
                color,
                (x1, y1),
                (x2, y2),
                grosor
            )


# ============================================================
# OBSTÁCULO
# ============================================================

def dibujar_obstaculo(pantalla):

    if not obstaculo_activo:

        return

    x1, y1 = NODOS["C"]
    x2, y2 = NODOS["E"]

    mitad_x = (x1 + x2) // 2
    mitad_y = (y1 + y2) // 2

    pygame.draw.rect(
        pantalla,
        NARANJA,
        (
            mitad_x - 30,
            mitad_y - 25,
            60,
            50
        )
    )

    fuente = pygame.font.SysFont(
        "Arial",
        16,
        bold=True
    )

    texto = fuente.render(
        "BLOQUEO",
        True,
        BLANCO
    )

    pantalla.blit(
        texto,
        (
            mitad_x -
            texto.get_width() // 2,
            mitad_y -
            texto.get_height() // 2
        )
    )


# ============================================================
# NODOS
# ============================================================

def dibujar_nodos(pantalla, fuente):

    for nombre, posicion in NODOS.items():

        x, y = posicion

        if nombre == ORIGEN:

            color = VERDE

        elif nombre == DESTINO:

            color = ROJO

        else:

            color = AZUL

        pygame.draw.circle(
            pantalla,
            color,
            (x, y),
            28
        )

        texto = fuente.render(
            nombre,
            True,
            BLANCO
        )

        pantalla.blit(
            texto,
            (
                x -
                texto.get_width() // 2,
                y -
                texto.get_height() // 2
            )
        )


# ============================================================
# HORMIGA
# ============================================================

def dibujar_hormiga(pantalla, hormiga):

    color = (
        MORADO
        if hormiga.finalizada
        else AMARILLO
    )

    pygame.draw.circle(
        pantalla,
        color,
        (
            int(hormiga.x),
            int(hormiga.y)
        ),
        6
    )


# ============================================================
# PANEL
# ============================================================

def dibujar_panel(
    pantalla,
    fuente_grande,
    fuente
):

    pygame.draw.rect(
        pantalla,
        (25, 30, 40),
        (0, 0, ANCHO, 105)
    )

    titulo = fuente_grande.render(
        "INTELIGENCIA DE ENJAMBRE",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (30, 15)
    )

    subtitulo = fuente.render(
        "Optimización mediante colonia de hormigas",
        True,
        GRIS
    )

    pantalla.blit(
        subtitulo,
        (32, 55)
    )

    controles = fuente.render(
        "ESPACIO: Pausar / Continuar     R: Reiniciar",
        True,
        CIAN
    )

    pantalla.blit(
        controles,
        (700, 55)
    )


# ============================================================
# ESTADÍSTICAS
# ============================================================

def dibujar_estadisticas(
    pantalla,
    fuente,
    hormigas,
    iteracion
):

    promedio = obtener_promedio(
        hormigas
    )

    if mejor_ruta_historica:

        ruta_texto = " -> ".join(
            mejor_ruta_historica
        )

        distancia_texto = (
            f"{mejor_distancia_historica:.2f}"
        )

    else:

        ruta_texto = "Buscando..."

        distancia_texto = "Calculando..."

    if (
        iteracion_obstaculo is not None
    ):

        texto_obstaculo = (
            f"Obstáculo: iteración "
            f"{iteracion_obstaculo}"
        )

    else:

        texto_obstaculo = (
            "Obstáculo: pendiente"
        )

    if (
        iteracion_adaptacion is not None
    ):

        tiempo_adaptacion = (
            iteracion_adaptacion
            - iteracion_obstaculo
        )

        texto_adaptacion = (
            f"Adaptación: {tiempo_adaptacion} iteraciones"
        )

    else:

        texto_adaptacion = (
            "Adaptación: en proceso"
        )

    textos = [

        f"Iteración: {iteracion}",

        f"Hormigas: {NUM_HORMIGAS}",

        f"Promedio actual: {promedio:.2f}",

        f"Mejor distancia histórica: {distancia_texto}",

        f"Mejor ruta histórica: {ruta_texto}",

        texto_obstaculo,

        texto_adaptacion,

        mensaje_entorno

    ]

    y = 125

    for texto in textos:

        if "OBSTÁCULO" in texto:

            color = NARANJA

        elif "ADAPTACIÓN" in texto:

            color = VERDE

        else:

            color = BLANCO

        superficie = fuente.render(
            texto,
            True,
            color
        )

        pantalla.blit(
            superficie,
            (30, y)
        )

        y += 28


# ============================================================
# REINICIAR
# ============================================================

def reiniciar():

    global GRAFO

    global obstaculo_activo
    global mensaje_entorno
    global mejor_ruta_historica
    global mejor_distancia_historica
    global mejor_ruta_antes_obstaculo
    global mejor_distancia_antes_obstaculo
    global iteracion_obstaculo
    global iteracion_adaptacion
    global adaptacion_completada

    GRAFO = {
        nodo: conexiones.copy()
        for nodo, conexiones
        in GRAFO_BASE.items()
    }

    obstaculo_activo = False

    mensaje_entorno = "ENTORNO: NORMAL"

    mejor_ruta_historica = None

    mejor_distancia_historica = float("inf")

    mejor_ruta_antes_obstaculo = None

    mejor_distancia_antes_obstaculo = float("inf")

    iteracion_obstaculo = None

    iteracion_adaptacion = None

    adaptacion_completada = False

    inicializar_feromonas()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    global pausado

    reiniciar()

    pygame.init()

    pantalla = pygame.display.set_mode(
        (
            ANCHO,
            ALTO
        )
    )

    pygame.display.set_caption(
        "ACO - Adaptación del Enjambre"
    )

    reloj = pygame.time.Clock()

    fuente_grande = pygame.font.SysFont(
        "Arial",
        30,
        bold=True
    )

    fuente = pygame.font.SysFont(
        "Arial",
        18
    )

    hormigas = [
        Hormiga()
        for _ in range(NUM_HORMIGAS)
    ]

    iteracion = 1

    ejecutando = True

    while ejecutando:

        reloj.tick(FPS)

        # ====================================================
        # EVENTOS
        # ====================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                ejecutando = False

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:

                    pausado = not pausado

                elif evento.key == pygame.K_r:

                    reiniciar()

                    hormigas = [
                        Hormiga()
                        for _ in range(NUM_HORMIGAS)
                    ]

                    iteracion = 1

        # ====================================================
        # SIMULACIÓN
        # ====================================================

        if not pausado:

            # Activar obstáculo

            if (
                iteracion >= ITERACION_OBSTACULO
                and not obstaculo_activo
            ):

                activar_obstaculo(
                    iteracion
                )

            # Actualizar hormigas

            for hormiga in hormigas:

                hormiga.actualizar()

            # =================================================
            # ¿TERMINÓ LA ITERACIÓN?
            # =================================================

            todas_terminaron = all(
                hormiga.finalizada
                for hormiga in hormigas
            )

            if todas_terminaron:

                actualizar_mejor_resultado(
                    hormigas,
                    iteracion
                )

                depositar_feromonas(
                    hormigas
                )

                evaporar_feromonas()

                hormigas = [
                    Hormiga()
                    for _ in range(NUM_HORMIGAS)
                ]

                iteracion += 1

        # ====================================================
        # DIBUJAR
        # ====================================================

        pantalla.fill(FONDO)

        dibujar_panel(
            pantalla,
            fuente_grande,
            fuente
        )

        dibujar_conexiones(
            pantalla
        )

        dibujar_obstaculo(
            pantalla
        )

        dibujar_nodos(
            pantalla,
            fuente
        )

        for hormiga in hormigas:

            dibujar_hormiga(
                pantalla,
                hormiga
            )

        dibujar_estadisticas(
            pantalla,
            fuente,
            hormigas,
            iteracion
        )

        # Indicador de pausa

        if pausado:

            pausa = fuente_grande.render(
                "SIMULACIÓN PAUSADA",
                True,
                NARANJA
            )

            pantalla.blit(
                pausa,
                (
                    ANCHO - 330,
                    125
                )
            )

        pygame.display.flip()

    pygame.quit()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()