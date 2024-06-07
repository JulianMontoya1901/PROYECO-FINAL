# PROYECO-FINAL

///1)Código de modelado virtual del brazo en html:
"
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="utf-8">
    <title>Mi primera aplicación three.js</title>
    <style>
        body { margin: 0; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/three@0.126.1/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.126.1/examples/js/controls/OrbitControls.js"></script>
	<style>
			button {
	            padding: 10px 20px;
	            font-size: 16px;
	            margin: 5px;
	            border-radius: 10px;
	            border: none;
	            cursor: pointer;
	            background-color: #ddd;
	        }
	        /* Estilos para la disposición de los botones */
	        .button-row {
	            display: flex;
	            justify-content: center;
	            align-items: center; /* Centra verticalmente */
	            margin-bottom: 10px; /* Agrega un espacio entre las filas de botones */
	        }
		</style>
</head>

<body>

   

    <!-- Contenedor para el gráfico 3D -->
    <div id="arm"></div>
    <div id="error"></div>

    <!-- Descripción de la funcionalidad
     <p>Control the onboard LED</p>-->




     <style>
        h1 {
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 36px;
            color: #333;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
    </style>
    
    <h1>Control del Carro</h1>

    <!-- Div para agrupar los botones en una fila -->
    <div class="button-row">
        <!-- Botón para mover hacia arriba con flecha hacia arriba -->
        <a href="?adelante"><button>&#8593;</button></a>
    </div>

    <!-- Div para agrupar los botones en una fila -->
    <div class="button-row">
        <!-- Botón para mover hacia la izquierda con flecha hacia la izquierda -->
        <a href="?izquierda"><button>&#8592;</button></a>

        <!-- Botón para mover hacia abajo con flecha hacia abajo -->
        <a href="?atras"><button>&#8595;</button></a>

        <!-- Botón para mover hacia la derecha con flecha hacia la derecha -->
        <a href="?derecha"><button>&#8594;</button></a>
    </div>

    <!-- Botón de baile -->
    <div class="button-row">
        <a href="?bailar"><button>¡Bailar!</button></a>
    </div>

    <!-- Botón de sierra -->
    <div class="button-row">
        <a href="?arriba1"><button>&#10227;</button></a>
        <a href="#" id="stopSierraButton"><button>&#9747;</button></a>
    </div>

    <!-- Botones brazo -->
    <div class="button-row">
        <a href="?arriba2"><button>&#8593;</button></a>
        <a href="?abajo2"><button>&#8595;</button></a>
    </div>

    <canvas id="canvas"></canvas>
    <script src="script.js"></script>
    <script>
    // Configuración de la simulación
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Parámetros de la circunferencia
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 200;
    const speed = 0.01;

    // Ángulo inicial
    let angle = 0;

    // Función para dibujar la pista (en este caso, una circunferencia)
    function drawTrack() {
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 3 * Math.PI);
        ctx.stroke();
    }

    // Función para dibujar el carro
    function drawCar(x, y, angle) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angle);
        ctx.fillStyle = '#ff0';
        ctx.fillRect(0, -15, 50, 30); // Ejemplo de dibujo de un carro básico
        ctx.restore();
    }

    // Función para actualizar la animación
    function update() {
        // Actualiza el ángulo del carro
        angle += speed;
        // Si el ángulo excede 2*pi, lo reseteamos
        if (angle >= Math.PI * 2) {
            angle = 0;
        }
    }

    // Función de renderizado principal
    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawTrack();
        const carX = centerX + radius * Math.cos(angle);
        const carY = centerY + radius * Math.sin(angle);
        drawCar(carX, carY, angle - Math.PI / 2); // Ajusta el ángulo para que el carro apunte hacia el centro
        update();
        requestAnimationFrame(render);
    }

    // Inicia la simulación
    render();
    </script>


    <script>
        // Configurar la escena y la cámara de Three.js
        const width = window.innerWidth;
        const height = window.innerHeight / 2;
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.x = 8; // Mover la cámara más lejos
        camera.position.y = 5; // Mover la cámara más lejos
        camera.position.z = 8; // Mover la cámara más lejos
        camera.lookAt(0, 0, 0);

        // Inicializar controles de la cámara
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(width, height);
        renderer.setClearColor(0x25EE22, 1); // Establecer el color de fondo a verde
        const arm_DOM = document.getElementById("arm");
        arm_DOM.appendChild(renderer.domElement);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enablePan = false; // Deshabilitar el movimiento de panorámica
        controls.enableZoom = false; // Deshabilitar el zoom

        // Variables para el control de la cámara
        let mouseX = 10;
        let mouseY = -10;
        let targetX = 20;
        let targetY = 30;

        // Definir un punto en el espacio 3D
        const point = new THREE.Vector3();

        // Establecer el color inicial del LED y las dimensiones del brazo
        let color_led = 0x00fff0;
        const a1 = 1;
        const a2 = 1.5;
        const a3 = 1.5;

        // Definir un pequeño punto para la visualización
        let dot = new THREE.BoxGeometry(0.01, 0.01, 0.01);


        // Crear la geometría de las protoboards
        const figuraGeometry = new THREE.BoxGeometry(1.75, 0.1, 0.6);
        const figuraMaterial = new THREE.MeshBasicMaterial({ color: 0xEAE3E3 });
        const proto = new THREE.Mesh(figuraGeometry, figuraMaterial);
        proto.translateY(a1 / 2.5);
        proto.rotation.y = Math.PI /2.7;
        proto.position.set(0.7, 0.3, 0.3);
        scene.add(proto);

        const figuraGeometry2 = new THREE.BoxGeometry(1, 0.1, 0.6);
        const figuraMaterial2 = new THREE.MeshBasicMaterial({ color: 0xEAE3E3});
        const proto2 = new THREE.Mesh(figuraGeometry2, figuraMaterial2);
        proto2.translateY(a1 / 2.5);
        proto2.rotation.y = Math.PI /2.7;
        proto2.position.set(-0.7, 0.3, -0.3);
        scene.add(proto2);
        

        // Crear la geometría de las raspberrys
        const figuraGeometry3 = new THREE.BoxGeometry(0.5, 0.05, 0.3);
        const figuraMaterial3 = new THREE.MeshBasicMaterial({ color: 0x0FA800 });
        const raspb = new THREE.Mesh(figuraGeometry3, figuraMaterial3);
        raspb.translateY(a1 / 2.5);
        raspb.rotation.y = Math.PI /2.7;
        raspb.position.set(0.45, 0.37, 0.8);
        scene.add(raspb);

        const figuraGeometry4 = new THREE.BoxGeometry(0.5, 0.05, 0.3);
        const figuraMaterial4 = new THREE.MeshBasicMaterial({ color: 0x0FA800 });
        const raspb2 = new THREE.Mesh(figuraGeometry4, figuraMaterial4);
        raspb2.translateY(a1 / 2.5);
        raspb2.rotation.y = Math.PI /2.7;
        raspb2.position.set(-0.66, 0.37, -0.45);
        scene.add(raspb2);

        // Crear la geometría del puente H y los servos
        const figuraGeometry5 = new THREE.BoxGeometry(0.4, 0.05, 0.4);
        const figuraMaterial5 = new THREE.MeshBasicMaterial({ color: 0xCB0303 });
        const pth = new THREE.Mesh(figuraGeometry5, figuraMaterial5);
        pth.translateY(a1 / 2.5);
        pth.rotation.y = Math.PI /2.7;
        pth.position.set(0.9, 0.37, -0.2);
        scene.add(pth);

        const figuraGeometry6 = new THREE.BoxGeometry(0.9, 0.3, 0.3);
        const figuraMaterial6 = new THREE.MeshBasicMaterial({ color: 0x002FCF });
        const servo = new THREE.Mesh(figuraGeometry6, figuraMaterial6);
        servo.translateY(a1 / 2.5);
        servo.rotation.y = Math.PI /2.7;
        servo.position.set(-0.05, 0.5, -0.025);
        scene.add(servo);


        // Configurar la base del brazo mecánico
        let geometry = new THREE.BoxGeometry(0.8, a1 / 2, 0.6);
        let material = new THREE.MeshBasicMaterial({ color: 0x7F6000 });
        const base = new THREE.Mesh(geometry, material);
        base.translateY(a1 / 2);
        scene.add(base);

        // Crear estructura jerárquica para los segmentos del brazo
        let shoulder = new THREE.Object3D();
        shoulder.translateY(a1 / 4);
        base.add(shoulder);

        geometry = new THREE.BoxGeometry(0.1, a2, 0.06);
        let lowerArm = new THREE.Mesh(geometry, material);
        let lowerArm2 = new THREE.Mesh(geometry, material);
        let lowerArm3 = new THREE.Mesh(geometry, material);

        geometry = new THREE.BoxGeometry(0.1, a3 * 1.36, 0.06);
        lowerArm4 = new THREE.Mesh(geometry, material);

        lowerArm4.position.set(0.20, -0.08, -0.15);
        lowerArm4.translateY(a3 / 2);

        shoulder.add(lowerArm4);

        let elbow4 = new THREE.Object3D();
        elbow4.position.set(0, -a2 / 3, 0);
        lowerArm4.add(elbow4);




        lowerArm.position.set(-0.3, 0.2, 0.15);
        lowerArm2.position.set(-0.3, 0.2, -0.15);
        lowerArm3.position.set(0.3, 0.2, 0.15);




        lowerArm.translateY(a2 / 2);
        lowerArm2.translateY(a2 / 2);
        lowerArm3.translateY(a2 / 2);
        shoulder.add(lowerArm);
        shoulder.add(lowerArm2);
        shoulder.add(lowerArm3);




        geometry = new THREE.BoxGeometry(0.03, 0.03, 0.1);
        let joint = new THREE.Mesh(geometry, material);
        let joint2 = new THREE.Mesh(geometry, material);
        joint.position.setY(a2 / 2);
        joint2.position.setY(a2 / 2);
        lowerArm.add(joint);
        lowerArm2.add(joint2);



        let elbow = new THREE.Object3D();
        elbow.translateY(a2 / 2);
        lowerArm.add(elbow);
        lowerArm2.add(elbow);


        // Agregar una pequeña sierra circular
        const sierraGeometry = new THREE.CylinderGeometry(0.2, 0.2, 0.04);
        const sierraMaterial = new THREE.MeshBasicMaterial({ color: 0x999999 });
        const sierra = new THREE.Mesh(sierraGeometry, sierraMaterial);
        sierra.name = 'sierra'; // Agregar un nombre al disco
        sierra.rotation.x = Math.PI / 2;
        sierra.position.set(-1.6, 1.04, 0.15);
        lowerArm4.add(sierra);

        // Obtener una referencia al botón de sierra
        const sierraButton = document.querySelector('a[href="?arriba1"]');
        const stopSierraButton = document.getElementById('stopSierraButton');

        // Obtener una referencia al disco de sierra
        const sierraObject = scene.getObjectByName('sierra');

        // Variable para controlar la animación del disco
        let animatingSierra = false;

        // Función para animar la rotación del disco
        function animateSierra() {
            if (animatingSierra) {
                requestAnimationFrame(animateSierra);
                sierraObject.rotation.y += 0.1; // Ajusta la velocidad de rotación según tus necesidades
            }
        }

        // Event listener para el botón de sierra
        sierraButton.addEventListener('click', (event) => {
            event.preventDefault(); // Evitar que el enlace se siga

            // Alternar la animación del disco
            animatingSierra = !animatingSierra;

            if (animatingSierra) {
                animateSierra();
            }
        });

        // Event listener para detener la sierra
        stopSierraButton.addEventListener('click', () => {
            animatingSierra = false;
        });

        // Agregar un material que haga alusión al motorreductor de la sierra
        const motorreductor0Geometry = new THREE.CylinderGeometry(0.1, 0.1, 0.25, 32);
        const motorreductor0Material = new THREE.MeshBasicMaterial({ color: 0x787878 });
        const motorreductor0 = new THREE.Mesh(motorreductor0Geometry, motorreductor0Material);
        motorreductor0.rotation.x = Math.PI /2;
        motorreductor0.rotation.y = Math.PI / 2;
        motorreductor0.position.set(-1.6, 1.04, 0.45);
        lowerArm4.add(motorreductor0); // Agregar el motorreductor0 al brazo extra

        // Agregar un material que haga alusión a los motoreductorreductores de las ruedas
        const motorreductorGeometry = new THREE.CylinderGeometry(0.15, 0.15, 0.4);
        const motorreductorMaterial = new THREE.MeshBasicMaterial({ color: 0xFFFB0C });
        const motorreductor = new THREE.Mesh(motorreductorGeometry, motorreductorMaterial);
        const motorreductor2 = new THREE.Mesh(motorreductorGeometry, motorreductorMaterial);
        motorreductor.rotation.z = Math.PI/2;
        motorreductor.position.set(-0.25, -0.45, 0.45);
        motorreductor2.rotation.z = Math.PI / 2;
        motorreductor2.position.set(-0.25, -0.45, -0.45);
        base.add(motorreductor);
        base.add(motorreductor2); // Agregar el motorreductor a la base



        let elbowMaterial = new THREE.MeshBasicMaterial({ color: 0x7F6000 });
        geometry = new THREE.BoxGeometry(0.05, a3 * 1.18, 0.06);
        let arm = new THREE.Mesh(geometry, elbowMaterial);
        let arm2 = new THREE.Mesh(geometry, elbowMaterial);

        geometry = new THREE.BoxGeometry(0.05, (a3*1.18)/1.5, 0.06);
        arm3 = new THREE.Mesh(geometry, elbowMaterial);
        arm3.position.set(0, -0.5, 0.6);
        arm3.translateY(a3 / 1.44);
        elbow.add(arm3);

        // Agregar los nuevos joint
        let joint3 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.2), new THREE.MeshBasicMaterial({ color: 0xFDED4A }));
        joint3.position.setY(a3 / 1.8);
        arm2.add(joint3);

        let joint4 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.8), new THREE.MeshBasicMaterial({ color: 0xFDED4A }));
        joint4.position.setY(a3 / 1.8);
        arm.add(joint4);

        let joint5 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.45), new THREE.MeshBasicMaterial({ color: 0x808080 }));
        joint5.position.setY(a3 / -3);
        joint5.position.setZ(a3 / -10);
        arm3.add(joint5);

        arm.position.set(0, -0.5, 0.3);
        arm2.position.set(0, -0.5, 0);

        arm.translateY(a3 / 2);
        arm2.translateY(a3 / 2);
        elbow.add(arm);
        elbow.add(arm2);



        let wrist = new THREE.Object3D();
        wrist.translateY(a3 / 2);
        arm.add(wrist);





        // Geometría de la pieza adicional
        const geometriaPiezaAdicional = new THREE.BoxGeometry(0.1, 0.7, 0.05);
        // Material de la pieza adicional
        const materialPiezaAdicional = new THREE.MeshBasicMaterial({ color: 0x7F6000 });
        const piezaAdicional = new THREE.Mesh(geometriaPiezaAdicional, materialPiezaAdicional);
        // Establecer rotación solo en Z
        piezaAdicional.rotation.x = 0;
        piezaAdicional.rotation.y = 2.74;
        piezaAdicional.rotation.z = -(3 * Math.PI) / 3.85; // 135 grados en radianes
        piezaAdicional.position.set(-0.2, 0.9, 0.1);
        scene.add(piezaAdicional);

        let baseCuadradaGeometry = new THREE.BoxGeometry(1.7, 0.1, 1.2);
        let baseCuadradaMaterial = new THREE.MeshBasicMaterial({ color: 0xBF9000 });
        const baseCuadrada = new THREE.Mesh(baseCuadradaGeometry, baseCuadradaMaterial);
        baseCuadrada.position.set(0.1, -0.3, 0);
        base.add(baseCuadrada);

        const ruedaGrandeFrenteGeometry = new THREE.CylinderGeometry(0.35, 0.35, 0.2, 12);
        const ruedaGrandeFrenteMaterial = new THREE.MeshBasicMaterial({ color: 0x312E2E });
        const ruedaGrandeFrente = new THREE.Mesh(ruedaGrandeFrenteGeometry, ruedaGrandeFrenteMaterial);
        ruedaGrandeFrente.name = 'ruedaGrandeFrente'; // Agregar un nombre a la rueda delantera
        ruedaGrandeFrente.rotation.x = Math.PI / 2;
        ruedaGrandeFrente.position.set(-0.1, -0.2, -0.7);
        baseCuadrada.add(ruedaGrandeFrente);

        const ruedaGrandeAtrasGeometry = new THREE.CylinderGeometry(0.35, 0.35, 0.2, 12);
        const ruedaGrandeAtrasMaterial = new THREE.MeshBasicMaterial({ color: 0x312E2E });
        const ruedaGrandeAtras = new THREE.Mesh(ruedaGrandeAtrasGeometry, ruedaGrandeAtrasMaterial);
        ruedaGrandeAtras.name = 'ruedaGrandeAtras'; // Agregar un nombre a la rueda trasera
        ruedaGrandeAtras.rotation.x = Math.PI / 2;
        ruedaGrandeAtras.position.set(-0.1, -0.2, 0.7);
        baseCuadrada.add(ruedaGrandeAtras);

        // Obtener referencias a las ruedas grandes
        const ruedaGrandeFrenteObject = scene.getObjectByName('ruedaGrandeFrente');
        const ruedaGrandeAtrasObject = scene.getObjectByName('ruedaGrandeAtras');

        // Variables para controlar la dirección y velocidad de las ruedas
        let direccionRuedas = 0; // 0: detenidas, 1: adelante, -1: atrás
        let velocidadRuedas = 0.1; // Ajusta la velocidad según tus necesidades

        // Función para mover las ruedas
        function moverRuedas() {
            requestAnimationFrame(moverRuedas);

            // Rotar las ruedas según la dirección
            if (direccionRuedas === 1) {
                ruedaGrandeFrenteObject.rotation.y += velocidadRuedas;
                ruedaGrandeAtrasObject.rotation.y += velocidadRuedas;
            } else if (direccionRuedas === -1) {
                ruedaGrandeFrenteObject.rotation.y -= velocidadRuedas;
                ruedaGrandeAtrasObject.rotation.y -= velocidadRuedas;
            }
        }

        // Iniciar la animación de las ruedas
        moverRuedas();

        // Event listeners para los botones
        const adelanteButton = document.querySelector('a[href="?adelante"]');
        const atrasButton = document.querySelector('a[href="?atras"]');

        adelanteButton.addEventListener('click', (event) => {
            event.preventDefault();
            direccionRuedas = 1;
        });

        atrasButton.addEventListener('click', (event) => {
            event.preventDefault();
            direccionRuedas = -1;
        });


        const ruedaDelgadaGeometry = new THREE.CylinderGeometry(0.25, 0.25, 0.25, 100);
        const ruedaDelgadaMaterial = new THREE.MeshBasicMaterial({ color: 0x444444 });
        const ruedaDelgada = new THREE.Mesh(ruedaDelgadaGeometry, ruedaDelgadaMaterial);
        ruedaDelgada.rotation.x = Math.PI / 2;
        ruedaDelgada.rotation.z = Math.PI / 0.5;
        ruedaDelgada.position.set(0.8, -0.27, 0);
        baseCuadrada.add(ruedaDelgada);

        //Contorno amarillo de las ruedas grandes y contorno gris de la delgada
        const ruedaGrandeFrenteGeometry2 = new THREE.CylinderGeometry(0.25, 0.25, 0.1, 32);
        const ruedaGrandeFrenteMaterial2 = new THREE.MeshBasicMaterial({ color: 0xFFFB0C });
        const ruedaGrandeAmr1 = new THREE.Mesh(ruedaGrandeFrenteGeometry2, ruedaGrandeFrenteMaterial2);
        ruedaGrandeAmr1.rotation.x = Math.PI / 2;
        ruedaGrandeAmr1.position.set(-0.1, -0.2, -0.8);
        baseCuadrada.add(ruedaGrandeAmr1);

        const ruedaGrandeFrenteGeometry3 = new THREE.CylinderGeometry(0.25, 0.25, 0.1, 32);
        const ruedaGrandeFrenteMaterial3 = new THREE.MeshBasicMaterial({ color: 0xFFFB0C });
        const ruedaGrandeAmr2 = new THREE.Mesh(ruedaGrandeFrenteGeometry3, ruedaGrandeFrenteMaterial3);
        ruedaGrandeAmr2.rotation.x = Math.PI / 2;
        ruedaGrandeAmr2.position.set(-0.1, -0.2, 0.8);
        baseCuadrada.add(ruedaGrandeAmr2);

        const ruedaDelgadaGeometry2 = new THREE.CylinderGeometry(0.15, 0.15, 0.35, 100);
        const ruedaDelgadaMaterial2 = new THREE.MeshBasicMaterial({ color: 0x999897 });
        const ruedaDelgadaGrs = new THREE.Mesh(ruedaDelgadaGeometry2, ruedaDelgadaMaterial2);
        ruedaDelgadaGrs.rotation.x = Math.PI / 2;
        ruedaDelgadaGrs.rotation.z = Math.PI / 0.5;
        ruedaDelgadaGrs.position.set(0.8, -0.27, 0);
        baseCuadrada.add(ruedaDelgadaGrs);


  




        // Definir dos puntos para la curva de Bezier
        const P0 = new THREE.Vector3(a2, a1 / 2, -a3);
        const P1 = new THREE.Vector3(a2, a1 / 2, a3);
        var t = 0;



        // Comenzar el bucle de animación
        animate();

        function animate() {
            requestAnimationFrame(animate);

            // Calcular la cinemática inversa y actualizar las posiciones del brazo
            let th1p, th2p, th3p, R;
            R = bezier2(P0, P1, t);
            [th1p, th2p, th3p] = inv_kin(R);
            // Recorrer el parámetro de la curva de Bezier
            if (t <= 1) {
                t = t + 0.01;
            } else {
                t = 0;
            }
            // Establecer una posición inicial estática para el brazo
            base.rotation.y = -0.4; // Ángulo de rotación inicial para la base
            shoulder.rotation.z = Math.PI / 3.5; // Ángulo de rotación inicial para el hombro
            elbow.rotation.z = Math.PI / 2; // Ángulo de rotación inicial para el codo





            // R_camara = bezier2(P0_camara, P1_camara, t_camara); // Comentar estas líneas
            // camera.position.copy(R_camara); // para mantener la cámara fija
            // camera.lookAt(0, 0, 0);
            // if (t_camara <= 1) {
            //     t_camara = t_camara + 0.00033;
            // } else {
            //     t_camara = 0;
            // }

            updateCamera(); // Actualizar la posición de la cámara

            renderer.render(scene, camera);
        }

