// ============================================================
// ACO - SIMULACIÓN DE COLONIA DE HORMIGAS
// Versión simple, estable y funcional
// ============================================================

const canvas = document.getElementById("simulationCanvas");
const ctx = canvas.getContext("2d");

// ============================================================
// ELEMENTOS HTML
// ============================================================

const antsRange = document.getElementById("antsRange");
const iterationsRange = document.getElementById("iterationsRange");
const alphaRange = document.getElementById("alphaRange");
const betaRange = document.getElementById("betaRange");
const evaporationRange = document.getElementById("evaporationRange");

const antsValue = document.getElementById("antsValue");
const iterationsValue = document.getElementById("iterationsValue");
const alphaValue = document.getElementById("alphaValue");
const betaValue = document.getElementById("betaValue");
const evaporationValue = document.getElementById("evaporationValue");

const startBtn = document.getElementById("startBtn");
const pauseBtn = document.getElementById("pauseBtn");
const resetBtn = document.getElementById("resetBtn");
const obstacleBtn = document.getElementById("obstacleBtn");

const iterationMetric = document.getElementById("iterationMetric");
const antsMetric = document.getElementById("antsMetric");
const distanceMetric = document.getElementById("distanceMetric");
const averageMetric = document.getElementById("averageMetric");

const routeMetric = document.getElementById("routeMetric");
const adaptationMetric = document.getElementById("adaptationMetric");

const statusText = document.getElementById("statusText");
const statusDot = document.getElementById("statusDot");

const environmentBadge =
    document.getElementById("environmentBadge");

// ============================================================
// VARIABLES
// ============================================================

let ants = [];

let pheromones = {};

let running = false;
let paused = false;

let iteration = 0;

let bestDistance = Infinity;
let bestPath = [];

let averageDistance = 0;

let obstacleActive = false;

let iterationTimer = null;

// ============================================================
// NODOS
// ============================================================

let nodes = {};

// ============================================================
// CAMINOS
// ============================================================

const edges = [
    ["A", "B"],
    ["A", "C"],
    ["B", "D"],
    ["C", "D"],
    ["B", "E"],
    ["C", "E"],
    ["D", "E"]
];

// ============================================================
// CANVAS
// ============================================================

function resizeCanvas() {

    const rect =
        canvas.parentElement.getBoundingClientRect();

    canvas.width = rect.width;
    canvas.height = Math.max(480, rect.height);

    createNodes();
    draw();
}

window.addEventListener(
    "resize",
    resizeCanvas
);

// ============================================================
// CREAR NODOS
// ============================================================

function createNodes() {

    const w = canvas.width;
    const h = canvas.height;

    nodes = {

        A: {
            x: w * 0.10,
            y: h * 0.50
        },

        B: {
            x: w * 0.35,
            y: h * 0.25
        },

        C: {
            x: w * 0.35,
            y: h * 0.75
        },

        D: {
            x: w * 0.65,
            y: h * 0.25
        },

        E: {
            x: w * 0.90,
            y: h * 0.50
        }

    };
}

// ============================================================
// DISTANCIA
// ============================================================

function getDistance(a, b) {

    const dx =
        nodes[a].x - nodes[b].x;

    const dy =
        nodes[a].y - nodes[b].y;

    return Math.sqrt(
        dx * dx + dy * dy
    );
}

// ============================================================
// CLAVE DEL CAMINO
// ============================================================

function edgeKey(a, b) {

    return [a, b]
        .sort()
        .join("-");
}

// ============================================================
// INICIALIZAR FEROMONAS
// ============================================================

function initializePheromones() {

    pheromones = {};

    edges.forEach(([a, b]) => {

        pheromones[
            edgeKey(a, b)
        ] = 1;

    });
}

// ============================================================
// CREAR HORMIGA
// ============================================================

function createAnt() {

    return {

        path: ["A"],

        currentNode: "A",

        nextNode: null,

        progress: 0,

        distance: 0,

        finished: false

    };
}

// ============================================================
// CREAR COLONIA
// ============================================================

function createAntColony() {

    ants = [];

    const number =
        Number(antsRange.value);

    for (let i = 0; i < number; i++) {

        ants.push(
            createAnt()
        );

    }

    antsMetric.textContent =
        number;
}

