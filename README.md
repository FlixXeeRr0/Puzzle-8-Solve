# Puzzle 8 Resuelto con Algoritmo A*

## Descripción

Este proyecto implementa una solución al clásico **Puzzle 8** utilizando el **Algoritmo A\***, un algoritmo de búsqueda heurística que encuentra el camino óptimo hacia la solución. El Puzzle 8 es un rompecabezas que consiste en un tablero de 3x3 con los números del 1 al 9 (donde el 9 representa el espacio vacío). El objetivo es ordenar los números en secuencia ascendente, utilizando el espacio vacío para mover las fichas adyacentes.

El objetivo final es que el tablero quede de la siguiente manera:
|   |   |   |
|---|---|---|
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |

El programa cuenta con el siguiente estado inicial el cual se podra comentar o eliminar para hacer uso del metodo `leer_ingreso_manual` para ingresar alguna combinacion personalizada:
|   |   |   |
|---|---|---|
| 4 | 1 | 3 |
| 7 | 2 | 6 |
| 9 | 5 | 8 |

## Funcionalidades

- **Resolución del Puzzle 8**: El programa utiliza el Algoritmo A* para encontrar el camino más corto desde cualquier estado inicial hacia el estado objetivo del puzzle.
- **Visualización paso a paso**: Muestra cada movimiento realizado para resolver el puzzle, indicando la dirección (Arriba, Abajo, Izquierda, Derecha) en que se mueve la ficha.
- **Entrada personalizada**: El programa permite ingresar un estado inicial del puzzle por teclado, usando `9` para representar el espacio vacío.


## Algoritmo A*

El Algoritmo A* es una combinación de los enfoques de búsqueda en anchura y búsqueda en profundidad. Utiliza una función heurística para estimar la distancia hasta el estado objetivo y garantiza que el camino encontrado sea óptimo. En este caso, la **distancia de Manhattan** se utiliza como heurística, la cual mide la distancia entre dos puntos considerando solo movimientos horizontales y verticales.

### Heurística: Distancia de Manhattan

La distancia de Manhattan se calcula sumando las distancias horizontales y verticales entre la posición actual de cada ficha y su posición objetivo en el tablero. Esta heurística es **admisible**, lo que significa que nunca sobreestima el costo para llegar al objetivo, garantizando una solución óptima.

## Estructura del Código

### Clases y Métodos

- **`Estado`**: Representa un estado del tablero. Contiene información sobre el tablero, el estado padre, el costo acumulado `g`, la heurística `h`, el valor total `f = g + h` y movimiento, el cual es una cadena de texto que nos indica hacia donde se realizo el movimiento. También maneja la generación de vecinos y el cálculo de la heurística.
  - **Métodos**:
    - `es_objetivo()`: Verifica si el estado actual es el objetivo final.
    - `generar_vecinos()`: Genera los posibles estados vecinos moviendo el espacio vacío en una de las cuatro direcciones posibles.
    - `calcular_heuristica()`: Calcula la heurística utilizando la distancia de Manhattan.

- **`resolver_puzzle_8`**: Implementa el Algoritmo A*. Usa una cola de prioridad (`heapq`) para almacenar y priorizar los estados según el valor `f`. Los vecinos se exploran hasta encontrar el estado objetivo o agotar las posibilidades.
  
- **`reconstruir_camino`**: Una vez encontrado el estado objetivo, reconstruye el camino óptimo desde el estado inicial al objetivo siguiendo los padres de cada estado.

- **`leer_estado_inicial`**: Permite ingresar el estado inicial del puzzle manualmente.

### Ejecución

El programa solicita al usuario que introduzca el estado inicial del puzzle y luego comienza a resolverlo usando el Algoritmo A*. Los pasos para resolver el puzzle se muestran en la consola, indicando las direcciones de los movimientos.

# Resumen de Carpetas: Puzzle 8 Web y A* Camino
Este repositorio incluye dos carpetas donde se implementa el algoritmo A*.

## A* Camino
Es una página web que implementa el algoritmo A* para encontrar el camino más corto en un mapa con obstáculos. Al finalizar, se muestra la ruta óptima resaltada en otro color para facilitar su identificación.

## Puzzle 8 Web
Esta es una página web que resuelve de forma visual el puzzle 8, paso a paso, utilizando el algoritmo A*. A diferencia del código en Python, la configuración inicial del puzzle debe ser ingresada manualmente modificando la variable de inicialización en el código.

