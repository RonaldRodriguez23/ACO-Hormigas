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


# ============================================================
# COLORES
# ============================================================

FONDO = (18, 22, 30)

BLANCO = (240, 240, 240)

GRIS = (80, 85, 95)

VERDE = (50, 220, 120)

ROJO = (240, 70, 70)

AZUL = (70, 140, 240)

AMARILLO = (245, 200, 60)

MORADO = (180, 100, 240)


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


# ============================================================
# GRAFO
# ============================================================

GRAFO = {

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


ORIGEN = "A"

DESTINO = "E"


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
                sorted(
                    (origen, destino)
                )
            )

            feromonas[conexion] = 1.0


# ============================================================
# OBTENER FEROMONA
# ============================================================

def obtener_feromona(
    origen,
    destino
):

    conexion = tuple(
        sorted(
            (origen, destino)
        )
    )

    return feromonas[conexion]


# ============================================================
# SELECCIÓN PROBABILÍSTICA
# ============================================================

def seleccionar_siguiente(
    actual,
    visitados
):

    candidatos = []

    valores = []


    for vecino, distancia in GRAFO[actual].items():

        if vecino not in visitados:

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


            candidatos.append(
                vecino
            )

            valores.append(
                valor
            )


    if not candidatos:

        return None


    suma = sum(valores)


    probabilidades = [

        valor / suma

        for valor in valores

    ]


    aleatorio = random.random()

    acumulado = 0


    for i, probabilidad in enumerate(
        probabilidades
    ):

        acumulado += probabilidad

        if aleatorio <= acumulado:

            return candidatos[i]


    return candidatos[-1]


# ============================================================
# CLASE HORMIGA
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

        self.esperando = False


        self.elegir_siguiente()


    # --------------------------------------------------------
    # ELEGIR SIGUIENTE NODO
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ACTUALIZAR MOVIMIENTO
    # --------------------------------------------------------

    def actualizar(self):

        if self.finalizada:

            return


        destino_x, destino_y = NODOS[
            self.siguiente
        ]


        dx = destino_x - self.x

        dy = destino_y - self.y


        distancia = math.sqrt(

            dx * dx +

            dy * dy

        )


        if distancia <= self.velocidad:

            self.x = destino_x

            self.y = destino_y


            distancia_arista = GRAFO[
                self.actual
            ][
                self.siguiente
            ]


            self.distancia += (
                distancia_arista
            )


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

                dx / distancia

            ) * self.velocidad


            self.y += (

                dy / distancia

            ) * self.velocidad


# ============================================================
# EVAPORACIÓN
# ============================================================

def evaporar_feromonas():

    for conexion in feromonas:

        feromonas[conexion] *= (
            1 - EVAPORACION
        )


# ============================================================
# DEPOSITAR FEROMONAS
# ============================================================

def depositar_feromonas(hormigas):

    for hormiga in hormigas:

        if not hormiga.finalizada:

            continue


        if hormiga.distancia <= 0:

            continue


        cantidad = Q / hormiga.distancia


        for i in range(
            len(hormiga.ruta) - 1
        ):

            origen = hormiga.ruta[i]

            destino = hormiga.ruta[
                i + 1
            ]


            conexion = tuple(

                sorted(

                    (
                        origen,
                        destino
                    )
                )

            )


            feromonas[conexion] += cantidad


# ============================================================
# DISTANCIA DE RUTA
# ============================================================

def distancia_ruta(ruta):

    total = 0


    for i in range(
        len(ruta) - 1
    ):

        origen = ruta[i]

        destino = ruta[i + 1]


        total += GRAFO[
            origen
        ][
            destino
        ]


    return total


# ============================================================
# MEJOR RUTA
# ============================================================

def obtener_mejor_ruta(hormigas):

    rutas = []


    for hormiga in hormigas:

        if hormiga.finalizada:

            rutas.append(
                (
                    hormiga.ruta,
                    hormiga.distancia
                )
            )


    if not rutas:

        return None


    return min(

        rutas,

        key=lambda x: x[1]

    )


# ============================================================
# DIBUJAR CONEXIONES
# ============================================================

def dibujar_conexiones(
    pantalla
):

    for origen in GRAFO:

        for destino in GRAFO[origen]:

            if origen > destino:

                continue


            x1, y1 = NODOS[origen]

            x2, y2 = NODOS[destino]


            conexion = tuple(

                sorted(

                    (
                        origen,
                        destino
                    )
                )

            )


            nivel = feromonas[
                conexion
            ]


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
# DIBUJAR NODOS
# ============================================================

def dibujar_nodos(
    pantalla,
    fuente
):

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
# DIBUJAR HORMIGA
# ============================================================

def dibujar_hormiga(

    pantalla,

    hormiga

):

    if hormiga.finalizada:

        color = MORADO

    else:

        color = AMARILLO


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

        (0, 0, ANCHO, 100)

    )


    titulo = fuente_grande.render(

        "INTELIGENCIA DE ENJAMBRE",

        True,

        BLANCO

    )


    pantalla.blit(

        titulo,

        (30, 18)

    )


    subtitulo = fuente.render(

        "Optimización mediante colonia de hormigas",

        True,

        GRIS

    )


    pantalla.blit(

        subtitulo,

        (32, 58)

    )


# ============================================================
# INFORMACIÓN
# ============================================================

def dibujar_estadisticas(

    pantalla,

    fuente,

    hormigas,

    iteracion

):

    mejor = obtener_mejor_ruta(
        hormigas
    )


    if mejor:

        ruta, distancia = mejor

        ruta_texto = " -> ".join(ruta)

    else:

        distancia = 0

        ruta_texto = "Buscando..."


    textos = [

        f"Iteración: {iteracion}",

        f"Hormigas: {len(hormigas)}",

        f"Mejor distancia: {distancia:.2f}",

        f"Mejor ruta: {ruta_texto}"

    ]


    y = 125


    for texto in textos:

        superficie = fuente.render(

            texto,

            True,

            BLANCO

        )


        pantalla.blit(

            superficie,

            (30, y)

        )


        y += 28


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    pygame.init()


    pantalla = pygame.display.set_mode(

        (
            ANCHO,
            ALTO
        )

    )


    pygame.display.set_caption(

        "ACO - Hormigas Inteligentes"

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


    inicializar_feromonas()


    hormigas = [

        Hormiga()

        for _ in range(
            NUM_HORMIGAS
        )

    ]


    iteracion = 1

    tiempo_iteracion = 0


    ejecutando = True


    while ejecutando:

        dt = reloj.tick(FPS)


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                ejecutando = False


        # ----------------------------------------------------
        # ACTUALIZAR HORMIGAS
        # ----------------------------------------------------

        for hormiga in hormigas:

            hormiga.actualizar()


        # ----------------------------------------------------
        # COMPROBAR SI TERMINARON
        # ----------------------------------------------------

        todas_terminaron = all(

            hormiga.finalizada

            for hormiga in hormigas

        )


        if todas_terminaron:

            depositar_feromonas(
                hormigas
            )


            evaporar_feromonas()


            hormigas = [

                Hormiga()

                for _ in range(
                    NUM_HORMIGAS
                )

            ]


            iteracion += 1


        # ----------------------------------------------------
        # DIBUJAR
        # ----------------------------------------------------

        pantalla.fill(FONDO)


        dibujar_panel(

            pantalla,

            fuente_grande,

            fuente

        )


        dibujar_conexiones(

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


        pygame.display.flip()


    pygame.quit()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    main()