// ============================================================
// OBTENER CAMINOS DISPONIBLES
// ============================================================

function getAvailableNodes(current, ant) {

    let options = [];

    edges.forEach(([a, b]) => {

        if (a === current) {

            options.push(b);

        }

        if (b === current) {

            options.push(a);

        }

    });

    // No regresar inmediatamente
    if (ant.path.length > 1) {

        const previous =
            ant.path[
                ant.path.length - 2
            ];

        options =
            options.filter(
                node => node !== previous
            );
    }

    // Obstáculo
    if (obstacleActive) {

        options =
            options.filter(
                node =>
                    edgeKey(
                        current,
                        node
                    ) !== edgeKey("A", "C")
            );
    }

    return options;
}

// ============================================================
// DECISIÓN ACO
// ============================================================

function chooseNextNode(ant) {

    const current =
        ant.currentNode;

    let options =
        getAvailableNodes(
            current,
            ant
        );

    if (options.length === 0) {

        return "E";

    }

    const alpha =
        Number(alphaRange.value);

    const beta =
        Number(betaRange.value);

    let probabilities = [];

    let total = 0;

    options.forEach(next => {

        const pheromone =
            pheromones[
                edgeKey(
                    current,
                    next
                )
            ] || 1;

        const distance =
            getDistance(
                current,
                next
            );

        const value =
            Math.pow(
                pheromone,
                alpha
            ) *
            Math.pow(
                1 / distance,
                beta
            );

        probabilities.push({
            node: next,
            value: value
        });

        total += value;

    });

    // Selección probabilística
    let random =
        Math.random() * total;

    for (
        const option of probabilities
    ) {

        random -= option.value;

        if (random <= 0) {

            return option.node;

        }

    }

    return options[
        options.length - 1
    ];
}

// ============================================================
// PREPARAR HORMIGAS
// ============================================================

function prepareAnts() {

    ants.forEach(ant => {

        if (!ant.finished) {

            ant.nextNode =
                chooseNextNode(
                    ant
                );

            ant.progress = 0;

        }

    });
}

// ============================================================
// MOVER HORMIGAS
// ============================================================

function moveAnts() {

    let finished = true;

    ants.forEach(ant => {

        if (ant.finished) {

            return;

        }

        finished = false;

        if (!ant.nextNode) {

            ant.nextNode =
                chooseNextNode(
                    ant
                );

        }

        // Velocidad controlada
        ant.progress += 0.025;

        if (ant.progress >= 1) {

            const next =
                ant.nextNode;

            ant.distance +=
                getDistance(
                    ant.currentNode,
                    next
                );

            ant.currentNode =
                next;

            ant.path.push(
                next
            );

            ant.progress = 0;

            ant.nextNode = null;

            if (
                ant.currentNode === "E"
            ) {

                ant.finished = true;

            }

        }

    });

    return ants.every(
        ant => ant.finished
    );
}

// ============================================================
// ACTUALIZAR FEROMONAS
// ============================================================

function updatePheromones() {

    const evaporation =
        Number(
            evaporationRange.value
        );

    // Evaporación
    Object.keys(
        pheromones
    ).forEach(key => {

        pheromones[key] *=
            (1 - evaporation * 0.15);

        pheromones[key] =
            Math.max(
                0.2,
                pheromones[key]
            );

    });

    // Depósito
    ants.forEach(ant => {

        if (!ant.finished) {
            return;
        }

        const deposit =
            100 /
            Math.max(
                ant.distance,
                1
            );

        for (
            let i = 0;
            i < ant.path.length - 1;
            i++
        ) {

            const key =
                edgeKey(
                    ant.path[i],
                    ant.path[i + 1]
                );

            pheromones[key] +=
                deposit * 0.08;

        }

    });
}

// ============================================================
// RESULTADOS
// ============================================================