// Función para actualizar la posición de la cámara
function updateCamera() {
    // Actualizar la posición objetivo de la cámara
    targetX = mouseX * .001; // Reducir la sensibilidad del movimiento horizontal
    targetY = mouseY * .001; // Reducir la sensibilidad del movimiento vertical

    // Suavizar el movimiento de la cámara
    camera.position.x += (targetX - camera.position.x) * 0.05; // Ajustar el factor de suavizado
    camera.position.y += (targetY - camera.position.y) * 0.05; // Ajustar el factor de suavizado

    // Establecer una distancia mínima desde el centro de la escena
    const minDistance = 3.5; // Ajustar esta distancia según tus necesidades
    const cameraDistance = Math.sqrt(camera.position.x ** 2 + camera.position.y ** 2 + camera.position.z ** 2);
    if (cameraDistance < minDistance) {
        camera.position.setLength(minDistance);
    }

    // Apuntar la cámara al centro de la escena
    camera.lookAt(0, 0.5, 0);
}

        // Agregar eventos de mouse para controlar la cámara
        renderer.domElement.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
        });

        // Función para calcular la cinemática inversa
        function inv_kin(P) {
            const x03 = -P.x;
            const z03 = P.y;
            const y03 = P.z;
            const th1 = Math.atan2(y03, x03);
            const r1 = Math.sqrt(x03 * 2 + y03 * 2);
            const r2 = -(z03 - a1);
            const phi2 = Math.atan2(r2, r1);
            const r3 = Math.sqrt(r1 * 2 + r2 * 2);
            const phi1 = Math.acos((a3 * 2 - a2 * 2 - r3 ** 2) / (-2 * a2 * r3));
            const th2 = phi2 - phi1;
            const phi3 = Math.acos((r3 * 2 - a2 * 2 - a3 ** 2) / (-2 * a2 * a3));
            const th3 = Math.PI - phi3;
            return [th1, th2, th3];
        }

        // Función para interpolación de Bezier entre dos puntos
        function bezier2(P0, P1, t) {
            const R = P0.clone().multiplyScalar(1 - t).add(P1.clone().multiplyScalar(t));
            return R;
        }


        // Obtener referencias a los botones
        const arriba2Button = document.querySelector('a[href="?arriba2"]');
        const abajo2Button = document.querySelector('a[href="?abajo2"]');

        // Obtener referencias a los materiales que se moverán
        const armMOV = [arm, arm2, arm3];
        const lowerArmMOV = [lowerArm, lowerArm2, lowerArm3, lowerArm4];

        // Event listener para el botón "?arriba2"
        arriba2Button.addEventListener('click', (event) => {
        event.preventDefault();
        
        // Cambiar el ángulo de inclinación de los materiales correspondientes
        for (let material of armMOV) {
            material.rotation.z = -0.3;
        }
        
        for (let material of lowerArmMOV) {
            material.rotation.z = -0.4; // 90 grados en radianes
        }
        });

        // Event listener para el botón "?abajo2"
        abajo2Button.addEventListener('click', (event) => {
        event.preventDefault();
        
        // Cambiar el ángulo de inclinación de los materiales correspondientes
        for (let material of armMOV) {
            material.rotation.z = 0.1; // 90 grados en radianes
        }
        
        for (let material of lowerArmMOV) {
            material.rotation.z = 0.2;
        }
        });



