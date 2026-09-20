import random
import math


# ============================================================
# CONFIGURACIÓN DEL GRAFO
# ============================================================

grafo = {
    "A": {"B": 4, "C": 2, "D": 7},
    "B": {"A": 4, "C": 5, "E": 6},
    "C": {"A": 2, "B": 5, "D": 3, "E": 4},
    "D": {"A": 7, "C": 3, "E": 2},
    "E": {"B": 6, "C": 4, "D": 2}
}


# ============================================================
# PARÁMETROS DEL ALGORITMO
# ============================================================

NUM_HORMIGAS = 30
NUM_ITERACIONES = 100

ALPHA = 1.0
BETA = 2.0
EVAPORACION = 0.5
Q = 100.0

ORIGEN = "A"
DESTINO = "E"


# ============================================================
# INICIALIZACIÓN DE FEROMONAS
# ============================================================

def inicializar_feromonas():

    feromonas = {}

    for nodo in grafo:

        for vecino in grafo[nodo]:

            conexion = tuple(sorted((nodo, vecino)))

            if conexion not in feromonas:
                feromonas[conexion] = 1.0

    return feromonas


feromonas = inicializar_feromonas()


# ============================================================
# OBTENER FEROMONA
# ============================================================

def obtener_feromona(origen, destino):

    conexion = tuple(sorted((origen, destino)))

    return feromonas[conexion]


# ============================================================
# CALCULAR DISTANCIA
# ============================================================

def calcular_distancia(ruta):

    distancia = 0

    for i in range(len(ruta) - 1):

        origen = ruta[i]
        destino = ruta[i + 1]

        distancia += grafo[origen][destino]

    return distancia


# ============================================================
# SELECCIONAR SIGUIENTE NODO
# ============================================================

def seleccionar_siguiente(actual, visitados):

    candidatos = []

    for vecino, distancia in grafo[actual].items():

        if vecino not in visitados:

            candidatos.append(
                (vecino, distancia)
            )

    if not candidatos:
        return None


    valores = []

    for vecino, distancia in candidatos:

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

        valores.append(valor)


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

            return candidatos[i][0]


    return candidatos[-1][0]


# ============================================================
# CONSTRUIR RUTA
# ============================================================

def construir_ruta():

    ruta = [ORIGEN]

    visitados = {ORIGEN}

    actual = ORIGEN

    max_movimientos = len(grafo)

    movimientos = 0


    while (
        actual != DESTINO
        and movimientos < max_movimientos
    ):

        siguiente = seleccionar_siguiente(
            actual,
            visitados
        )

        if siguiente is None:

            return None


        ruta.append(siguiente)

        visitados.add(siguiente)

        actual = siguiente

        movimientos += 1


    if actual == DESTINO:

        return ruta


    return None


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

def depositar_feromonas(rutas):

    for ruta, distancia in rutas:

        cantidad = Q / distancia


        for i in range(len(ruta) - 1):

            origen = ruta[i]
            destino = ruta[i + 1]

            conexion = tuple(
                sorted(
                    (origen, destino)
                )
            )

            feromonas[conexion] += cantidad


# ============================================================
# EJECUTAR ACO
# ============================================================

def ejecutar_aco():

    global feromonas

    feromonas = inicializar_feromonas()


    mejor_ruta = None
    mejor_distancia = math.inf

    historial = []


    for iteracion in range(
        1,
        NUM_ITERACIONES + 1
    ):

        rutas_validas = []


        for _ in range(NUM_HORMIGAS):

            ruta = construir_ruta()


            if ruta is not None:

                distancia = calcular_distancia(
                    ruta
                )

                rutas_validas.append(
                    (ruta, distancia)
                )


                if distancia < mejor_distancia:

                    mejor_distancia = distancia

                    mejor_ruta = ruta.copy()


        # ----------------------------------------------------
        # EVAPORACIÓN
        # ----------------------------------------------------

        evaporar_feromonas()


        # ----------------------------------------------------
        # NUEVAS FEROMONAS
        # ----------------------------------------------------

        depositar_feromonas(
            rutas_validas
        )


        # ----------------------------------------------------
        # ESTADÍSTICAS
        # ----------------------------------------------------

        if rutas_validas:

            promedio = sum(
                distancia
                for _, distancia in rutas_validas
            ) / len(rutas_validas)

        else:

            promedio = 0


        datos_iteracion = {

            "iteracion": iteracion,

            "mejor_distancia":
                mejor_distancia,

            "promedio":
                promedio,

            "hormigas_validas":
                len(rutas_validas),

            "mejor_ruta":
                mejor_ruta.copy()
        }


        historial.append(
            datos_iteracion
        )


        # ----------------------------------------------------
        # MOSTRAR RESULTADO
        # ----------------------------------------------------

        print(
            f"Iteración {iteracion:03d} | "
            f"Mejor: {mejor_distancia:.2f} | "
            f"Promedio: {promedio:.2f} | "
            f"Hormigas válidas: "
            f"{len(rutas_validas):02d} | "
            f"Ruta: "
            f"{' -> '.join(mejor_ruta)}"
        )


    return (
        mejor_ruta,
        mejor_distancia,
        historial
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 75)
    print(
        "SIMULACIÓN DE INTELIGENCIA DE ENJAMBRE"
    )
    print(
        "OPTIMIZACIÓN MEDIANTE COLONIA DE HORMIGAS"
    )
    print("=" * 75)
    print()


    ruta, distancia, historial = ejecutar_aco()


    print()
    print("=" * 75)
    print("RESULTADO FINAL")
    print("=" * 75)

    print(
        f"Mejor ruta: {' -> '.join(ruta)}"
    )

    print(
        f"Distancia: {distancia:.2f}"
    )

    print(
        f"Iteraciones: {NUM_ITERACIONES}"
    )

    print(
        f"Hormigas por iteración: "
        f"{NUM_HORMIGAS}"
    )

    print()
    print(
        "Simulación finalizada correctamente."
    )