function calculateResults() {

    const finishedAnts =
        ants.filter(
            ant => ant.finished
        );

    if (
        finishedAnts.length === 0
    ) {

        return;

    }

    const distances =
        finishedAnts.map(
            ant => ant.distance
        );

    averageDistance =
        distances.reduce(
            (a, b) => a + b,
            0
        ) / distances.length;

    const currentBest =
        Math.min(
            ...distances
        );

    if (
        currentBest < bestDistance
    ) {

        bestDistance =
            currentBest;

        const winner =
            finishedAnts.find(
                ant =>
                    ant.distance ===
                    currentBest
            );

        bestPath =
            [...winner.path];

    }

    updateMetrics();
}

// ============================================================
// MÉTRICAS
// ============================================================

function updateMetrics() {

    iterationMetric.textContent =
        iteration;

    antsMetric.textContent =
        antsRange.value;

    distanceMetric.textContent =
        isFinite(bestDistance)
            ? bestDistance.toFixed(0)
            : "—";

    averageMetric.textContent =
        averageDistance > 0
            ? averageDistance.toFixed(0)
            : "—";

    if (
        bestPath.length > 0
    ) {

        routeMetric.textContent =
            bestPath.join(" → ");

    }

}

// ============================================================
// EJECUTAR ITERACIÓN
// ============================================================

function runIteration() {

    if (
        iteration >=
        Number(iterationsRange.value)
    ) {

        finishSimulation();

        return;

    }

    iteration++;

    updateMetrics();

    createAntColony();

    prepareAnts();

    adaptationMetric.textContent =
        obstacleActive
            ? "Adaptándose al cambio"
            : "Explorando rutas";

    // Las hormigas se mueven
    // hasta completar el recorrido
    running = true;
}

// ============================================================
// FINALIZAR SIMULACIÓN
// ============================================================

function finishIteration() {

    calculateResults();

    updatePheromones();

    running = false;

    if (
        iteration <
        Number(iterationsRange.value)
    ) {

        iterationTimer =
            setTimeout(() => {

                if (!paused) {

                    runIteration();

                }

            }, 300);

    } else {

        finishSimulation();

    }
}

// ============================================================
// FINALIZAR TODO
// ============================================================

function finishSimulation() {

    running = false;

    statusText.textContent =
        "Finalizado";

    adaptationMetric.textContent =
        "Modelo estabilizado";

    updateMetrics();
}

// ============================================================
// CICLO DE ANIMACIÓN
// ============================================================

function animationLoop() {

    if (
        running &&
        !paused
    ) {

        const finished =
            moveAnts();

        if (finished) {

            finishIteration();

        }

    }

    draw();

    requestAnimationFrame(
        animationLoop
    );
}

// ============================================================
// DIBUJAR TODO
// ============================================================

function draw() {

    if (
        !canvas.width ||
        !canvas.height
    ) {

        return;

    }

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBackground();

    drawEdges();

    drawPheromones();

    drawObstacle();

    drawNodes();

    drawAnts();

}

// ============================================================
// FONDO
// ============================================================

function drawBackground() {

    ctx.fillStyle =
        "#0b1220";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );
}

// ============================================================
// CAMINOS
// ============================================================

function drawEdges() {

    edges.forEach(
        ([a, b]) => {

            if (
                obstacleActive &&
                edgeKey(a, b) ===
                edgeKey("A", "C")
            ) {

                return;

            }

            ctx.beginPath();

            ctx.moveTo(
                nodes[a].x,
                nodes[a].y
            );

            ctx.lineTo(
                nodes[b].x,
                nodes[b].y
            );

            ctx.strokeStyle =
                "#334155";

            ctx.lineWidth = 2;

            ctx.stroke();

        }
    );
}

// ============================================================
// FEROMONAS
// ============================================================

function drawPheromones() {

    edges.forEach(
        ([a, b]) => {

            if (
                obstacleActive &&
                edgeKey(a, b) ===
                edgeKey("A", "C")
            ) {

                return;

            }

            const value =
                pheromones[
                    edgeKey(a, b)
                ] || 1;

            const width =
                Math.min(
                    2 + value * 1.5,
                    12
                );

            const alpha =
                Math.min(
                    0.20 +
                    value * 0.08,
                    0.85
                );

            ctx.beginPath();

            ctx.moveTo(
                nodes[a].x,
                nodes[a].y
            );

            ctx.lineTo(
                nodes[b].x,
                nodes[b].y
            );

            ctx.strokeStyle =
                `rgba(34,197,94,${alpha})`;

            ctx.lineWidth =
                width;

            ctx.stroke();

        }
    );
}