// Obtener referencia al botón "?bailar"
const bailarButton = document.querySelector('a[href="?bailar"]');

// Función para alternar entre "?arriba2", la posición inicial y "?abajo2"
function alternarPosiciones() {
  let intervalo = setInterval(() => {
    // Activar funcionalidad del botón "?arriba2"
    for (let material of armMOV) {
      material.rotation.z = -0.3;
    }
    for (let material of lowerArmMOV) {
      material.rotation.z = -0.4;
    }

    setTimeout(() => {
      // Posición inicial de los materiales
      for (let material of armMOV) {
        material.rotation.z = 0;
      }
      for (let material of lowerArmMOV) {
        material.rotation.z = 0;
      }
    }, 500); // Cambiar a la posición inicial después de 0.5 segundos

    setTimeout(() => {
      // Activar funcionalidad del botón "?abajo2"
      for (let material of armMOV) {
        material.rotation.z = 0.1;
      }
      for (let material of lowerArmMOV) {
        material.rotation.z = 0.2;
      }
    }, 1000); // Cambiar a la posición "?abajo2" después de 1 segundo
  }, 1500); // Repetir cada 1.5 segundos

  // Detener el intervalo después de 500 segundos
  setTimeout(() => {
    clearInterval(intervalo);
  }, 500000);
}

