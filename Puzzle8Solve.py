# estado prueba = [
#     [4, 1, 3],
#     [7, 2, 6],
#     [9, 5, 8]
# ]

# Usamos la libreria heapq para gestionar una lista de prioridades,
# esta libreria es util para manejar una colecion de elementos
# donde siempre se quiere acceder al valor minimo o maximo.
import heapq

# Clase Estado que representa un tablero del Puzzle 8 en un punto determinado.
class Estado:
    
    # Constructor de la clase Estado.
    #   - tablero: El tablero actual del puzzle, una lista de listas (3x3).
    #   - padre: El estado previo que llevó a este estado (para reconstruir el camino).
    #   - g: El costo acumulado desde el estado inicial hasta el estado actual.
    #   - h: La heurística estimada de la distancia hasta el objetivo.
    #   - f: El costo total (f = g + h).
    #   - movimiento: El movimiento que se realizó para llegar a este estado.
    def __init__(self, tablero, padre=None, g=0, h=0, movimiento="Estado Inicial"):
        self.tablero = tablero
        self.padre = padre
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.movimiento = movimiento

    # Método para comparar dos estados según su valor f,
    # para usarlos en la cola de prioridad.
    def __lt__(self, other):
        return self.f < other.f

    # Comprueba si el tablero actual es el estado objetivo:
    #   - El estado objetivo es el tablero ordenado como 
    #   [1, 2, 3],
    #   [4, 5, 6],
    #   [7, 8, 9].
    def es_objetivo(self):
        objetivo = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        return self.tablero == objetivo

    # Encuentra la posición del espacio vacío
    # (representado por el número 9) en el tablero.
    def encontrar_vacio(self):
        for i in range(3):  # Itera sobre las Filas.
            for j in range(3):  # Itera sobre las Columnas.
                if self.tablero[i][j] == 9:
                    return i, j  # Devuelve las coordenadas (i, j) del espacio vacío.

    # Genera los posibles estados vecinos moviendo el espacio vacío en las 4
    # direcciones posibles (arriba, abajo, izquierda, derecha).
    def generar_vecinos(self):
        vecinos = []
        
        # Encuentra la posición del espacio vacío.
        x, y = self.encontrar_vacio()
        movimientos = [
            (-1, 0, "Arriba"),
            (1, 0, "Abajo"),
            (0, -1, "Izquierda"),
            (0, 1, "Derecha"),
        ]

        # Intenta mover en cada dirección.
        for dx, dy, direccion in movimientos:
            nuevo_x, nuevo_y = x + dx, y + dy

            # Verifica si el nuevo movimiento está dentro de los límites del tablero.
            if 0 <= nuevo_x < 3 and 0 <= nuevo_y < 3:
                # Crea una copia del tablero para evitar modificar el original.
                nuevo_tablero = [fila[:] for fila in self.tablero]
                # Intercambia la posición del espacio vacío con el nuevo espacio.
                nuevo_tablero[x][y], nuevo_tablero[nuevo_x][nuevo_y] = nuevo_tablero[nuevo_x][nuevo_y], nuevo_tablero[x][y]
                # Crea un nuevo estado vecino y lo agrega a la lista de vecinos.
                vecinos.append(Estado(nuevo_tablero, self, self.g + 1, movimiento=direccion))

        return vecinos  # Devuelve la lista de estados vecinos.

    # Calcula la heurística del tablero actual usando la distancia de Manhattan.
    # La distancia de Manhattan es la suma de las distancias en los ejes x, y
    # desde cada pieza hasta su posición objetivo.
    def calcular_heuristica(self):
        objetivo = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        
        # Inicializa la distancia total en 0.
        distancia = 0  
        for i in range(3):  # Itera sobre las Filas.
            for j in range(3):  # Itera sobre las Columnas.
                valor = self.tablero[i][j]
                if valor != 9:  # No cuenta el espacio vacío en el cálculo.
                    # Calcula la posición objetivo de la pieza actual.
                    objetivo_x = (valor - 1) // 3
                    objetivo_y = (valor - 1) % 3
                    # Suma la distancia de Manhattan para esa pieza.
                    distancia += abs(i - objetivo_x) + abs(j - objetivo_y)
        
        # Asigna la distancia total a la heurística h.
        self.h = distancia
        # Calcula el valor f actualizado.
        self.f = self.g + self.h