// ============================================================
// OBSTÁCULO
// ============================================================

function drawObstacle() {

    if (!obstacleActive) {
        return;
    }

    const a = nodes.A;
    const c = nodes.C;

    const x =
        (a.x + c.x) / 2;

    const y =
        (a.y + c.y) / 2;

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        25,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        "rgba(239,68,68,0.85)";

    ctx.fill();

    ctx.fillStyle =
        "#ffffff";

    ctx.font =
        "bold 12px Arial";

    ctx.textAlign =
        "center";

    ctx.fillText(
        "OBSTÁCULO",
        x,
        y + 4
    );
}

// ============================================================
// NODOS
// ============================================================

function drawNodes() {

    Object.entries(
        nodes
    ).forEach(
        ([name, node]) => {

            ctx.beginPath();

            ctx.arc(
                node.x,
                node.y,
                22,
                0,
                Math.PI * 2
            );

            if (name === "A") {

                ctx.fillStyle =
                    "#22c55e";

            } else if (
                name === "E"
            ) {

                ctx.fillStyle =
                    "#ef4444";

            } else {

                ctx.fillStyle =
                    "#2563eb";

            }

            ctx.fill();

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "bold 16px Arial";

            ctx.textAlign =
                "center";

            ctx.textBaseline =
                "middle";

            ctx.fillText(
                name,
                node.x,
                node.y
            );

        }
    );
}

// ============================================================
// HORMIGAS
// ============================================================

function drawAnts() {

    ants.forEach(
        ant => {

            let x;
            let y;

            if (
                ant.nextNode
            ) {

                const start =
                    nodes[
                        ant.currentNode
                    ];

                const end =
                    nodes[
                        ant.nextNode
                    ];

                x =
                    start.x +
                    (
                        end.x -
                        start.x
                    ) *
                    ant.progress;

                y =
                    start.y +
                    (
                        end.y -
                        start.y
                    ) *
                    ant.progress;

            } else {

                x =
                    nodes[
                        ant.currentNode
                    ].x;

                y =
                    nodes[
                        ant.currentNode
                    ].y;

            }

            drawAnt(
                x,
                y
            );

        }
    );
}

// ============================================================
// DIBUJAR HORMIGA
// ============================================================