// Función para activar todas las funcionalidades
function activarFuncionalidades() {
  // Activar funcionalidad del botón "?arriba1" (animación de la sierra)
  animatingSierra = true;
  animateSierra();

  // Activar funcionalidad de los botones de movimiento de ruedas
  direccionRuedas = 1; // Adelante
  setTimeout(() => {
    direccionRuedas = -1; // Atrás
  }, 2000); // Cambiar la dirección después de 2 segundos

  // Llamar a la función alternarPosiciones
  alternarPosiciones();
}

// Event listener para el botón "?bailar"
bailarButton.addEventListener('click', (event) => {
  event.preventDefault();
  activarFuncionalidades();
});

    </script>
</body>
</html>
"

///2)Códgo para el funcionamiento del brazo real en python:
"
from machine import Pin, PWM
from time import sleep
import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
import socket
from machine import Pin
import utime
from machine import Pin, I2C
import ssd1306
import math

L11 = Pin(19, Pin.OUT)
L12 = Pin(18, Pin.OUT)
L21 = Pin(17, Pin.OUT)
L22 = Pin(16, Pin.OUT)
servo1 = Pin(13, Pin.OUT)
servo2 = Pin(12, Pin.OUT)
motor_pin1 = Pin(20, Pin.OUT) # Por ejemplo, GPIO 6
motor_pin2 = Pin(21, Pin.OUT)

