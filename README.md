**If you want to see this repository in English, [click here](https://github.com/Pdddro28/K-O-M-R-A-D/blob/main/README_EN.md)**

``` Para mejor visualización, se recomienda ver el repositorio en la computadora ```

# WRO 2026 Future Engineers – LNM

<div align="center">
<img width="839" height="826" alt="WhatsApp Image 2026-06-19 at 11 43 02 PM" src="https://github.com/user-attachments/assets/f7fbb04b-66f2-47e6-98a5-c69e94db7eae" />
</div>

Bienvenidos al repositorio de GitHub del **Equipo LNM**, anteriormente conocido como Ars Machina, que compite en la categoría **World Robot Olympiad™ (WRO®) Future Engineers 2026**. Nuestro equipo está formado por David Wang y Pedro Catamo que han diseñado un vehículo autónomo compacto e innovador para hacer frente a los retos dinámicos de la competición WRO 2026.

El Equipo
====

<div align="center">
	
<img width="1280" height="720" alt="Team_pic (1)" src="https://github.com/user-attachments/assets/156c3c29-799e-44e6-a7f0-629da61873b8" />

</div>

- ### Miembros:

	- **David Wang**
   
		Nacido en: 01/04/2011 (15 años)

		Estudio: 3º año en la U.E.C. Eduardo Blanco

  		Gmail: davidwangwu104@gmail.com
  	  
	- **Pedro Catamo**
   
 	  	Nacido en: 28/01/2009 (17 años)
   
   		Estudio: 5º año en la U.E.C. Eduardo Blanco
   
   		Gmail: pedrocatamo.2009@gmail.com

 - ### Coach:

	- **Jesús Alcalá**
   
  		Nacido en: 18/11/2005 (21 Años)
   
   		Estudio: Ingenieria en computación & Ingenieria informática
   
   		Gmail: Jdam50002@gmail.com

Foto del carro
====

<div align="center">

<img width="1060" height="1080" alt="604003001-cc130bf0-8547-48cc-847e-28dbd9029fba" src="https://github.com/user-attachments/assets/f1dc12a1-dbfc-46f3-9a21-a679aa1aa3db" />

</div>

Estructura de carpetas
====

Esta es la estructura de carpetas de nuestro repositorio:

```
LNM/
├── models/
├── schemes/
├── src/
├── t-photos/
├── v-photos/
└── video/

```

Donde:

- `models`: Todos los archivos 3D utilizados en el coche. [ver](./models/README.md)
- `schemes`: Esquema de cableado, instrucciones de montaje y descripción de los componentes. [ver](./schemes/README.md)
- `src`: Todo el código necesario para controlar el robot. [ver](./src/README.md) 
- `t-photos`: Fotos del equipo. [ver](./t-photos/README.md)
- `v-photos`: Fotos del vehículo. [ver](./v-photos/README.md)
- `videos`: Vídeos de las actuaciones del robot. [ver](./videos/README.md)

# 1- Mobilidad y diseño

- ### Diseños anteriores:
  
<div align="center">
	
| Foto | Nombre | Descripción |
|---|---|---|
| <img width="920" height="920" alt="Captura de pantalla 2026-06-17 185504" src="https://github.com/user-attachments/assets/36166165-a542-42d6-a771-41a60693a399" /> | **Cyber Cooper** | Teníamos pensado diseñar el coche desde cero, modelando e imprimiendo nuestras propias piezas en 3D, incluidos el chasis y el sistema de dirección. Aunque al principio parecía una buena idea, a medida que avanzábamos empezamos a encontrarnos con un problema tras otro, y nos dimos cuenta de que nuestro diseño actual nos acarrearía más dificultades. Al final, hicimos todo lo que pudimos dentro de las limitaciones de tiempo que teníamos, y este fue el vehículo que presentamos en la WRO 2024. |
| <img width="920" height="920" alt="front2" src="https://github.com/user-attachments/assets/ce130237-cc0b-4aa9-a620-0aea287408c2" /> | **Cooper** | Desarrollamos un chasis de PLA naranja estructurado en dos niveles impreso gracias a nuestro patrocinador Fab Lab Caracas. El nivel inferior albergaba los sensores y la electrónica de bajo nivel, mientras que el superior sostenía las baterías y la Raspberry Pi 3 para optimizar el espacio. Aunque logramos un gran avance estético y funcional, sufrimos lecciones duras en pista: el peso hizo que los acoples de la transmisión trasera flexarany tuviera problemas severos de fricción mecánica entre las piezas impresas en plástico. |
| <img width="920" height="920" alt="front" src="https://github.com/user-attachments/assets/804b3d7f-3500-4351-a917-ccf781029804" /> | **Halbi** | Teniendo en cuenta los recursos de los que disponíamos en ese momento, nuestra idea principal era rediseñar el Cybercooper, modificando la base y la estrategia existentes y utilizando mejores componentes electrónicos; empezamos a imprimir las nuevas piezas con material blanco y a pensar en mejores formas de montar el sistema de dirección del coche. Al final, decidimos utilizar una base prefabricada para el chasis; la razón principal fue ahorrar tiempo (y dolores de cabeza) con el diseño mecánico, lo que nos permitía dedicar más tiempo a la electrónica y la programación. |
| <img width="920" height="920" alt="WhatsApp Image 2026-06-18 at 7 39 40 PM" src="https://github.com/user-attachments/assets/ca9f62ff-7b8b-452a-97de-95ebf12dc0ef" /> | **The Fridge** | A diferencia de los modelos anteriores que pertenecían a nuestro coach, "The Fridge" fue un diseño construido enteramente por nosotros. Aquí dimos el salto a la geometría Ackermann e imprimimos la gran mayoría de las piezas en 3D. A nivel motriz, usamos un motor DC con un engranaje acoplado para traccionar ambas ruedas. Físicamente le instalamos 3 sensores ultrasónicos, una Raspberry Pi 4 y un giroscopio MPU6050, pero por falta de tiempo y severos problemas de configuración, la Raspberry y el IMU quedaron como peso muerto y terminamos controlando todo únicamente desde la MegaPi. Sufrimos muchísimo: las piezas de la dirección impresas en 3D se rompían constantemente por el estrés, y programar la navegación autónoma en Arduino dependiendo de puros rebotes ultrasónicos fue casi imposible. Siendo sinceros, terminó siendo el peor proyecto de los tres. |

</div>

 - ### Halbi The Green:

    - ### Foto:

	<div align="center">

	
	| Superior | Derecha | Izquierda | Frontal | Trasero |
	|---|---|---|---|---|
	| <img width="1360" height="1380" alt="Upper-Pov" src="https://github.com/user-attachments/assets/74863cc8-5128-49cf-845e-0f087c50bcf1" /> | <img width="1360" height="1380" alt="RightSide-Pov" src="https://github.com/user-attachments/assets/8b9c2020-cc18-441f-9152-c86d9a233b10" /> | <img width="1360" height="1380" alt="LeftSide-Pov" src="https://github.com/user-attachments/assets/cdbabe27-6e45-4dab-98e6-e63b24ed7371" /> | <img width="1360" height="1380" alt="Front-Pov" src="https://github.com/user-attachments/assets/d9b65dd5-ca97-4087-ba20-77f7cbeb4bf6" /> | <img width="1360" height="1380" alt="Back-Pov" src="https://github.com/user-attachments/assets/dd1737be-1173-4cae-9229-25821f05dc22" /> |

    </div>

	- ### Especificaciones mecánicas principales:

		- **Dimensiones totales: 24.4 cm (largo) × 15.4 cm (ancho) × 15.9 cm (alto).**
		- **Peso del carro: aproximadamente 1,2Kg.**
		- **Sistema de tracción: Tracción Trasera Mecánica Bifásica.**
		- **Sistema de dirección: Geometría Ackermann.**
	
	- ### Mecanismo de Dirección Ackermann

		El vehículo utiliza una geometría precisa basada en el **Principio de Dirección Ackermann** para conquistar curvas cerradas con cero deslizamiento lateral y un desgaste mínimo de los neumáticos.

		* **La Física Detrás del Principio:** Cuando un vehículo entra en una curva, la rueda delantera interior sigue un radio concéntrico más cerrado y pequeño que la rueda exterior. Si ambas ruedas giraran exactamente al mismo ángulo, los neumáticos lucharían entre sí, provocando que el neumático exterior se arrastre, pierda agarre mecánico e introduzca vibraciones estructurales severas que arruinarían el seguimiento visual de los carriles. Para resolver esto, la geometría mecánica obliga a la rueda interior a pivotar a un ángulo más profundo que la rueda exterior, asegurando que las cuatro ruedas roten alrededor de un único centro instantáneo de curvatura (ICC) común.

		* **La Ejecución Mecánica:** Un servo digital **MG996R** de alto par ($11 \text{ kg}\cdot\text{cm}$ de par) se ancla al mamparo delantero mediante un soporte de aluminio en forma de L mecanizado a medida para eliminar la deflexión estructural. El brazo del servo acciona una cremallera de dirección de doble enlace conectada a tirantes asimétricos y manguetas de dirección. Los brazos de dirección están angulados hacia el interior, apuntando al centro del eje trasero, completando el clásico "Trapezoide de Ackermann". Este diseño mecánico exacto convierte el desplazamiento lineal del servo en ángulos de rueda no lineales de forma automática.

		* **El Control Digital y Calibración:** El MG996R es controlado por un tren de pulsos PWM por hardware continuo y libre de fluctuaciones (*jitter*) a $50\text{Hz}$ directamente desde el microcontrolador MegaPi. La dirección está rígidamente mapeada y calibrada a una banda muerta de software donde los $80^\circ$ representan el centro geométrico absoluto. Los puntos finales mecánicos están limitados por software entre $40^\circ$ (Máximo Izquierda) y $105^\circ$ (Máximo Derecha) para evitar que los eslabones de la dirección alcancen un bloqueo mecánico o fuercen los límites de pérdida del motor.

	- ### ¿Qué es la Geometría Ackermann? 

		Entendiendo la Matemática y Cinemática Ackermann, en robótica móvil tradicional (como los robots de la categoría *RoboMission*), se utiliza la tracción diferencial porque es matemáticamente simple: varías la velocidad de dos motores y el robot gira sobre su propio eje. Sin embargo, a altas velocidades, la tracción diferencial es inestable e impredecible.

		**La Geometría Ackermann** resuelve esto mediante un principio puramente mecánico. Para que un vehículo gire sin deslizarse lateralmente, las líneas extendidas desde los ejes de todas las ruedas deben cruzarse en un único punto en el espacio: el **Centro Instantáneo de Rotación (CIR)** o ICC.

		La ecuación matemática fundamental que gobierna esta cinemática es:
		<div align="center">
	
		$$\cot(\theta_{\text{out}}) - \cot(\theta_{\text{in}}) = \frac{w}{L}$$
		
		</div>
		Donde:
		* $\theta_{\text{in}}$ es el ángulo de giro de la rueda interna.
		* $\theta_{\text{out}}$ es el ángulo de giro de la rueda externa.
		* $w$ es el ancho de la vía (*track width* o distancia entre las ruedas frontales).
		* $L$ es la batalla del carro (*wheelbase* o distancia entre el eje delantero y trasero).

		Dado que la cotangente crece más rápido a ángulos pequeños, esta relación obliga mecánicamente a que $\theta_{\text{in}} > \theta_{\text{out}}$ de forma automática en cualquier curva, abriendo el ángulo de la rueda exterior para que dibuje un círculo más grande.

		<div align="center">
  
		<img width="567" height="600" alt="17523247_203569336801744_2788986523412924047_n" src="https://github.com/user-attachments/assets/c36a271c-b45c-492a-805e-b107851429cd" />
		
		</div>

	- ### Propulsión Electrónica 2WD con Transmisión Mecánica Bifásica 

		La fuerza motriz de la plataforma se genera mediante un sistema de tracción trasera (2WD) de alto rendimiento, el cual rompe con los esquemas tradicionales de acoplamiento directo al integrar una transmisión mecánica desmultiplicada de dos velocidades por engranajes cilíndricos rectos.

		* **Arquitectura del Sistema de Transmisión:** A diferencia de las configuraciones comunes que acoplan la rueda directamente a la caja reductora del motor, este diseño monta el motor RS380 en una disposición paralela superior sobre un bloque de soporte rígido. La potencia se transfiere desde el eje primario del motor hacia un eje secundario de tracción inferior mediante un tren de engranajes expuesto con dentado recto. Este sistema de dos velocidades mecánicas intercambiables permite configurar el robot según las exigencias de la pista:
  		1. **Relación de Fuerza/Torque (Primera Velocidad):** Optimiza el desmultiplique para obtener la máxima aceleración y un control milimétrico en curvas cerradas u obstáculos, ideal para tramos revirados. 
  		2. **Relación de Velocidad Final (Segunda Velocidad):** Reduce la pérdida de revoluciones para aprovechar la inercia lineal en rectas largas, garantizando una alta velocidad de crucero sin saturar el consumo eléctrico.

		<div align="center">
  
		<img width="515" height="218" alt="Sistema de transmision de 2 velocidades K-O-M-R-A-D" src="https://github.com/user-attachments/assets/da8175e6-313d-42d6-bd3b-b1318082536f" />
		
		</div>

		* **Especificaciones Técnicas de los Motores (RS380):** El bloque motriz confía en motores de CC con escobillas imantadas, seleccionados específicamente por su curva de respuesta dinámica y tolerancia a picos transitorios de carga.

	    * **Voltaje Nominal:** $12\text{V}$ (Operando a un voltaje nominal de celda de $11.1\text{V}$ mediante una batería LiPo 3S para asegurar la estabilidad térmica).
   
 		* **Corriente de Vacío (No-load):** $0.3\text{A}$ | **Corriente de Arranque/Pérdida (Stall):** $3\text{A}$ de protección en el driver.
   
 		* **Velocidad de Rotación de Fábrica:** $15000\text{ RPM}$ en el núcleo del motor, reducida internamente y ajustada finalmente por el engranaje externo para entregar una velocidad final estimada de transferencia de aprox. $450\text{ RPM}$ en el eje de la rueda.

		* **Análisis Cinemático y Cálculo de la Velocidad Teórica Absoluta:**
		Para determinar el rendimiento del chasis en pista y calibrar las ventanas de tiempo por vuelta (como el parámetro de control `lap_time = 4.3`), se realiza el cálculo cinemático basado en el diámetro de las ruedas motrices de $6.5\text{ cm}$ ($0.065\text{ m}$). Evaluamos la circunferencia de rodadura ($C$) y la velocidad lineal máxima teórica ($V$):

	<div align="center">
	
	$$C = \pi \times 0.065\text{ m} \approx 0.2041\text{ m}$$

	</div>

	Transformando las revoluciones por minuto del eje secundario de la transmisión a revoluciones por segundo y multiplicando por el desarrollo de la circunferencia, obtenemos la velocidad de avance del chasis:

	<div align="center">
	
	$$V = \frac{450\text{ RPM}}{60} \times 0.2041\text{ m} \approx 1.53\text{ m/s}$$
		
	</div>

	Este valor de $1.53\text{ m/s}$ representa la velocidad límite ideal de la plataforma. En condiciones reales de competencia, este vector se modula por software mediante los comandos de velocidad (`speed=90` u `80`) para absorber la fricción estática del suelo, la resistencia al avance de los rodamientos y las demandas instantáneas de corriente solicitadas por la MegaPi al gestionar el cambio de inercias.


	- ### 3D Printed Parts:

		- **Impresora:** Se usó las impresoras Creality Hi y Creality K1.

   			- **Creality Hi:** Es una de las propuestas más recientes de Creality, diseñada con un fuerte enfoque en competir directamente en el mercado de impresión multicolor accesible.
        
        		- Volumen de construcción (lo que puedes imprimir): $260 \times 260 \times 300\text{ mm}$. Es un tamaño intermedio-alto, excelente para robótica porque te permite hacer chasis completos en una sola pieza sin tener que segmentarlos.
            
          		- Dimensiones de la máquina: $409 \times 392 \times 477\text{ mm}$ (Peso: $8.75\text{ kg}$).
  
        		Es una impresora cartesiana de alta velocidad equipada con motores step-servo en los ejes X/Y para evitar la pérdida de pasos. Su gran fuerte es la compatibilidad nativa con el sistema CFS (Creality Filament System), un módulo externo tipo "banco de filamentos" que te permite alternar de forma automatizada hasta 4 colores diferentes (o hasta 16 si encadenas 4 módulos). Su velocidad máxima es de $500\text{ m/s}$ con una aceleración de $12,000\text{ mm/s}^2$ y alcanza los $300^\circ\text{C}$ en la boquilla.
  
        		- **¿Qué tan buena es?**
  
           			* **Puntos Fuertes:** Estructura de aluminio fundido extremadamente rígida, calibración y nivelación 100% automática por sensor de deformación, y detección inteligente de enredos o fin de filamento. Si compras la versión Combo (con el CFS), es una máquina brutal para piezas que necesitan soportes solubles o combinar materiales rígidos y flexibles.
  
       				* **Puntos Débiles:** Al no ser cerrada de fábrica (diseño abierto), imprimir materiales técnicos propensos a contraerse como el ABS o ASA de forma consistente puede ser complicado sin construirle una cabina externa.
          
	   			- **¿Se recomienda usarla a futuro?**
  
   					Sí, totalmente. Al ser una plataforma moderna, cuenta con el soporte de software más actualizado (Creality Print 5.1 / OrcaSlicer) y está diseñada bajo el ecosistema de cambio de filamento automático, que es hacia donde se mueve toda la industria. Es una excelente inversión a largo plazo para un taller.

			- **Creality K1:** Lanzada originalmente como la respuesta directa de Creality a la serie P1 de Bambu Lab, es una máquina de nivel profesional diseñada para velocidad pura y materiales exigentes.

     			- Volumen de construcción (lo que puedes imprimir): $220 \times 220 \times 250\text{ mm}$. Es un espacio estándar (ligeramente más pequeña que la Creality Hi).
        
    			- Dimensiones de la máquina: $355 \times 355 \times 480\text{ mm}$ (Peso: $12.5\text{ kg}$).
  
        		Utiliza un sistema cinemático CoreXY donde el cabezal se mueve de forma ultraligera en los ejes X/Y usando correas cruzadas, mientras la cama solo baja en el eje Z. Al estar completamente cerrada con paneles de vidrio y acrílico, retiene el calor interno en la cámara de impresión. Alcanza una velocidad de $600\text{ mm/s}$ y una aceleración masiva de $20,000\text{ mm/s}^2$ gracias a su firmware basado en Klipper (Creality OS).
  
   				- **¿Qué tan buena es?**
  
   					* **Puntos Fuertes:** Es una bestia para materiales técnicos. Su cámara cerrada es perfecta para imprimir PETG, ABS, ASA y Nylon sin sufrir warping (despegue de bordes). Su aceleración es casi el doble que la de la Creality Hi, reduciendo los tiempos de impresión de piezas mecánicas complejas drásticamente.
  
       				* **Puntos Débiles:** Las primeras unidades que salieron al mercado (lotes de 2023) sufrieron de problemas en el extrusor (versión V1) y en el hotend. Creality corrigió esto en las versiones posteriores (extrusor con palanca brillante y boquilla tipo Unicorn), por lo que si adquieres una hoy, te aseguras de tener la versión corregida y madura.
          
	   			- **¿Se recomienda usarla a futuro?**
  
   					Sí, pero bajo ciertas condiciones. Sigue siendo una máquina excepcionalmente rápida y robusta para piezas de ingeniería. Sin embargo, debes tener en cuenta que la K1 original no es compatible con sistemas de impresión multicolor multihilo modernos de manera nativa (esa característica se reservó para la serie K2 con el nuevo CFS).

		- #### **PETG vs PLA:**

		<div align="center">

		| Descripción | PETG | PLA |
		|---|---|---|
		| **¿Que és?** | El Polietileno Tereftalato Glicol (PETG) es un termoplástico derivado del petróleo, modificado con glicol para evitar la cristalización y fragilidad del PET común. Combina la facilidad de impresión del PLA con la resistencia mecánica del ABS. Se caracteriza por su excelente tenacidad, resistencia al desgaste químico y capacidad de absorber impactos mediante una ligera flexión elástica, lo que lo hace ideal para componentes funcionales. | El Ácido Poliláctico (PLA) es un termoplástico biodegradable de origen natural (derivado del almidón de maíz o caña de azúcar) ampliamente utilizado en impresión 3D por su facilidad de uso. Destaca por su alta rigidez estructural y mínima contracción térmica al enfriarse, lo que permite fabricar piezas con tolerancias geométricas muy precisas y sin deformaciones. Sin embargo, su naturaleza molecular lo hace frágil frente a impactos directos. |
		| **Características** | Presenta una alta resistencia al impacto y una notable resistencia a la fatiga mecánica. Cuenta con un módulo elástico que le otorga cierta flexibilidad estructural, permitiéndole soportar torsiones, vibraciones mecánicas y cargas dinámicas sin sufrir fracturas catastróficas. Es el material idóneo para piezas del robot expuestas a colisiones, fuerzas de tracción o movimientos mecánicos constantes. | Ofrece una excelente resistencia a la tracción y una rigidez mecánica superior, lo que significa que no se deforma ni se dobla fácilmente bajo cargas estáticas. Su principal desventaja es la fragilidad extrema; ante esfuerzos mecánicos bruscos o vibraciones continuas, tiende a fisurarse o quebrarse de forma repentina en lugar de flexionarse, limitando su uso en zonas de alta tensión dinámica. |
		| **Ventajas** | Destaca por una estabilidad térmica superior, soportando temperaturas de trabajo de hasta 75°C u 80°C sin perder su rigidez ni sufrir deformaciones estructurales. Esto permite colocarlo directamente junto a disipadores, motores DC o reguladores de voltaje. Además, posee propiedades hidrofóbicas y una alta resistencia química frente a alcoholes, aceites, grasas y a la degradación por exposición a la intemperie. | Posee una baja resistencia térmica, con un punto de ablandamiento (temperatura de transición vítrea) situado entre los 50°C y 55°C. Esto lo vuelve vulnerable a la deformación geométrica si se expone al calor disipado por motores de alta potencia o si el robot opera en entornos cálidos. Asimismo, su resistencia a la degradación por rayos UV y agentes químicos es limitada a largo plazo. |
		| **Desventajas** |  Exige condiciones de impresión más estrictas, con temperaturas de boquilla de 230°C a 250°C y cama caliente obligatoria entre 70°C y 90°C. Es propenso a generar hilos finos (stringing) y requiere un control riguroso de la humedad, ya que es altamente higroscópico y absorbe el agua del ambiente rápidamente, lo que degrada la calidad de la pieza si el filamento no se almacena en seco. | Es el material más sencillo de procesar en el taller de robótica, requiriendo temperaturas de boquilla bajas (190°C - 220°C) y una temperatura de cama moderada (50°C - 60°C) o incluso nula. No genera gases nocivos, no sufre de warping (despegue de bordes) y tolera altas velocidades de impresión con ventilación de capa al 100%, facilitando el prototipado rápido de piezas complejas. |
		| **Donde se utiliza** | Se utiliza de forma prioritaria en los componentes críticos sometidos a estrés físico y térmico. Es la elección correcta para parachoques frontales (bumpers) expuestos a colisiones, soportes para motores DC que generan calor por fricción, estructuras internas que sujetan baterías pesadas (soportando inercias bruscas al frenar o girar) y piezas móviles del varillaje del sistema de dirección. | Se aplica en la fabricación de componentes fijos que exigen máxima precisión dimensional y rigidez absoluta, donde las tolerancias geométricas de los encajes deban ser milimétricas. Es ideal para soportes de sensores ópticos o de líneas (que no deben oscilar), carcasas de cámaras de visión artificial, brackets de sujeción estáticos y maquetas de prueba donde el peso y el ajuste de tornillos sean críticos. |
	
		</div>

		- #### **Piezas:**

		<div align="center">
			
		| Component & Preview | Design & Geometry | Engineering Purpose |
		|---|---|---|
		| **Battery Case** <br><br><img width="400" height="400" alt="BatteryCase" src="https://github.com/user-attachments/assets/a5362844-dd0e-4073-bef8-bb034bae3ad9" /> | Diseñado como una jaula de torre vertical estructurada con cuatro pilares reforzados en cada lado, integrada directamente sobre una base de montaje sólida con ojales para tornillos en las esquinas. Las paredes laterales cuentan con grandes recortes circulares para minimizar el peso del material mientras permiten un flujo de aire pasivo máximo para evitar el estrés térmico en las celdas LiPo durante altas tasas de descarga. El pilar superior incluye ojales de retención ranurados para una sujeción segura de las correas. | Centraliza la masa combinada de las celdas de la batería verticalmente a lo largo del eje geométrico central del chasis. Este diseño de jaula abierta garantiza un acceso rápido para el reemplazo de la batería entre carreras, al tiempo que proporciona una contención estructural rígida contra las fuerzas de inercia laterales durante giros a alta velocidad. |
		| **Camera Case** <br><br><img width="400" height="400" alt="CameraCase" src="https://github.com/user-attachments/assets/7adbc42b-15eb-4677-a0a4-8d9b3c98bab3" /> | Una carcasa protectora rectangular y compacta, diseñada específicamente para encapsular el sensor IMX219 (Arducam). La sección inferior integra una robusta bisagra de pivote cilíndrico que cuenta con dientes de bloqueo externos (perfil de engranaje recto) diseñada para engranar perfectamente con una base de montaje correspondiente para el bloqueo mecánico del ángulo. | Protege el delicado PCB de la cámara de los escombros externos o de los impactos directos en la pista. La bisagra engranada entrelazada permite ajustar y bloquear mecánicamente el ángulo de inclinación de la cámara a un ángulo preciso de 15 grados hacia abajo, evitando cualquier cambio no deseado en el lente causado por las vibraciones de alta frecuencia del chasis durante la operación. |
		| **MegaPi Case** <br><br><img width="400" height="400" alt="MegaPiBase (1)" src="https://github.com/user-attachments/assets/8db95bf2-a29a-468c-ace8-e21bb1fae9f6" /> | Una bandeja robusta de perfil bajo equipada con cuatro soportes verticales integrados de alta resistencia posicionados en las esquinas para asegurar el PCB principal. La placa base cuenta con guías de distribución internas y cortes de holgura estructural para evitar los componentes en la parte inferior de la placa, manteniendo el perfil lo más cercano posible al chasis. | Funciona como una cuna mecánica rígida para la electrónica de potencia de bajo nivel. Al elevar el PCB mediante los soportes integrados de 3 mm, evita cortocircuitos eléctricos con el chasis al tiempo que amortigua las vibraciones. El perímetro completamente abierto garantiza el acceso inmediato a los terminales de tornillo del motor, los rieles de alimentación y los puertos de sensores para el mantenimiento en campo. |
		| **RaspberryPi Base** <br><br><img width="400" height="400" alt="RaspberryPiBase (1)" src="https://github.com/user-attachments/assets/2403b708-2e1d-4360-9504-aae68c0027d1" /> | Una plataforma modular plana de nivel medio que cuenta con cuatro soportes de esquina integrados para montar la Raspberry Pi 4 de forma segura. La sección frontal de la base integra un montaje de bisagra de doble oreja equipado con dientes de bloqueo internos que se acoplan directamente con la bisagra de la carcasa de la cámara (Camera Case). | Sirve como un puente estructural de doble propósito. Proporciona un montaje estable y elevado para la computadora de a bordo de alto nivel, asegurando una disipación óptima del calor a través de la convección natural para evitar el estrangulamiento térmico del CPU. Al mismo tiempo, su montaje engranado integrado bloquea firmemente el ensamblaje de la cámara en la parte delantera, eliminando la necesidad de componentes adicionales y ahorrando valioso espacio en el chasis.|
		| **Ultrasonic Case** <br><br><img width="400" height="400" alt="UltrasonicSensorCase" src="https://github.com/user-attachments/assets/f9696c40-13e6-46b5-9712-2d7849a80005" /> | Un soporte protector compacto de doble barril hecho a medida para encapsular firmemente los cilindros del transmisor y receptor del módulo del sensor ultrasónico. Cuenta con pestañas de montaje traseras integradas y bridas inferiores para un acoplamiento mecánico continuo a las vigas transversales delanteras de la estructura del chasis. | Proporciona una carcasa rígida y aislada de vibraciones que mantiene el sensor ultrasónico perfectamente perpendicular al plano horizontal de la pista. Esta alineación precisa elimina la distorsión de la señal acústica y la dispersión de las ondas, garantizando mediciones de distancia en tiempo real altamente precisas para la detección de obstáculos y mapas de frenado de emergencia. |

		</div>

# 2. Componentes

- ### Precios:

<div align="center">

| Cantidad | Productos | Precio | Total |
|---|---|---|---|
| 1 | [Raspberry Pi 4 B](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X) | $123.99 | $123.99 |
| 1 | [Yfrobot steering chassis](https://yfrobot.com/products/steering-gear-robot) | $118.50 | $118.50 |
| 2 | [Zeee 3S Lipo Battery 2200mAh 11.1V 50C](https://www.amazon.nl/Zeee-Vrachtwagen-Vliegtuig-Quadcopter-Helikopter/dp/B0C2CHMCC3) | $50.65 | $50.65 |
| 1 | [Arducam 8MP IMX219 175°](https://www.amazon.com/Arducam-IMX219-Degree-Raspberry-Compatible/dp/B09VSVB4DT/ref=sr_1_7?crid=10W18P0RVDUOR&s=electronics&sr=1-7) | $26.99 | $26.99 |
| 4 | [Lever wire connectors](https://www.amazon.com/Conductor-Compact-Connectors-Electrical-Terminals/dp/B0D9Y5XFQC/ref=sr_1_2_sspa?sr=8-2-spons) | $9.99 | $9.99|
| 1 | [Buck Converter 3A 15W Type-C](https://www.amazon.com/-/es/Convertidor-Impermeable-Adaptador-corriente-compatible/dp/B0D2MTJQK8) | $8.79 | $8.79 |
| 1 | [MAKEBLOCK MegaPi (from mbot mega)](https://www.robotshop.com/products/makeblock-mbot-mega-robot-car-rechargeable-li-po-battery-kit?qd=c181467e2368e663479ab211142e2920) | $148.97 | $148.97 |
| 1 | [Crash Collision Sensor Module](https://www.amazon.com/-/es/Generic-detecci%C3%B3n-colisi%C3%B3n-interruptor-Arduino/dp/B0D6GZDV95) | $5.54 | $5.54 |
| 1 | [LED Traffic Light Module](https://www.amazon.com/Traffic-Light-Module-Board-Arduino/dp/B07R1KJ4DT) | $10.99| $10.99 |
| | | | **$504.41** |

</div>

- ### Descripción:

<div align="center">

| Foto | Descripción |
|---|---|
| **Yfrobot kit** <div  align="center"> <div  style="width:290 px"> ![halbi](https://funduinoshop.com/media/image/84/6f/82/YFROBOT-chassis-kit-mit-lenkachse-technische-zeichnung_600x600@2x.png) </div> </div>  | El chasis modular YFROBOT 4WD combina tracción en las cuatro ruedas con un sistema de dirección tipo automóvil para ofrecer mayor estabilidad y un control preciso. Diseñado con soportes específicos para controladores como Arduino o Raspberry Pi, simplifica el ensamblaje mecánico y permite añadir sensores o accesorios fácilmente. Al reducir la complejidad del diseño desde cero, resulta una plataforma ideal en educación y competiciones para que los equipos se concentren directamente en la programación, la navegación autónoma y los sistemas de control. |
| **Raspberry PI 4 B** <div align="center"> <img width="293" height="172" alt="images" src="https://github.com/user-attachments/assets/5c007a1e-273e-4ce2-89a7-fa99dd9b069b" /> </div> | La Raspberry Pi 4 Modelo B es un potente ordenador de placa única (SBC) del tamaño de una tarjeta de crédito desarrollado por la Fundación Raspberry Pi. Se utiliza ampliamente en robótica, proyectos de IoT y 	sistemas embebidos debido a su versatilidad, rendimiento y precio asequible. |
| **Makeblock MegaPi** <div  align="center"> ![nano](https://ardubotics.eu/10754/makeblock-mega-pi-born-to-control.jpg) </div> | Se seleccionó la placa **Makeblock MegaPi** (**ATmega2560**) como microcontrolador central por su capacidad para gestionar múltiples motores y sensores simultáneamente, superando a opciones como Arduino Uno o Nano gracias a sus interfaces plug-and-play. Aunque está diseñada para acoplarse directamente sobre una Raspberry Pi, se optó por conectarla únicamente vía **USB** para la transferencia de datos. Esta alternativa optimiza el espacio del chasis, aprovecha que la MegaPi cuenta con alimentación propia y evita exponer la placa principal a riesgos durante el proceso de soldadura. |
| **Zeee 3S Lipo Battery 2200mAh 11.1V 50C** <div  align="center"> <div  style="width:290 px"> ![LX2-BUSB](https://m.media-amazon.com/images/I/71-SIfPk3XL._AC_UF1000,1000_QL80_.jpg) </div> | El robot utiliza una batería LiPo Zeee 3S (2200mAh, 11.1V, 50C) como fuente de energía única, elegida por su alta tasa de descarga y un diseño compacto que optimiza el espacio en el chasis frente a opciones más voluminosas. Esta configuración simplifica el sistema al alimentar tanto la lógica como los motores, aunque exige el uso de reguladores de voltaje externos (como convertidores CC-CC) para proteger componentes sensibles como la Raspberry Pi. A pesar de requerir un manejo cuidadoso con cargadores específicos para evitar riesgos y prolongar su vida útil, ofrece un balance excelente entre potencia, tamaño y rendimiento para aplicaciones robóticas. |
| **Steering servo mg996r** <div  align="center"> ![L298N](https://cdn-global-hk.hobbyking.com/media/catalog/product/cache/10/image/9df78eab33525d08d6e5fb8d27136e95/6/2/6221_1_high_7_.jpg) </div> | Incluido en el kit de YFROBOT para controlar el eje de dirección, el MG996R es un servomotor digital de alto torque que opera mediante señales PWM en un rango de 0° a 180°. Su piñonería metálica le otorga una mayor durabilidad y fuerza frente a los servos de plástico, permitiéndole soportar cargas mecánicas exigentes. Con un rango de operación de 4.8V a 6V, ofrece un torque de entre 9.4 y 11 kg·cm y velocidades de hasta 0.15 segundos por cada 60°, utilizando una interfaz estándar de tres pines totalmente compatible con microcontroladores como Arduino y Raspberry Pi. |
| **RS380 motor** <div  align="center"> ![motor](https://novatronicec.com/wp-content/uploads/2020/10/Motor-con-caja-reductora-25GA370_2.jpg) </div> | El conjunto de motor RS-380 con caja reductora es un sistema de corriente continua compacto y versátil, ideal para robótica pequeña y automatización ligera. Por sí solo, el RS-380 es un motor con escobillas de tamaño reducido que gira a altas revoluciones (entre 10 000 y más de 20 000 RPM según el voltaje) pero genera muy poco torque. La incorporación de la caja reductora soluciona esta limitación al disminuir la velocidad de giro mediante una serie de engranajes, lo que incrementa significativamente el torque de salida y permite al sistema mover cargas mecánicas más pesadas de manera práctica. |
| **ArduCam IMX219 8MP** <div  align="center"> ![Encorder](https://cdn.arducam.com/wp-content/uploads/2022/04/Arducam_IMX219_MIPI_Pi_B0392-8.jpg) </div> | La ArduCam IMX219 de 8MP es un módulo de cámara compacto basado en el sensor Sony IMX219, el mismo estándar de la Raspberry Pi Camera v2, que equilibra resolución y rendimiento para proyectos de visión artificial y robótica. Se conecta mediante la interfaz CSI (Camera Serial Interface), lo que garantiza una transferencia de datos a alta velocidad y con baja latencia hacia computadoras como Raspberry Pi o Jetson Nano. Este diseño la convierte en una solución eficiente y de fácil integración para sistemas embebidos que requieren procesamiento de imagen en tiempo real. |
| **Buck Converter 3A 15W Type-C** <div  align="center"> ![camera](https://m.media-amazon.com/images/I/61pOfxNxUnL._AC_UF1000,1000_QL80_.jpg) </div> | El módulo **convertidor buck tipo C de 3A y 15W** es un regulador reductor de CC-CC que transforma voltajes de entrada elevados en una salida baja y estable con una eficiencia del 85 al 95%. En este proyecto, se utilizó para conectar la batería **LiPo Zeee 3S** (de hasta 12.6V) a la **Raspberry Pi 4B**, la cual exige un suministro constante de **5V y hasta 3A**. Debido a que el voltaje directo de la batería dañaría la placa, el convertidor reduce y regula la tensión de manera segura, protegiendo los componentes contra sobrevoltajes, minimizando las pérdidas de energía por calor y garantizando un rendimiento estable del sistema a medida que la batería se descarga. |
| **Ultrasonic Sensor HC-SR04** <div  align="center"> <img width="466" height="466" alt="61CXJgLZwUL _SX466_" src="https://github.com/user-attachments/assets/1345b129-76f7-4f39-8ec2-b839398ea61b" /> </div> | El sensor ultrasónico HC-SR04 es un dispositivo compacto de medición de distancia que opera bajo el principio del eco de sonar, ideal para la evasión de obstáculos en robótica. Está equipado con dos transductores que emiten una ráfaga de ondas de alta frecuencia ($40\text{ kHz}$) y reciben su rebote tras chocar con un objeto. Al calcular con precisión el tiempo que tarda la señal en ir y venir, el módulo determina la distancia lineal en un rango efectivo de 2 a 400 centímetros con una precisión de 3 milímetros, proporcionando datos en tiempo real cruciales para la navegación del vehículo.|

</div>

- ### Disposición de Sensores y Justificación:

	El diseño de nuestro vehículo autónomo, K-O-M-R-A-D, se fundamenta en una arquitectura modular de dos niveles, optimizada para la gestión eficiente del centro de gravedad y la distribución de componentes electrónicos. Esta configuración en "pisos" permite una separación crítica entre la potencia (actuadores) y la lógica (procesamiento), facilitando tanto la estabilidad mecánica como el mantenimiento del sistema.

	- Arquitectura del Chasis:
	El chasis se organiza en una estructura vertical de dos niveles. En el nivel inferior se encuentra el núcleo motriz: la placa MegaPi, el motor de tracción DC y el servomotor de dirección. Esta base sólida garantiza que el tren de rodaje tenga un centro de gravedad bajo. Sobre este soporte se eleva una plataforma superior que actúa como el "cerebro" del vehículo, albergando la Raspberry Pi 4, los sistemas de gestión de energía y la base ajustable de la cámara, garantizando que el procesado de datos esté aislado de las vibraciones mecánicas generadas por la transmisión.

	- Sistema de Percepción:
 	Esta organización estructural complementa nuestro sistema de percepción mixto, compuesto por una cámara de visión artificial y tres sensores ultrasónicos, ubicados estratégicamente para cubrir los puntos críticos de navegación:

		- Distribución Frontal:
		En la parte delantera del nivel inferior, se ha colocado un sensor ultrasónico en una posición adelantada respecto a la cámara. Esta configuración permite una sincronización ideal: mientras la cámara procesa la información visual (detección de colores y líneas), el sensor ultrasónico frontal actúa como medida de seguridad de hardware en tiempo real, midiendo con exactitud la proximidad de obstáculos antes de ejecutar maniobras de frenado o evasión.

		- Distribución Lateral:
		Para el control y la estabilización, se integraron dos sensores ultrasónicos situados a cada costado del chasis, anclados firmemente al nivel inferior. Estos se encuentran posicionados longitudinalmente entre las ruedas delanteras y traseras, y alineados verticalmente a la altura del eje de las ruedas. Esta ubicación centralizada es fundamental: al mantener esta altura y posición respecto al centro de masas, se minimizan las perturbaciones causadas por el balanceo del chasis, permitiendo que el vehículo calcule de manera constante y simétrica la distancia hacia las paredes, manteniendo así una trayectoria recta, fluida y precisa.

<div  align="center">

<img width="1600" height="1200" alt="WhatsApp Image 2026-06-18 at 11 34 59 PM" src="https://github.com/user-attachments/assets/5bea7abe-f434-4bbd-9ce3-3c26d1443c42" />

</div>

- ### Batería:

	La Zeee 3S LiPo 11.1V 2200mAh 50C es una batería de polímero de litio de alto rendimiento, diseñada específicamente para entusiastas del radiocontrol (RC) que buscan un equilibrio óptimo entre peso, tamaño y potencia. Con una configuración de 3 celdas (3S) y un voltaje nominal de 11.1V, este componente proporciona la energía constante y agresiva necesaria para impulsar una amplia variedad de modelos, desde drones de carreras y aviones a escala hasta vehículos terrestres RC. Su capacidad de 2200mAh asegura un tiempo de juego o vuelo sumamente competitivo, permitiendo exprimir al máximo el rendimiento del motor sin añadir un peso excesivo que pueda comprometer la agilidad del modelo.

	El verdadero punto fuerte de esta batería radica en su tasa de descarga de 50C, lo que significa que es capaz de entregar picos de corriente elevados de forma segura cuando el acelerador lo demanda, garantizando aceleraciones explosivas y una respuesta inmediata a los mandos. Fabricada con materiales de alta calidad y una baja resistencia interna, la Zeee 3S destaca por su ciclo de vida 			prolongado y su estabilidad térmica durante un uso intensivo. Viene equipada habitualmente con conectores de alta conductividad (como el Deans T o XT60) y un conector de equilibrado JST-XH, lo que facilita tanto una carga segura celda por celda como una compatibilidad directa con la mayoría de los cargadores inteligentes del mercado.

- ### Presupuesto de Energía:

<div align="center">

| Componentes | Cantidad | Voltaje de Operación | Consumo Nominal/Pico | Consumo Total |
|---|---|---|---|---|
| **Raspberry Pi 4 B** | 1 | 5.0 V | 600 mA / 1250 mA | 1250 mA |
| **Arducam 8MP IMX219 (175°)** | 1 | 3.3 V (vía RPi) | 250 mA | 250 mA |
| **Makeblock MegaPi (Lógica)** | 1 | 5.0 V | 100 mA | 100 mA |
| **Sensores Ultrasonido HC-SR04** | 3 | 5.0 V | 15 mA (c/u) | 45 mA |
| **Módulo Sensor de Colisión (Crash)** | 1 | 5.0 V | 10 mA | 10 mA |
| **Módulo Semáforo LED (Traffic Light)** | 1 | 5.0 V | 30 mA | 30 mA |
| **Servomotor de Dirección MG996R** | 1 | 5.0 V - 6.0 V | 500 mA / 2500 mA (Stall) | 2500 mA |
| **Motor de Tracción RS380** | 1 | 7.2 V - 12.0 V | 1200 mA / 2000 mA (Stall) | 2000 mA |
| | | | | 6,185 mA (6.18 A) |

</div>

Para garantizar la estabilidad operativa de nuestro carro, hemos implementado una arquitectura de alimentación redundante mediante el uso de dos baterías independientes. Esta división es fundamental para proteger la integridad de nuestros sistemas:

- Circuito de Potencia: Una batería dedicada exclusivamente a la placa MegaPi, la cual gestiona los actuadores de alta demanda (el motor de tracción RS380 y el servomotor de dirección MG996R), además de los tres sensores ultrasónicos y el botón de inicio. Este aislamiento evita que las caídas de tensión (transitorios) provocadas por los arranques repentinos o el bloqueo de los motores afecten el procesado de datos.

- Circuito de Lógica y Visión: Una segunda batería independiente alimenta exclusivamente a la Raspberry Pi 4 y la cámara Arducam. Esta separación es crítica; al no compartir el bus de energía con los motores, eliminamos el riesgo de interferencia electromagnética (EMI) y picos de voltaje que podrían inducir ruido en la señal de video o, en el peor de los casos, provocar reinicios inesperados del sistema de visión artificial durante la competencia.

Esta configuración nos permite operar con la máxima seguridad, garantizando que, incluso bajo condiciones de estrés mecánico severo en la dirección y tracción, nuestro "cerebro" (Raspberry Pi) mantenga una alimentación constante y limpia para procesar la trayectoria con total precisión.

- ### Diagrama de Cableado:

<div align="center">

<img width="2960" height="1625" alt="L-N-M@1 25x" src="https://github.com/user-attachments/assets/13e15df3-6f13-4d22-9dfd-a9a075e6561c" />

</div>

# 3.  Software

- ### Utilidades:

	- Color Detector: Es una herramienta interactiva de calibración visual diseñada para segmentar y aislar colores específicos en tiempo real mediante el espacio de color LAB (Luminancia, A y B) y filtros de desenfoque gaussiano. El sistema captura el flujo de video de una Picamera2, aplica transformaciones morfológicas de erosión y dilatación para limpiar el ruido de la imagen, y genera una máscara binaria basada en umbrales máximos y mínimos ajustables por deslizadores en una interfaz gráfica (GUI) construida con CustomTkinter. Su función principal es preajustar firmas de color (como rojo, verde, azul o negro) y exportar estos rangos óptimos a un archivo de configuración JSON para que el robot pueda reconocer objetos o líneas de manera 	estable bajo diferentes condiciones de luz.

	- ROI Detector: Es una utilidad de configuración espacial basada en OpenCV que permite delimitar "Regiones de Interés" (ROI) personalizadas sobre la transmisión de video de la cámara mediante clics y arrastres del mouse. El script escala el fotograma original de forma proporcional dentro de un lienzo centrado con bordes negros constantes, permitiendo al usuario dibujar múltiples cuadrantes, visualizando dinámicamente sus dimensiones en píxeles. Su propósito principal es limpiar la memoria caché con la tecla 'C' o finalizar la captura con la tecla 'ESC' para activar una ventana flotante de Tkinter que exporta de forma automatizada las coordenadas $(x_1, y_1, x_2, y_2)$ estructuradas como una lista de objetos en un archivo nativo de Python (.py), aislando las zonas específicas de análisis visual donde el robot debe procesar la información (como la línea del suelo) e ignorando el ruido del entorno.

- ### MegaPiController:

	Esta es una descripción completa de todos los atributos y métodos de la clase, junto con sus argumentos. Te recomendamos que la consultes primero antes de pasar a las demás secciones y que, cuando clones el repositorio, la utilices como guía para orientarte en nuestro código.

  	### MegaPiController.ino (class Carro)

	**Dependencies**

	- ```MeMegaPi.h```

	- ```Servo.h```

	- ```Adafruit_MPU6050.h (Optional / Commented)```

	- ```Ultrasonic.h```

	- ```Wire.h```

	#### Description of the constructor method

	```
	Carro() : motorTraccion(PORT4B) {}
	```

	El constructor inicializa la representación de bajo nivel del hardware del vehículo autónomo. Vincula explícitamente el motor de tracción de corriente continua RS380 de alto rendimiento a la ranura física del puente en H de alta potencia PORT4B de la placa Makeblock MegaPi.

	#### Descripción del atributo

	| Atributo | Tipo de datos | Funcionalidad|
	|---|---|---|
	| ```motorTraccion``` | ```MeMegaPiDCMotor``` | Objeto de la biblioteca Makeblock que se utiliza para regular el ciclo de trabajo del PWM y el vector de rotación del motor de tracción de corriente continua trasero. |
	| ```servoDireccion```  | ```Servo``` | Objeto Servo estándar de Arduino que maneja el tren de pulsos PWM de hardware ($50\text{Hz}$) para controlar la posición del servomotor de dirección Ackermann delantero MG996R. |

	#### Descripción de métodos:

	| Método | Parámetros | Retorno | Descripción |
	|---|---|---|---|
	| ```inicializar()``` | Ninguno | void | Configura los recursos de hardware: activa la resistencia de pull-up interna para el botón de inicio, acopla el servo de dirección al pin A7 y fuerza su alineación física al centro geométrico (90°). |
	| ```botonPresionado()```	| Ninguno | bool | Realiza una lectura digital en el botón de ejecución principal (A9). Devuelve true si el botón está físicamente presionado (estado LOW debido a la resistencia pull-up interna). |
	| ```obtenerDistancia()``` | trig: int, echo: int	long | Genera un pulso de disparo en bruto en los pines del sensor ultrasónico especificados y evalúa el tiempo de retroalimentación del eco. Devuelve automáticamente un umbral seguro de respaldo de 400 cm si está fuera de rango.|
	| ```getDistanciaFront()``` | Ninguno | long | Recupera la lectura de distancia actual en tiempo real en centímetros desde el conjunto del sensor ultrasónico delantero (sensorF). |
	| ```getDistanciaLeft()``` | Ninguno | long | Recupera la lectura de distancia actual en tiempo real en centímetros desde el sensor ultrasónico de orientación izquierdo (sensorL). |
	| ```getDistanciaRight()``` | Ninguno	| long | Recupera la lectura de distancia actual en tiempo real en centímetros desde el sensor ultrasónico de orientación derecho (sensorD). |
	| ```avanzar()``` | velocidad: byte | void | Mueve el tren motriz trasero hacia adelante a la intensidad PWM en bruto especificada e indicada por la interfaz del controlador de alto nivel. |
	| ```retroceder()``` | angulo: byte, velocidad: byte | void | Restablece momentáneamente las ruedas físicas a la alineación central, ajusta el servo de dirección a un vector de recuperación dado y asume la salida inversa del motor DC (-velocidad). |
	| ```girarIzquierda()``` | angulo: byte, velocidad: byte | void | Aplica el ángulo de dirección entrante al servo MG996R hacia el extremo físico izquierdo y proporciona tracción hacia adelante para navegar en curvas cerradas. |
	| ```girarDerecha()``` | angulo: byte, velocidad: byte | void	| Aplica el ángulo de dirección entrante al servo MG996R hacia el extremo físico derecho y proporciona tracción hacia adelante para navegar en curvas cerradas. |
	| ```detenerse()``` | Ninguno	| void | Corta de forma segura todos los suministros de voltaje que van al puente H del motor trasero (motor.stop()) e instantáneamente regresa el mecanismo de dirección al eje neutral. |
	| ```girarCentro()``` | Ninguno | void | Aísla el servo de dirección y fuerza su matriz de rotación directamente al centro predeterminado (90°), sin modificar el estado de velocidad actual del motor de tracción. |

- ### Arduino Controller:

	- Open Challenge:

		- Estrategia:
  
		    Para cumplir con los desafíos del Open Challenge, se diseñó e implementó una arquitectura de software basada en un bucle de control de alta frecuencia, dividida en cuatro pilares estratégicos: Percepción Visual, Control de Trayectoria (PID), Navegación en Esquinas y Seguridad Activa.
		
		- ROIS:
 
    		Para optimizar el procesamiento computacional y evitar falsos positivos con el entorno, la cámara segmenta el espacio en dos ROIs laterales específicas (roi y roi2). Estas regiones buscan activamente las líneas negras que delimitan las paredes o carriles de la pista.

		- Contador de Loops:
 
   			Se procesa el área de los colores clave en los primeros instantes. Si se detecta un área mayor a un umbral crítico 200px de color naranja, el robot asume una orientación de giro a la derecha; si el color es azul, se configura para girar a la izquierda.

		- Diagrama de Flujo:

	- Obstacle Challenge:

		- Estrategia:
		
		- ROIS:

		- Contador de Loops:

		- Diagrama de Flujo:

# 4. Challenges

- ### Problemas de Hardware:

	**Objetivo:** Completar tres vueltas de forma autónoma en circuitos configurados dinámicamente.

	### Problemas de espaciamiento

	Durante el desarrollo temprano de *Halbi the Green*, se presentaron inconvenientes con respecto al posicionamiento de los componentes dentro del chasis base (sin modificar). Debido a que los componentes ocupaban más espacio del disponible, el problema se resolvió temporalmente fijándolos con cinta aislante. Aunque esto funcionó de forma provisional, no era una solución viable a largo plazo. 

	Por ello, se decidió implementar una serie de bases impresas en 3D pensadas para agregar **dos niveles adicionales** al vehículo y **tres soportes complementarios** (dos laterales y uno frontal) para ubicar los sensores de ultrasonido, los cuales originalmente no tenían un lugar asignado.

	De manera más específica, los problemas de espaciamiento y sus respectivas soluciones fueron los siguientes:

	* **Espacio ocupado por las baterías:** * *Problema:* Ocupaban demasiado volumen en el chasis y no dejaban espacio para ubicar los componentes de forma cómoda.

    	* *Solución:* Se les diseñó una base a medida para ubicarlas en el centro del robot y, sobre esta estructura, se construyó el piso superior.
       
	* **Anclaje de sensores de ultrasonido:** * *Problema:* No tenían puntos previstos para anclarlos al chasis original.

    * *Solución:* Se diseñaron 3 bases impresas que van adjuntas a 3 caras del chasis.
      
    * *Nota técnica:* Esta solución no fue del todo ideal, ya que estas bases sobresalen un poco de la estructura, causando atascamientos mecánicos cuando el vehículo pasa muy cerca de una esquina.
      
	* **Ubicación de la cámara y controlador:** * *Problema:* No había lugar físico para situar la cámara ni la placa de procesamiento.
  
    	* *Solución:* Sobre la base de las baterías se diseñó un soporte dedicado para la Raspberry Pi y la cámara. Esta última incluye una base con ángulo graduable para poder ajustar el punto de vista del lente de manera cómoda y precisa.

	### Problemas con las conexiones (Cableado)

	* **Problema:** Al tener cables sueltos y expuestos, estos se quedaban atascados constantemente con el entorno e incluso se llevaban por delante los obstáculos del circuito en algunas ocasiones.
  
	* **Solución:** Se reorganizaron por completo las conexiones para eliminar los bucles y partes sobresalientes del cableado.
  
- ### Problemas de Software:

	- a