function drawAnt(x, y) {

    ctx.fillStyle =
        "#facc15";

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        5,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.fillStyle =
        "#111827";

    ctx.beginPath();

    ctx.arc(
        x + 5,
        y,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.strokeStyle =
        "#facc15";

    ctx.lineWidth =
        1.5;

    // patas
    for (
        let i = -1;
        i <= 1;
        i++
    ) {

        ctx.beginPath();

        ctx.moveTo(
            x,
            y
        );

        ctx.lineTo(
            x - 7,
            y + i * 5
        );

        ctx.stroke();

        ctx.beginPath();

        ctx.moveTo(
            x + 2,
            y
        );

        ctx.lineTo(
            x + 8,
            y + i * 5
        );

        ctx.stroke();

    }
}

// ============================================================
// BARRA: HORMIGAS
// ============================================================

antsRange.addEventListener(
    "input",
    () => {

        const value =
            Number(
                antsRange.value
            );

        antsValue.textContent =
            value;

        antsMetric.textContent =
            value;

        // Si no está corriendo,
        // mostrar inmediatamente
        // la nueva cantidad
        if (!running) {

            createAntColony();

            draw();

        }

    }
);

// ============================================================
// BARRA: ITERACIONES
// ============================================================

iterationsRange.addEventListener(
    "input",
    () => {

        const value =
            Number(
                iterationsRange.value
            );

        iterationsValue.textContent =
            value;

        // Si la iteración actual
        // supera el nuevo límite,
        // ajustamos el valor mostrado
        if (
            iteration > value
        ) {

            iteration =
                value;

            updateMetrics();

        }

    }
);

// ============================================================
// BARRA: ALPHA
// ============================================================

alphaRange.addEventListener(
    "input",
    () => {

        const value =
            Number(
                alphaRange.value
            );

        alphaValue.textContent =
            value.toFixed(1);

    }
);

// ============================================================
// BARRA: BETA
// ============================================================

betaRange.addEventListener(
    "input",
    () => {

        const value =
            Number(
                betaRange.value
            );

        betaValue.textContent =
            value.toFixed(1);

    }
);

// ============================================================
// BARRA: EVAPORACIÓN
// ============================================================

evaporationRange.addEventListener(
    "input",
    () => {

        const value =
            Number(
                evaporationRange.value
            );

        evaporationValue.textContent =
            value.toFixed(2);

    }
);

// ============================================================
// BOTÓN INICIAR
// ============================================================

startBtn.addEventListener(
    "click",
    () => {

        clearTimeout(
            iterationTimer
        );

        // Si terminó una simulación,
        // comenzar una nueva
        if (
            iteration >=
            Number(
                iterationsRange.value
            )
        ) {

            iteration = 0;

            bestDistance =
                Infinity;

            bestPath = [];

            averageDistance =
                0;

            initializePheromones();

        }

        paused = false;

        running = false;

        statusText.textContent =
            "Simulando";

        adaptationMetric.textContent =
            obstacleActive
                ? "Adaptándose al cambio"
                : "Explorando rutas";

        runIteration();

    }
);

// ============================================================
// BOTÓN PAUSA
// ============================================================

pauseBtn.addEventListener(
    "click",
    () => {

        paused =
            !paused;

        if (paused) {

            statusText.textContent =
                "Pausado";

            adaptationMetric.textContent =
                "Simulación pausada";

        } else {

            statusText.textContent =
                "Simulando";

            adaptationMetric.textContent =
                obstacleActive
                    ? "Adaptándose al cambio"
                    : "Explorando rutas";

        }

    }
);

// ============================================================
// BOTÓN REINICIAR
// ============================================================

resetBtn.addEventListener(
    "click",
    () => {

        clearTimeout(
            iterationTimer
        );

        running = false;

        paused = false;

        iteration = 0;

        bestDistance =
            Infinity;

        bestPath = [];

        averageDistance =
            0;

        obstacleActive =
            false;

        initializePheromones();

        createAntColony();

        iterationMetric.textContent =
            "0";

        distanceMetric.textContent =
            "—";

        averageMetric.textContent =
            "—";

        routeMetric.textContent =
            "A → C → E";

        adaptationMetric.textContent =
            "Esperando simulación";

        statusText.textContent =
            "Listo";

        environmentBadge.textContent =
            "ENTORNO NORMAL";

        environmentBadge.className =
            "badge normal";

        obstacleBtn.textContent =
            "⚠ Activar obstáculo";

        draw();

    }
);

// ============================================================
// BOTÓN OBSTÁCULO
// ============================================================

obstacleBtn.addEventListener(
    "click",
    () => {

        obstacleActive =
            !obstacleActive;

        if (obstacleActive) {

            environmentBadge.textContent =
                "OBSTÁCULO ACTIVO";

            environmentBadge.className =
                "badge warning";

            obstacleBtn.textContent =
                "✓ Obstáculo activo";

            adaptationMetric.textContent =
                "Adaptándose al cambio";

        } else {

            environmentBadge.textContent =
                "ENTORNO NORMAL";

            environmentBadge.className =
                "badge normal";

            obstacleBtn.textContent =
                "⚠ Activar obstáculo";

        }

        draw();

    }
);

// ============================================================
// INICIALIZACIÓN
// ============================================================

antsValue.textContent =
    antsRange.value;

iterationsValue.textContent =
    iterationsRange.value;

alphaValue.textContent =
    Number(
        alphaRange.value
    ).toFixed(1);

betaValue.textContent =
    Number(
        betaRange.value
    ).toFixed(1);

evaporationValue.textContent =
    Number(
        evaporationRange.value
    ).toFixed(2);

initializePheromones();

resizeCanvas();

createAntColony();

updateMetrics();

requestAnimationFrame(
    animationLoop
);