# Configuración del I2C para la pantalla OLED
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# Inicialización de la pantalla OLED (128x64)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Valores iniciales para las ruedas
velocidad_rueda_derecha = 0
velocidad_rueda_izquierda = 0
nivel_bateria = 100

v_i = 0
v_d = 0

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid = 'moto_g52'
pw = 'mateus07'

wlan.connect(ssid, pw)



# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)


    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed ',wlan_status)
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# pantalla

# Función para dibujar un círculo
def dibujar_circulo(oled, x0, y0, radio):
    x = radio
    y = 0
    err = 0

    while x >= y:
        oled.pixel(x0 - x, y0 - y, 1)
        oled.pixel(x0 - y, y0 - x, 1)
        oled.pixel(x0 + y, y0 - x, 1)
        oled.pixel(x0 + x, y0 - y, 1)
        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

# Función para dibujar una línea desde el centro del velocímetro
def dibujar_lineas(oled, x0, y0, length, angle):
    x1 = int(x0 + length * math.cos(math.radians(angle)))
    y1 = int(y0 + length * math.sin(math.radians(angle)))
    oled.line(x0, y0, x1, y1, 1)
    
def lineas_cortas(oled, x0, y0, radio_interior, radio_exterior, angle):
    x1 = int(x0 + radio_interior * math.cos(math.radians(angle)))
    y1 = int(y0 + radio_interior * math.sin(math.radians(angle)))
    x2 = int(x0 + radio_exterior * math.cos(math.radians(angle)))
    y2 = int(y0 + radio_exterior * math.sin(math.radians(angle)))
    oled.line(x1, y1, x2, y2, 1)

