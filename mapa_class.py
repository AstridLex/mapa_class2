import numpy as np
import heapq

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = self.crear_mapa(filas, columnas)
        self.obstaculos = []

    def crear_mapa(self, filas, columnas):
        return np.full((filas, columnas), " ")

    def poner_obstaculos(self, obstaculos):
        self.obstaculos = obstaculos
        for (fila, columna) in obstaculos:
            self.mapa[fila][columna] = "#"

    def mostrar_mapa(self):
        for fila in self.mapa:
            print("|".join(celda for celda in fila))

    def obtener_coordenadas(self, mensaje):
        while True:
            entrada = input(mensaje)
            if ' ' in entrada:
                x, y = entrada.split()
                if x.isdigit() and y.isdigit():
                    x, y = int(x), int(y)
                    if 0 <= x < self.filas and 0 <= y < self.columnas:
                        return (x, y)
            print("Por favor, ingrese las coordenadas en el formato correcto (x y).")

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def limpiar_camino(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.mapa[fila][columna] == '°':
                    self.mapa[fila][columna] = ' '

    def a_estrella(self, inicio, final):
        abierta = []
        heapq.heappush(abierta, (0, inicio))
        cerrada = {} #los nodo padre e hijo estan dentro del diccionario 
        g_puntaje = {inicio: 0}
        f_puntaje = {inicio: self.heuristica(inicio, final)}

        while abierta:
            _, actual = heapq.heappop(abierta)

            if actual == final:
                camino = []
                while actual in cerrada:
                    camino.append(actual)
                    actual = cerrada[actual]
                camino.append(inicio)
                camino.reverse()
                return camino

            vecinos = [(actual[0] + n_x, actual[1] + n_y) for n_x, n_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

            for vecino in vecinos:
                if 0 <= vecino[0] < self.filas and 0 <= vecino[1] < self.columnas and self.mapa[vecino[0]][vecino[1]] != '#':
                    posible_g = g_puntaje[actual] + 1

                    if vecino not in g_puntaje or posible_g < g_puntaje[vecino]:
                        cerrada[vecino] = actual
                        g_puntaje[vecino] = posible_g
                        f_puntaje[vecino] = posible_g + self.heuristica(vecino, final)
                        heapq.heappush(abierta, (f_puntaje[vecino], vecino))

        return None

    def agregar_obstaculos(self):
        while True:
            entrada = input("Ingrese las coordenadas del obstáculo que desea agregar (x y) o 'X' para terminar: ")
            if entrada.lower() == 'x':
                break
            if ' ' in entrada:
                x, y = entrada.split()
                if x.isdigit() and y.isdigit():
                    x, y = int(x), int(y)
                    if 0 <= x < self.filas and 0 <= y < self.columnas:
                        self.obstaculos.append((x, y))
                        self.mapa[x][y] = "#"
                        print(f"Agregado obstáculo en: ({x}, {y})")
                    else:
                        print(f"Las coordenadas ingresadas no son válidas.")

    def quitar_obstaculos(self):
        while True:
            entrada = input("Ingrese las coordenadas del obstáculo que desea quitar (x y) o 'X' para terminar: ")
            if entrada.lower() == 'x':
                break
            if ' ' in entrada:
                x, y = entrada.split()
                if x.isdigit() and y.isdigit():
                    x, y = int(x), int(y)
                    if (x, y) in self.obstaculos:
                        self.obstaculos.remove((x, y))
                        self.mapa[x][y] = ' '
                    else:
                        print(f"Las coordenadas ingresadas no son válidas o no hay un obstáculo en esa posición.")
                else:
                    print(f"Entrada inválida. Ingrese las coordenadas como números enteros separados por un espacio.")

    def actualizar_objetivos(self, inicio, final):
        self.mapa[inicio[0]][inicio[1]] = 'I'
        self.mapa[final[0]][final[1]] = 'F'

filas, columnas = 31, 31
mapa_obj = Mapa(filas, columnas)

obstaculos = [
    (0, 2), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 12), 
    (0,14), (0, 21), (0, 24), (0, 27), (0, 29), (0, 30), (1, 0), 
    (1, 3), (1, 12), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), 
    (1, 19), (1, 21), (1, 24), (1, 27), (1, 29), (1, 30), (2, 1), (2, 4), (2, 12), (2, 21), (2, 24), (2, 27), (2, 29), (2, 30), (3, 2), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 12), (3, 14), (3, 16), (3, 21), (3, 24), (3, 27), (3, 29), (3, 30), (4, 3), (4, 16), (5, 1), (5, 4), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 13), (5, 14), (5, 16), (5, 20), (5, 23), (6, 1), (6, 3), (6, 5), (6, 13), (6, 14), (6, 16), (6, 19), (6, 24), (7, 1),  (7, 3), (7, 5), (7, 6), (7, 9), (7, 13), (7, 14), (7, 18), (7, 25), (8, 1),  (8, 3), (8, 5), (8, 6), (8, 9), (8, 13), (8, 14), (8, 17), (8, 26), (9, 1), (9, 3), (9, 5), (9, 6), (9, 13), (9, 14), (9, 27), (10, 9), (10, 13), (10, 14), (10, 28), (11, 1), (11, 3), (11, 5), (11, 6), (11, 9), (11, 13), (11, 14), (11, 17), (11, 18), (11, 19), (11, 20), (11, 21), (11, 22), (11, 23), (11, 24), (11, 29), (11, 30), (12, 1),  (12, 3), (12, 5), (12, 6), (12, 9), (12, 13), (12, 14), (12, 17), (12, 24), (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 9), (13, 13), (13, 14), (13, 17), (13, 24), (13, 29), (13, 30), (14, 9), (14, 13), (14, 14), (14, 17), (14, 24), (14, 29), (14, 30), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 9), (15, 13), (15, 14), (15, 17), (15, 18), (15, 19), (15, 20), (15, 22), (15, 23), (15, 24), (15, 29), (15, 30), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 13), (16, 14), (16, 29), (16, 30), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 9), (17, 13), (17, 14), (17, 29), (17, 30), (18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 9), (18, 13), (18, 14), (18, 17), (18, 18), (18, 19), (18, 20), (18, 21), (18, 22), (18, 29), (18, 30), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 9), (19, 13), (19, 14), (19, 17), (19, 23), (20, 2), (20, 3), (20, 4), (20, 5), (20, 6), (20, 9), (20, 13), (20, 14), (20, 17), (20, 24), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 9), (21, 13), (21, 14), (21, 17), (21, 20), (21, 21), (21, 25), (22, 2), (22, 3), (22, 4), (22, 5), (22, 6), (22, 9), (22, 13), (22, 14), (22, 17), (22, 21), (22, 22), (22, 26), (23, 13), (23, 14), (23, 18), (23, 22), (23, 23), (23, 27), (24, 0), (24, 1), (24, 2), (24, 3), (24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 13), (24, 14), (24, 19), (24, 23), (24, 24), (24, 28), (25, 0), (25, 1), (25, 2), (25, 3), (25, 4), (25, 5), (25, 6), (25, 7), (25, 8), (25, 13), (25, 14), (25, 20), (25, 24), (25, 25), (25, 29), (26, 0), (26, 1), (26, 2), (26, 3), (26, 4), (26, 5), (26, 6), (26, 7), (26, 8), (26, 17), (26, 21), (26, 25), (26, 26), (26, 30), (27, 0), (27, 1), (27, 2), (27, 3), (27, 4), (27, 5), (27, 6), (27, 7), (27, 8), (27, 17), (27, 18), (27, 22), (27, 26), (27, 27), (27, 30), (28, 0), (28, 1), (28, 2), (28, 3), (28, 4), (28, 5), (28, 6), (28, 7), (28, 8), (28, 13), (28, 14), (28, 17), (28, 18), (28, 19), (28, 23), (28, 27), (28, 28), (29, 13),  (29, 14), (29, 24), (29, 28), (29, 29), (30, 9), (30, 10), (30, 13), (30, 14), (30, 29)
]
mapa_obj.poner_obstaculos(obstaculos)
inicio = mapa_obj.obtener_coordenadas("Ingrese las coordenadas de inicio (x y): ")
final = mapa_obj.obtener_coordenadas("Ingrese las coordenadas de final (x y): ")

mapa_obj.limpiar_camino()
mapa_obj.actualizar_objetivos(inicio, final)
camino = mapa_obj.a_estrella(inicio, final)

if camino:
    for paso in camino:
        if paso != inicio and paso != final:
            mapa_obj.mapa[paso[0]][paso[1]] = "°"
else:
    print("No hay camino posible.")

mapa_obj.mostrar_mapa()

mapa_obj.agregar_obstaculos()
mapa_obj.quitar_obstaculos()

mapa_obj.limpiar_camino()
mapa_obj.actualizar_objetivos(inicio, final)
camino = mapa_obj.a_estrella(inicio, final)

if camino:
    for paso in camino:
        if paso != inicio and paso != final:
            mapa_obj.mapa[paso[0]][paso[1]] = "°"
else:
    print("No hay camino posible.")

mapa_obj.mostrar_mapa()
