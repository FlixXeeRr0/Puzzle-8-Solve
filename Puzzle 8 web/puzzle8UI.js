
window.addEventListener('DOMContentLoaded', function () {

  // Configuraciones del canvas
  const canvas = document.getElementById('puzzleCanvas');
  const ctx = canvas.getContext('2d');
  const tileSize = 100; // Tamaño de cada celda (100x100)
  
  // Estado de la solución
  let camino = [];
  let pasoActual = 0;
  
  // Función para dibujar el tablero
  function dibujarTablero(tablero) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        const valor = tablero[i][j];
        if (valor !== 9) {
          // No dibujar el espacio vacío (9)
          ctx.fillStyle = '#FFF';
          ctx.fillRect(j * tileSize, i * tileSize, tileSize, tileSize);
          ctx.strokeStyle = '#000';
          ctx.strokeRect(j * tileSize, i * tileSize, tileSize, tileSize);
          ctx.fillStyle = '#000';
          ctx.font = '40px Arial';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(
            valor,
            j * tileSize + tileSize / 2,
            i * tileSize + tileSize / 2
          );
        }
      }
    }
  }
  
  // Lógica del Puzzle 8 con A* (similar al código anterior, adaptado aquí)
  class Estado {
    constructor(tablero, padre = null, g = 0, h = 0) {
      this.tablero = tablero;
      this.padre = padre;
      this.g = g;
      this.h = h;
      this.f = this.g + this.h;
    }
  
    esObjetivo() {
      const objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
      ];
      return JSON.stringify(this.tablero) === JSON.stringify(objetivo);
    }
  
    encontrarVacío() {
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          if (this.tablero[i][j] === 9) {
            return { x: i, y: j };
          }
        }
      }
    }
  
    generarVecinos() {
      const vecinos = [];
      const { x, y } = this.encontrarVacío();
      const movimientos = [
        { dx: -1, dy: 0 }, // Arriba
        { dx: 1, dy: 0 }, // Abajo
        { dx: 0, dy: -1 }, // Izquierda
        { dx: 0, dy: 1 }, // Derecha
      ];
  
      movimientos.forEach((mov) => {
        const nuevoX = x + mov.dx;
        const nuevoY = y + mov.dy;
        if (nuevoX >= 0 && nuevoX < 3 && nuevoY >= 0 && nuevoY < 3) {
          const nuevoTablero = this.tablero.map((fila) => fila.slice());
          [nuevoTablero[x][y], nuevoTablero[nuevoX][nuevoY]] = [
            nuevoTablero[nuevoX][nuevoY],
            nuevoTablero[x][y],
          ];
          vecinos.push(new Estado(nuevoTablero, this, this.g + 1));
        }
      });
  
      return vecinos;
    }
  
    calcularHeuristica() {
      const objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
      ];
      let distancia = 0;
  
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          const valor = this.tablero[i][j];
          if (valor !== 9) {
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
  
  function resolverPuzzle8(estadoInicial) {
    const openSet = [];
    const closedSet = new Set();
    const estadoInicialObj = new Estado(estadoInicial);
    estadoInicialObj.calcularHeuristica();
    openSet.push(estadoInicialObj);
  
    while (openSet.length > 0) {
      let actual = openSet.reduce((a, b) => (a.f < b.f ? a : b));
  
      if (actual.esObjetivo()) {
        return reconstruirCamino(actual);
      }
  
      openSet.splice(openSet.indexOf(actual), 1);
      closedSet.add(JSON.stringify(actual.tablero));
  
      const vecinos = actual.generarVecinos();
      vecinos.forEach((vecino) => {
        if (!closedSet.has(JSON.stringify(vecino.tablero))) {
          vecino.calcularHeuristica();
  
          const yaEnOpenSet = openSet.find(
            (e) => JSON.stringify(e.tablero) === JSON.stringify(vecino.tablero)
          );
          if (!yaEnOpenSet || vecino.g < yaEnOpenSet.g) {
            openSet.push(vecino);
          }
        }
      });
    }
  
    return [];
  }
  
  function reconstruirCamino(estado) {
    const camino = [];
    let actual = estado;
  
    while (actual) {
      camino.push(actual.tablero);
      actual = actual.padre;
    }
  
    return camino.reverse();
  }
  
  // Estado inicial del tablero (ejemplo aleatorio)
  const estadoInicial = [
    [4, 1, 3],
    [7, 2, 6],
    [9, 5, 8], // El 9 representa el espacio vacío
  ];
  
  // Resolver el puzzle y obtener el camino
  camino = resolverPuzzle8(estadoInicial);
  console.log('Pasos para resolver el puzzle:', camino);
  
  // Dibujar el estado inicial
  dibujarTablero(camino[pasoActual]);
  
  // Manejar el evento de clic en el botón para avanzar al siguiente paso
  document.getElementById('nextStepButton').addEventListener('click', () => {
    if (pasoActual < camino.length - 1) {
      pasoActual++;
      dibujarTablero(camino[pasoActual]);
    } else {
      alert('El puzzle ya está resuelto.');
    }
  });
});