# Función para dibujar la batería
def dibujar_bateria(oled, x, y, ancho, altura, level):
    # Dibujar el contorno de la batería
    oled.rect(x, y, ancho, altura, 1)  # Contorno de la batería
    oled.rect(x + ancho, y + altura//4, 2, altura//2, 1)  # Terminal positivo
    
    # Dibujar el nivel de la batería
    inner_width = int((ancho - 2) * level / 100)
    oled.fill_rect(x + 1, y + 1, inner_width, altura - 2, 1)

# Función para mostrar el velocímetro
def mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria):
    oled.fill(0)  # Limpiar la pantalla
    
    # Dibujar el velocímetro
    centro_x, centro_y = 96, 32
    radio = 30
    
    dibujar_circulo(oled, centro_x, centro_y, radio)
    
    # Dibujar las líneas del velocímetro
    angulos = [-150, -120, -90, -60, -30]
    for angulo in angulos:
        lineas_cortas(oled, centro_x, centro_y, radio - 8, radio, angulo)
     
    # Dibujar líneas de referencia del velocímetro
    lineas_cortas(oled, centro_x, centro_y, 0, radio-25, 90)
    lineas_cortas(oled, 67, centro_y, 0, radio-25, 90)
    lineas_cortas(oled, 123, centro_y, 0, radio-25, 90)

    # Dibujar la línea horizontal en la mitad del círculo
    oled.line(centro_x - radio, centro_y, centro_x + radio, centro_y, 1)
    
    # Dibujar las agujas del velocímetro
    angulo_derecha = 180 + (180 * velocidad_rueda_derecha / 100)
    angulo_izquierda = 180 + (180 * velocidad_rueda_izquierda / 100)
    
    # Aguja para la rueda derecha
    dibujar_lineas(oled, centro_x, centro_y, radio-1, angulo_derecha)
    
    # Aguja para la rueda izquierda (más corta)
    dibujar_lineas(oled, centro_x, centro_y, radio - 10, angulo_izquierda)
    
    # Dibujar la batería
    dibujar_bateria(oled, 0, 0, 20, 10, nivel_bateria)
    
    oled.show()  # Actualizar la pantalla OLED con los dibujos
   
    # Porcentaje batería
    oled.text('%'+str(nivel_bateria), 25, 3)
    
    # Valores referencia velocímetro
    oled.text('0', 65, 40)
    oled.text('50', 85, 40)
    oled.text('100', 105, 40)
    
    # Mostrar los valores de las ruedas
    oled.text('R.D:', 0, 40)
    oled.text(str(velocidad_rueda_derecha), 30, 40)
    oled.text('R.I:', 0, 50)
    oled.text(str(velocidad_rueda_izquierda), 30, 50)
    
    oled.show()


# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(1)

print('Listening on', addr)
led = machine.Pin('LED', machine.Pin.OUT)

# Listen for connections
while True:
    try:
#         pantalla
        L11.value(0)
        L12.value(0)
        L21.value(0)
        L22.value(0)

        motor_pin1.value(0)
        motor_pin2.value(0)
        velocidad_rueda_derecha = v_d
        velocidad_rueda_izquierda = v_i
        nivel_bateria = 90

        mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
        
#         pantalla

        cl, addr = s.accept()
        print('Client connected from', addr)
        r = cl.recv(1024)
        # print(r)
        
        r = str(r)
        adelante = r.find('?adelante')
        atras = r.find('?atras')
        derecha = r.find('?derecha')
        izquierda = r.find('?izquierda')
        baile = r.find('?bailar')
        arriba1 = r.find('?arriba1')
        arriba2 = r.find('?arriba2')
        abajo1 = r.find('?abajo1')
        abajo2 = r.find('?abajo2')
        


        if adelante > -1:
            print('adelante')
            led.value(1)
            L11.value(0)
            L12.value(1)
            L21.value(0)
            L22.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            
            
              
        if atras > -1:
            print('atras')
            led.value(1)
            L11.value(0)
            L12.value(1)
            L22.value(0)
            L21.value(1)
            led.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)

            
        if derecha > -1:
            print('derecha')
            led.value(1)
            L11.value(0)
            L12.value(1)
            L21.value(1)
            L22.value(0)
            led.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
           
            
        if izquierda > -1:
            print('izquierda')
            led.value(1)
            L11.value(1)
            L12.value(0)
            L21.value(0)
            L22.value(1)
            led.value(1)
            print(L11.value())
            print(L12.value())
            print(L21.value())
            print(L22.value())
            v_i += 10
            v_d += 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            time.sleep(0.2)
            led.value(0)
            L11.value(0)
            L12.value(0)
            L21.value(0)
            L22.value(0)
            led.value(0)
            v_i -= 10
            v_d -= 10
            velocidad_rueda_derecha = v_d
            velocidad_rueda_izquierda = v_i
            nivel_bateria = 90
            mostrar_velocimetro(velocidad_rueda_derecha, velocidad_rueda_izquierda, nivel_bateria)
            
            
        if baile > -1:
            print('Prendiendo motor')
            motor_pin1.value(1)
            motor_pin2.value(0)
            utime.sleep(1)      # Esperar 5 segundos
            print('Apagando motor')
            motor_pin1.value(0)
            motor_pin2.value(0)


            
        if arriba1 > -1:
            pwm = PWM(servo1)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 7
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            

        if arriba2 > -1:
            pwm = PWM(servo2)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 2
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            
               
        if abajo1 > -1:
            pwm = PWM(servo1)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 2
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            
        if abajo2 > -1:
            pwm = PWM(servo2)
            pwm.freq(50) 
            duty_cycle = 3
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            duty_cycle = 7
            pwm.duty_u16(int(65535 * duty_cycle / 100))
            utime.sleep(1)
            pwm.deinit()
            
        response = get_html('web_server_cube.html')
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')

# Make GET request
#request = requests.get('http://www.google.com')
#print(request.content)
#request.close()

"


