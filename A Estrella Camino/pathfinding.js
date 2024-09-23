let canvas;
let ctx;
const FPS = 120;

// ESCENARIO / TABLERO
const columnas = 50;
const filas = 50;
let escenario = []; // Matriz de columnas x filas

// TILES / CASILLAS / CUADRICULA
let anchoT;
let altoT;

const muro = '#000000';
const tierra = '#ffffff';

// RUTA
let principio;
let final;

let openSet = [];
let closedSet = [];

let camino = [];
let terminado = false;

// CREAMOS UNA MATRIZ 2D
function crearArray2D(filas, columnas) {
    return Array.from({ length: filas }, () => Array(columnas).fill(null));
}

// FUNCION PARA LA HEURISTICA
function heuristica(a, b) {
    return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); // Distancia Manhattan
}

// ELIMINAR ELEMENTO DE UN ARRAY
function borraArray(array, elemento) {
    const index = array.indexOf(elemento);
    if (index !== -1) array.splice(index, 1);
}

// CLASE CASILLA
class Casilla {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.tipo = Math.floor(Math.random() * 5) === 1 ? 1 : 0; // Muro o tierra
        this.f = 0; // Coste total (g + h)
        this.g = 0; // Coste desde el inicio
        this.h = 0; // Heurística (coste hasta el final)
        this.vecinos = [];
        this.padre = null;
    }

    // AGREGAR VECINOS
    agregarVecinos() {
        if (this.x > 0) this.vecinos.push(escenario[this.y][this.x - 1]); // Izquierda
        if (this.x < columnas - 1) this.vecinos.push(escenario[this.y][this.x + 1]); // Derecha
        if (this.y > 0) this.vecinos.push(escenario[this.y - 1][this.x]); // Arriba
        if (this.y < filas - 1) this.vecinos.push(escenario[this.y + 1][this.x]); // Abajo
    }

    // DIBUJAR CASILLA
    dibuja(color) {
        ctx.fillStyle = color;
        ctx.fillRect(this.x * anchoT, this.y * altoT, anchoT, altoT);
    }

    // DIBUJAR OPEN SET, CLOSED SET Y CAMINO
    dibujaOS() { this.dibuja('#0000ff'); }
    dibujaCS() { this.dibuja('#ff0000'); }
    dibujaCamino() { this.dibuja('#00ff00'); }
}

// INICIALIZACIÓN
function inicio() {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // CALCULAR EL TAMAÑO DE LOS TILES
    anchoT = canvas.width / columnas;
    altoT = canvas.height / filas;

    // CREAR EL ESCENARIO
    escenario = crearArray2D(filas, columnas);

    // AÑADIR CASILLAS Y VECINOS
    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            escenario[i][j] = new Casilla(j, i);
        }
    }
    
    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            escenario[i][j].agregarVecinos();
        }
    }

    // INICIALIZAR PRINCIPIO Y FINAL
    principio = escenario[0][0];
    final = escenario[filas - 1][columnas - 1];

    // INICIAR OPEN SET
    openSet.push(principio);

    // BUCLE PRINCIPAL
    setInterval(principal, 1000 / FPS);
}

// DIBUJAR ESCENARIO
function dibujaEscenario() {
    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            escenario[i][j].dibuja(escenario[i][j].tipo === 1 ? muro : tierra);
        }
    }

    openSet.forEach(casilla => casilla.dibujaOS());
    closedSet.forEach(casilla => casilla.dibujaCS());
    camino.forEach(casilla => casilla.dibujaCamino());
}

// LIMPIAR EL CANVAS
function borrarCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// ALGORITMO A*
function algoritmo() {
    if (!terminado && openSet.length > 0) {
        // Elegir la casilla con el menor coste f
        let ganador = openSet.reduce((acc, curr, idx) => curr.f < openSet[acc].f ? idx : acc, 0);
        let actual = openSet[ganador];

        if (actual === final) {
            terminado = true;
            console.log("HEMOS LLEGADO AL FINAL");

            let temp = actual;
            camino.push(temp);
            while (temp.padre) {
                camino.push(temp.padre);
                temp = temp.padre;
            }
        } else {
            borraArray(openSet, actual);
            closedSet.push(actual);

            actual.vecinos.forEach(vecino => {
                if (!closedSet.includes(vecino) && vecino.tipo !== 1) {
                    const tempG = actual.g + 1;

                    if (openSet.includes(vecino)) {
                        if (tempG < vecino.g) {
                            vecino.g = tempG;
                        }
                    } else {
                        vecino.g = tempG;
                        openSet.push(vecino);
                    }

                    vecino.h = heuristica(vecino, final);
                    vecino.f = vecino.g + vecino.h;
                    vecino.padre = actual;
                }
            });
        }
    } else if (openSet.length === 0) {
        console.log("NO HAY SOLUCIÓN");
        terminado = true;
    }
}

// FUNCIÓN PRINCIPAL
function principal() {
    borrarCanvas();
    algoritmo();
    dibujaEscenario();
}
