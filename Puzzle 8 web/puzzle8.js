// Puzzle 8 usando el algoritmo A*

class Estado {
    constructor(tablero, padre = null, g = 0, h = 0) {
        this.tablero = tablero; // Tablero actual (matriz 3x3)
        this.padre = padre;     // Estado padre
        this.g = g;             // Coste desde el inicio
        this.h = h;             // Heurística (distancia al objetivo)
        this.f = this.g + this.h; // f = g + h
    }

    // Comprobar si el tablero actual es igual al objetivo
    esObjetivo() {
        const objetivo = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ];
        return JSON.stringify(this.tablero) === JSON.stringify(objetivo);
    }

    // Función para encontrar la posición del número 9 (vacío)
    encontrarVacío() {
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (this.tablero[i][j] === 9) {
                    return { x: i, y: j };
                }
            }
        }
    }

    // Generar posibles movimientos a partir del estado actual
    generarVecinos() {
        const vecinos = [];
        const { x, y } = this.encontrarVacío(); // Coordenadas del espacio vacío (9)

        // Definir movimientos (arriba, abajo, izquierda, derecha)
        const movimientos = [
            { dx: -1, dy: 0 }, // Arriba
            { dx: 1, dy: 0 },  // Abajo
            { dx: 0, dy: -1 }, // Izquierda
            { dx: 0, dy: 1 }   // Derecha
        ];

        movimientos.forEach(mov => {
            const nuevoX = x + mov.dx;
            const nuevoY = y + mov.dy;
            if (nuevoX >= 0 && nuevoX < 3 && nuevoY >= 0 && nuevoY < 3) {
                // Copiar el tablero actual
                const nuevoTablero = this.tablero.map(fila => fila.slice());
                // Intercambiar el vacío con el vecino
                [nuevoTablero[x][y], nuevoTablero[nuevoX][nuevoY]] = [nuevoTablero[nuevoX][nuevoY], nuevoTablero[x][y]];
                // Crear un nuevo estado vecino
                vecinos.push(new Estado(nuevoTablero, this, this.g + 1));
            }
        });

        return vecinos;
    }

    // Calcular la heurística (distancia de Manhattan)
    calcularHeuristica() {
        const objetivo = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ];
        let distancia = 0;

        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const valor = this.tablero[i][j];
                if (valor !== 9) {
                    // Coordenadas objetivo del valor actual
                    const objetivoX = Math.floor((valor - 1) / 3);
                    const objetivoY = (valor - 1) % 3;
                    distancia += Math.abs(i - objetivoX) + Math.abs(j - objetivoY);
                }
            }
        }

        this.h = distancia;
        this.f = this.g + this.h;
    }
}

// Función principal para resolver el Puzzle 8 con A*
function resolverPuzzle8(estadoInicial) {
    const openSet = [];
    const closedSet = new Set();
    const estadoInicialObj = new Estado(estadoInicial);
    estadoInicialObj.calcularHeuristica();
    openSet.push(estadoInicialObj);

    while (openSet.length > 0) {
        // Encontrar el estado con el menor valor de f
        let actual = openSet.reduce((a, b) => (a.f < b.f ? a : b));

        // Si hemos llegado al estado objetivo
        if (actual.esObjetivo()) {
            console.log("¡Puzzle resuelto!");
            reconstruirCamino(actual);
            return;
        }

        // Eliminar el estado actual del openSet y agregarlo al closedSet
        openSet.splice(openSet.indexOf(actual), 1);
        closedSet.add(JSON.stringify(actual.tablero));

        // Generar vecinos
        const vecinos = actual.generarVecinos();
        vecinos.forEach(vecino => {
            if (!closedSet.has(JSON.stringify(vecino.tablero))) {
                vecino.calcularHeuristica();

                const yaEnOpenSet = openSet.find(e => JSON.stringify(e.tablero) === JSON.stringify(vecino.tablero));
                if (!yaEnOpenSet || vecino.g < yaEnOpenSet.g) {
                    openSet.push(vecino);
                }
            }
        });
    }

    console.log("No hay solución.");
}

// Función para reconstruir el camino desde el estado final al inicial
function reconstruirCamino(estado) {
    const camino = [];
    let actual = estado;

    while (actual) {
        camino.push(actual.tablero);
        actual = actual.padre;
    }

    // Imprimir el camino desde el estado inicial al final
    camino.reverse().forEach(tablero => {
        console.log(tablero.map(fila => fila.join(" ")).join("\n"));
        console.log("\n");
    });
}

// Estado inicial del tablero (ejemplo aleatorio)
const estadoInicial = [
    [3, 5, 4],
    [8, 7, 9],
    [1, 2, 6] // El 9 representa el espacio vacío
];

// Resolver el puzzle
resolverPuzzle8(estadoInicial);