///3)Código de control remoto en html: 
"
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="utf-8">
    <title>Mi primera aplicación three.js</title>
    <style>
        body { margin: 0; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/three@0.126.1/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.126.1/examples/js/controls/OrbitControls.js"></script>
	<style>
			button {
	            padding: 10px 20px;
	            font-size: 16px;
	            margin: 5px;
	            border-radius: 10px;
	            border: none;
	            cursor: pointer;
	            background-color: #ddd;
	        }
	        /* Estilos para la disposición de los botones */
	        .button-row {
	            display: flex;
	            justify-content: center;
	            align-items: center; /* Centra verticalmente */
	            margin-bottom: 10px; /* Agrega un espacio entre las filas de botones */
	        }
		</style>
</head>
<body>
        <!-- Contenedor para el gráfico 3D -->
        <div id="arm"></div>
        <div id="error"></div>

       <!-- Descripción de la funcionalidad 
        <p>Control the onboard LED</p>-->
        
   

		
		<h1>Control de Carro</h1>

		<!-- Div para agrupar los botones en una fila -->
		<div class="button-row">
			<!-- Botón para mover hacia arriba con flecha hacia arriba -->
			<a href="?adelante"><button>&#8593;</button></a>
		</div>
	
		<!-- Div para agrupar los botones en una fila -->
		<div class="button-row">
			<!-- Botón para mover hacia la izquierda con flecha hacia la izquierda -->
			<a href="?izquierda"><button>&#8592;</button></a>
	
			<!-- Botón para mover hacia abajo con flecha hacia abajo -->
			<a href="?atras"><button>&#8595;</button></a>
	
			<!-- Botón para mover hacia la derecha con flecha hacia la derecha -->
			<a href="?derecha"><button>&#8594;</button></a>
		</div>

		<!-- Botón de baile -->
		<div class="button-row">
			<a href="?bailar"><button>¡Bailar!</button></a>
		</div>

		<!-- Botones brazo -->
		<div class="button-row">
			<a href="?arriba1"><button>&#8593;</button></a>
			<a href="?arriba2"><button>&#8593;</button></a>
		</div>

		<!-- Botones de flechas hacia abajo -->
		<div class="button-row">
			<a href="?abajo1"><button>&#8595;</button></a>
			<a href="?abajo2"><button>&#8595;</button></a>
		</div>


<script>
    // Configurar la escena y la cámara de Three.js
const width = window.innerWidth;
const height = window.innerHeight / 2;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
camera.position.x = 8; // Mover la cámara más lejos
camera.position.y = 5; // Mover la cámara más lejos
camera.position.z = 8; // Mover la cámara más lejos
camera.lookAt(0, 0, 0);

    // Inicializar controles de la cámara
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    const arm_DOM = document.getElementById("arm");
    arm_DOM.appendChild(renderer.domElement);
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enablePan = false; // Deshabilitar el movimiento de panorámica
    controls.enableZoom = false; // Deshabilitar el zoom

    // Variables para el control de la cámara
    let mouseX = 10;
    let mouseY = -10;
    let targetX = 20;
    let targetY = 30;

    // Definir un punto en el espacio 3D
    const point = new THREE.Vector3();

    // Establecer el color inicial del LED y las dimensiones del brazo
    let color_led = 0x00fff0;
    const a1 = 1;
    const a2 = 1.5;
    const a3 = 1.5;

    // Definir un pequeño punto para la visualización
    let dot = new THREE.BoxGeometry(0.01, 0.01, 0.01);

    // Configurar la base del brazo mecánico
    let geometry = new THREE.BoxGeometry(0.8, a1/2, 0.6);
    let material = new THREE.MeshBasicMaterial({ color: 0x7F6000 });
    const base = new THREE.Mesh(geometry, material);
    base.translateY(a1 / 2);
    scene.add(base);

    // Crear estructura jerárquica para los segmentos del brazo
    let shoulder = new THREE.Object3D();
    shoulder.translateY(a1 / 4);
    base.add(shoulder);

    geometry = new THREE.BoxGeometry(0.1, a2, 0.06);
    let lowerArm = new THREE.Mesh(geometry, material);
    let lowerArm2 = new THREE.Mesh(geometry, material);
    let lowerArm3 = new THREE.Mesh(geometry, material);
    let lowerArm4 = new THREE.Mesh(geometry, material);

    lowerArm.position.set(0, 0, 0.15);
    lowerArm2.position.set(0, 0, -0.15);
    lowerArm3.position.set(0.5, 0, 0.15);
    lowerArm4.position.set(0.5, 0, -0.15);

    lowerArm.translateY(a2 / 2);
    lowerArm2.translateY(a2 / 2);
    lowerArm3.translateY(a2 / 2);
    lowerArm4.translateY(a2 / 2);
    shoulder.add(lowerArm);
    shoulder.add(lowerArm2);
    shoulder.add(lowerArm3);
    shoulder.add(lowerArm4);

    geometry = new THREE.BoxGeometry(0.03, 0.03, 0.3);
    let joint = new THREE.Mesh(geometry, material);
    let joint2 = new THREE.Mesh(geometry, material);
    joint.position.setY(a2 / 2);
    joint2.position.setY(a2 / 2);
    lowerArm.add(joint);
    lowerArm2.add(joint2);

    let elbow = new THREE.Object3D();
    elbow.translateY(a2 / 2);
    lowerArm.add(elbow);

    let elbowMaterial = new THREE.MeshBasicMaterial({ color: 0x7F6000 });
    geometry = new THREE.BoxGeometry(0.05, a3*1.18, 0.06);
    let arm = new THREE.Mesh(geometry, elbowMaterial);
    let arm2 = new THREE.Mesh(geometry, elbowMaterial);

    arm.position.set(0, -0.5, 0);
    arm2.position.set(0, -0.5, -0.3);

    arm.translateY(a3 / 2);
    arm2.translateY(a3 / 2);
    elbow.add(arm);
    elbow.add(arm2);

    let wrist = new THREE.Object3D();
    wrist.translateY(a3 / 2);
    arm.add(wrist);

    geometry = new THREE.TorusGeometry(0.2, 0.02, 6, 7, 6);
    let hand = new THREE.Mesh(geometry, material);
    hand.rotation.y = Math.PI/3;
    hand.rotation.x = Math.PI / 1.85;
    wrist.add(hand);

    hand.position.set(0.05, 0.22, -0.15);

    let baseCuadradaGeometry = new THREE.BoxGeometry(1.5, 0.2, 1);
    let baseCuadradaMaterial = new THREE.MeshBasicMaterial({ color: 0xBF9000 });
    const baseCuadrada = new THREE.Mesh(baseCuadradaGeometry, baseCuadradaMaterial);
    baseCuadrada.position.setY(-0.3);
    base.add(baseCuadrada);
  
    const ruedaGrandeFrenteGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.2, 32);
    const ruedaGrandeFrenteMaterial = new THREE.MeshBasicMaterial({ color: 0x312E2E });
    const ruedaGrandeFrente = new THREE.Mesh(ruedaGrandeFrenteGeometry, ruedaGrandeFrenteMaterial);
    ruedaGrandeFrente.rotation.x = Math.PI / 2;
    ruedaGrandeFrente.position.set(0, -0.18, -0.6);
    baseCuadrada.add(ruedaGrandeFrente);

    const ruedaGrandeAtrasGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.2, 32);
    const ruedaGrandeAtrasMaterial = new THREE.MeshBasicMaterial({ color: 0x312E2E });
    const ruedaGrandeAtras = new THREE.Mesh(ruedaGrandeAtrasGeometry, ruedaGrandeAtrasMaterial);
    ruedaGrandeAtras.rotation.x = Math.PI / 2;
    ruedaGrandeAtras.position.set(0, -0.18, 0.6);
    baseCuadrada.add(ruedaGrandeAtras);