# Implementa el algoritmo A* para resolver el puzzle 8.
#   - Usa una lista de prioridades (cola de prioridad) para gestionar 
#   los estados a explorar (open_set).
#   - Usa un conjunto (closed_set) para almacenar los estados que ya 
#   fueron explorados.
def resolver_puzzle_8(estado_inicial):
    # Cola de prioridad que almacena los estados por explorar.
    open_set = [] 
    # Inserta el estado inicial en la cola de prioridad.
    heapq.heappush(open_set, estado_inicial) 
    # Conjunto de estados ya explorados.
    closed_set = set()

    # Mientras haya estados por explorar en open_set.
    while open_set:
        print("OPEN SET: ", open_set)
        print("CLOSED SET: ", closed_set)
        # Toma el estado con el menor valor f.
        actual = heapq.heappop(open_set)

        # Si el estado actual es el objetivo, se reconstruye el camino y
        # retorna la solución.
        if actual.es_objetivo():
            return reconstruir_camino(actual)

        # Marca el estado actual como explorado (usando una representación inmutable).
        closed_set.add(tuple(map(tuple, actual.tablero)))

        # Genera los vecinos del estado actual.
        vecinos = actual.generar_vecinos()
        for vecino in vecinos:
            # Si el estado vecino ya fue explorado, se salta.
            if tuple(map(tuple, vecino.tablero)) in closed_set:
                continue

            # Calcula la heurística y el valor f para el vecino.
            vecino.calcular_heuristica()

            # Agrega el vecino a la cola de prioridad.
            heapq.heappush(open_set, vecino)

    # Si no hay solución, devuelve una lista vacía.
    return []


# Reconstruye el camino desde el estado objetivo hasta el estado inicial,
# siguiendo la cadena de 'padres'.
def reconstruir_camino(estado):
    camino = []
    actual = estado
    
    # Va hacia atrás en el camino desde el estado objetivo hasta el inicial.
    while actual:
        # Añade el tablero actual a la lista del camino.
        camino.append((actual.tablero, actual.movimiento))
        # Retrocede al estado padre.
        actual = actual.padre
    
    # Invierte el camino para que esté en orden desde el inicio hasta el final.
    return camino[::-1]


# Función para leer el estado inicial del puzzle ingresado por el usuario.
def leer_estado_inicial():
    estado_inicial = []
    print("""
===============================================================
==        Introduce el estado inicial del Puzzle 8           ==
==            (usa '9' para el espacio vacío)                ==
===============================================================""")
    print(" NOTA: Los números deben estar separados por un espacio.\n")
    for i in range(3):
        # Lee cada fila del tablero desde la entrada del usuario.
        fila = input(f"Introduce la fila {i+1}: ")
        estado_inicial.append([int(x) for x in fila.split()])

    print("===============================================================")
    return estado_inicial  # Devuelve el tablero inicial ingresado por el usuario.

# Asignar el estado inicial ingresado por el usuario.
# estado_inicial = leer_estado_inicial()
estado_inicial = [
    [4, 1, 3],
    [7, 2, 6],
    [9, 5, 8],
]

# Crear el estado inicial como un objeto de la clase Estado.
estado_inicial_obj = Estado(estado_inicial)
# Calcula la heurística del estado inicial.
estado_inicial_obj.calcular_heuristica()

# Resolver el puzzle.
camino_resuelto = resolver_puzzle_8(estado_inicial_obj)

# Imprimir los pasos para resolver el puzzle.
if camino_resuelto:
    print("==              Pasos para resolver el Puzzle:               ==")
    print("===============================================================")
    for paso, (tablero, movimiento) in enumerate(camino_resuelto):
        if paso < 10:
            print(f"Paso 0{paso + 1}:\t({movimiento})")
        else:
            print(f"Paso {paso + 1}:\t({movimiento})")
        for fila in tablero:
            print(fila)
        print("-------------------------------------")
else:
    # Mostramos un mensaje al usuario si no se encuentra la solución.
    print("Ups, el estado inicial del puzzle no tiene solución.")
