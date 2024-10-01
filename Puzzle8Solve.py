import heapq
class Estado:
    
    # Constructor de la clase Estado.
    #   - tablero: El tablero actual del puzzle.
    #   - padre: El estado previo.
    #   - g: El costo acumulado desde el estado inicial hasta el estado actual.
    #   - h: La heurística estimada de la distancia hasta el objetivo.
    #   - f: El costo total (f = g + h).
    #   - movimiento: El movimiento que se realizó para llegar a este estado.
    #   - dimension: La dimensión del tablero (3x3 o 4x4).
    def __init__(self, tablero, padre=None, g=0, h=0, movimiento="Estado Inicial", dimension=3):
        self.tablero = tablero
        self.padre = padre
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.movimiento = movimiento
        self.dimension = dimension
        
    def __lt__(self, other):
        return self.f < other.f

    # Comprueba si el tablero actual es el estado objetivo
    def es_objetivo(self):
        if self.dimension == 3:
            objetivo = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]
        else:
            objetivo = [
                [1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16]
            ]
        return self.tablero == objetivo

    def encontrar_vacio(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.tablero[i][j] == (self.dimension ** 2):
                    return i, j  # Devuelve las coordenadas (i, j) del espacio vacío.

    # Genera los posibles estados vecinos moviendo el espacio vacío en las 4
    # direcciones posibles (arriba, abajo, izquierda, derecha).
    def generar_vecinos(self):
        vecinos = []
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
            if 0 <= nuevo_x < self.dimension and 0 <= nuevo_y < self.dimension:
                # Crea una copia del tablero para evitar modificar el original.
                nuevo_tablero = [fila[:] for fila in self.tablero]
                # Intercambia las posiciones.
                nuevo_tablero[x][y], nuevo_tablero[nuevo_x][nuevo_y] = nuevo_tablero[nuevo_x][nuevo_y], nuevo_tablero[x][y]
                # Crea un nuevo estado vecino y lo agrega a la lista de vecinos.
                vecinos.append(Estado(nuevo_tablero, self, self.g + 1, movimiento=direccion, dimension=self.dimension))

        return vecinos

    # Calcula la heurística del tablero actual usando la distancia de Manhattan.
    # La distancia de Manhattan es la suma de las distancias en los ejes x, y
    # desde cada pieza hasta su posición objetivo.
    def calcular_heuristica(self):
        distancia = 0  
        for i in range(self.dimension):
            for j in range(self.dimension):
                valor = self.tablero[i][j]
                if valor != (self.dimension ** 2):
                    objetivo_x = (valor - 1) // self.dimension # División entera para obtener la fila.
                    objetivo_y = (valor - 1) % self.dimension # Modulo 3 para obtener la columna.
                    # Suma la distancia de Manhattan para esa pieza.
                    distancia += abs(i - objetivo_x) + abs(j - objetivo_y)

        self.h = distancia
        self.f = self.g + self.h


# Implementacion del algoritmo A*
def resolver_puzzle_8(estado_inicial):
    # Cola de prioridad que almacena los estados por explorar.
    open_set = []
    # Inserta el estado inicial en la cola de prioridad.
    heapq.heappush(open_set, estado_inicial) 
    # Conjunto de estados ya explorados.
    closed_set = set()

    # Mientras haya estados por explorar en open_set.
    while open_set:
        # Toma el estado con el menor valor f.
        actual = heapq.heappop(open_set)

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
    return []


# Reconstruye el camino desde el estado objetivo hasta el estado inicial.
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



# Funcion para solicitar al usuario si la matriz sera de 3x3 o 4x4
def leer_dimension_tablero():
    print("""
===============================================================
==        Seleccione un tipo de tablero para el puzzle       ==
===============================================================""")
    print("\t1. 3x3")
    print("\t2. 4x4")
    print("===============================================================")
    while True:
        opcion = input("Ingrese una de las opciones (1,2): ")
        if opcion in ["1", "2"]:
            break
        print("Opción inválida. Inténtalo de nuevo.")
    return opcion
    

# Función para leer el estado inicial del puzzle ingresado por el usuario.
def leer_estado_inicial(dimension):
    estado_inicial = []
    print("""
===============================================================
==          Introduce el estado inicial del Puzzle           ==
==   (usa '9' para el espacio vacío en 3x3 o '16' para 4x4)  ==
===============================================================""")
    print(" NOTA: Los números deben estar separados por un espacio.\n")
    for i in range(dimension):
        # Lee cada fila del tablero desde la entrada del usuario.
        fila = input(f"Introduce la fila {i+1}: ")
        estado_inicial.append([int(x) for x in fila.split()])

    print("===============================================================")
    return estado_inicial  # Devuelve el tablero inicial ingresado por el usuario.



# INICIO DE LA EJECUCIÓN DEL PROGRAMA

# Diccionario para mapear el tipo de tablero a su respectiva dimensión.
tablero_Enum = {
    1: 3,
    2: 4,
}
# Elegir el tipo de tablero
tipo_tablero = leer_dimension_tablero()
dimension = tablero_Enum[int(tipo_tablero)]

# Asignar el estado inicial ingresado por el usuario.
# estado_inicial = leer_estado_inicial(dimension)

# Tableros de prueba
if dimension == 3:
    estado_inicial = [
        [4, 1, 3],
        [7, 2, 6],
        [9, 5, 8],
    ]
else:
    estado_inicial = [
        [15, 1, 2, 4],
        [7, 6, 3, 11],
        [5, 16, 9, 10],
        [14, 13, 8, 12],
    ]

# Crear el estado inicial.
estado_tablero = Estado(estado_inicial, dimension=dimension)
# Calcula la heurística del estado inicial.
estado_tablero.calcular_heuristica()

# Resolver el puzzle.
camino_resuelto = resolver_puzzle_8(estado_tablero)

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
    print("Ups, el estado inicial del puzzle no tiene solución.")