const ruedaDelgadaGeometry = new THREE.CylinderGeometry(0.18, 0.18, 0.1, 100);
const ruedaDelgadaMaterial = new THREE.MeshBasicMaterial({ color: 0x444444 });
const ruedaDelgada = new THREE.Mesh(ruedaDelgadaGeometry, ruedaDelgadaMaterial);
ruedaDelgada.rotation.x = Math.PI / 2;
ruedaDelgada.rotation.z = Math.PI/0.5 ;
ruedaDelgada.position.set(-0.8, -0.2, 0);
baseCuadrada.add(ruedaDelgada);





// Definir dos puntos para la curva de Bezier
const P0 = new THREE.Vector3(a2, a1 / 2, -a3);
const P1 = new THREE.Vector3(a2, a1 / 2, a3);
var t = 0;



// Comenzar el bucle de animación
animate();

function animate() {
    requestAnimationFrame(animate);

    // Calcular la cinemática inversa y actualizar las posiciones del brazo
    let th1p, th2p, th3p, R;
    R = bezier2(P0, P1, t);
    [th1p, th2p, th3p] = inv_kin(R);
    // Recorrer el parámetro de la curva de Bezier
    if (t <= 1) {
        t = t + 0.01;
    } else {
        t = 0;
    }
// Establecer una posición inicial estática para el brazo
    base.rotation.y = -0.4; // Ángulo de rotación inicial para la base
    shoulder.rotation.z = Math.PI / 3.5; // Ángulo de rotación inicial para el hombro
    elbow.rotation.z = Math.PI / 2; // Ángulo de rotación inicial para el codo
   


   

    // R_camara = bezier2(P0_camara, P1_camara, t_camara); // Comentar estas líneas
    // camera.position.copy(R_camara); // para mantener la cámara fija
    // camera.lookAt(0, 0, 0);
    // if (t_camara <= 1) {
    //     t_camara = t_camara + 0.00033;
    // } else {
    //     t_camara = 0;
    // }

    updateCamera(); // Actualizar la posición de la cámara

    renderer.render(scene, camera);
}

// Función para actualizar la posición de la cámara
function updateCamera() {
    // Actualizar la posición objetivo de la cámara
    targetX = mouseX * .001; // Reducir la sensibilidad del movimiento horizontal
    targetY = mouseY * .001; // Reducir la sensibilidad del movimiento vertical

    // Suavizar el movimiento de la cámara
    camera.position.x += (targetX - camera.position.x) * 0.05; // Ajustar el factor de suavizado
    camera.position.y += (targetY - camera.position.y) * 0.05; // Ajustar el factor de suavizado

   // Establecer una distancia mínima desde el centro de la escena
    const minDistance = 3.5; // Ajustar esta distancia según tus necesidades
    const cameraDistance = Math.sqrt(camera.position.x ** 2 + camera.position.y ** 2 + camera.position.z ** 2);
    if (cameraDistance < minDistance) {
        camera.position.setLength(minDistance);
    }

    // Apuntar la cámara al centro de la escena
    camera.lookAt(0, 0.5, 0);	
}

// Agregar eventos de mouse para controlar la cámara
renderer.domElement.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
});

// Función para calcular la cinemática inversa
function inv_kin(P) {
    const x03 = -P.x;
    const z03 = P.y;
    const y03 = P.z;
    const th1 = Math.atan2(y03, x03);
    const r1 = Math.sqrt(x03 ** 2 + y03 ** 2);
    const r2 = -(z03 - a1);
    const phi2 = Math.atan2(r2, r1);
    const r3 = Math.sqrt(r1 ** 2 + r2 ** 2);
    const phi1 = Math.acos((a3 ** 2 - a2 ** 2 - r3 ** 2) / (-2 * a2 * r3));
    const th2 = phi2 - phi1;
    const phi3 = Math.acos((r3 ** 2 - a2 ** 2 - a3 ** 2) / (-2 * a2 * a3));
    const th3 = Math.PI - phi3;
    return [th1, th2, th3];
}

// Función para interpolación de Bezier entre dos puntos
function bezier2(P0, P1, t) {
    const R = P0.clone().multiplyScalar(1 - t).add(P1.clone().multiplyScalar(t));
    return R;
}

</script> 
</body>
</html>
"

///4)Póser de sustentación del proyecto: 

"

![Imágen P](https://github.com/JulianMontoya1901/PROYECO-FINAL/assets/159487872/9a4f9515-2671-4d5f-b478-23188b230022)


"
