Aquí tienes una reestructuración completa, profunda y pedagógica del documento técnico, adaptada exactamente a las correcciones solicitadas por el jurado/profesor.

Se eliminó el tono excesivamente denso, se estructuró en los bloques obligatorios y se redactó de forma **didáctica** (ideal para que los nuevos integrantes del club de robótica lo entiendan a la primera), utilizando analogías claras y explicaciones paso a paso sin perder el rigor de ingeniería.

---

# Electromechanical Diagrams & System Architecture

Este documento detalla la arquitectura de nuestro vehículo autónomo de la categoría *Future Engineers*. El diseño está dividido en subsistemas modulares para que cualquier miembro del equipo pueda entender, replicar o mejorar la plataforma.

---

## 1. Mechanics (Mecánica y Geometría)

Para que un vehículo autónomo sea predecible en la pista, su comportamiento físico debe ser impecable. En lugar de utilizar una configuración diferencial clásica (tipo tanque), este diseño implementa las leyes de la física automotriz real sobre un chasis **YFROBOT 4WD modificado**.

### Sistema de Dirección: Principio de Ackermann

Cuando un vehículo toma una curva, las ruedas delanteras no giran en el mismo ángulo. La rueda interna dibuja un círculo más pequeño que la rueda externa. Si ambas giraran igual, el carro patinaría, perdería tracción y descalibraría los cálculos de navegación.

* **La Física:** La geometría de Ackermann asegura que las líneas perpendiculares trazadas desde los ejes de todas las ruedas se corten en un único punto central de rotación.
* **La Ejecución Mecánica:** Un servomotor digital **MG996R** (que aporta un torque de $11\text{ kg}\cdot\text{cm}$) se monta firmemente en un soporte en forma de L. Mediante varillas de dirección asimétricas y brazos de dirección (*rudder arms*), el servo empuja las ruedas de tal forma que la rueda interna siempre se orienta con un ángulo mayor que la externa de manera puramente mecánica.
* **El Control Electrónico:** La posición se mantiene estable gracias a una señal de hardware PWM constante a $50\text{ Hz}$ generada por la placa MegaPi, calibrando el centro exacto a 90°.

### Propulsión: Configuración Tracción Trasera (Electronic 4WD)

La fuerza motriz se genera mediante motores de corriente continua **RS380**, acoplados directamente al tren de rodaje.

* **Especificaciones del Motor RS380:**
* Voltaje nominal: $7.2\text{V} - 12\text{V}$
* Velocidad máxima sin carga: $\approx 15,000\text{ RPM}$ (reducida mediante caja de engranajes interna para ganar torque).
* Consumo de corriente: $1.5\text{A}$ en vacío / Hasta $10\text{A}$ en picos de arranque (*Stall Current*).


* **Cálculo de la Velocidad Promedio del Carro:**
Para calcular la velocidad teórica del vehículo ($v$), utilizamos el radio de las ruedas ($r = 0.0325\text{ m}$) y las RPM finales del motor bajo carga en la pista ($\omega \approx 300\text{ RPM}$ tras la reducción geométrica):
$$\omega_{\text{rad/s}} = 300 \times \frac{2\pi}{60} \approx 31.416\text{ rad/s}$$


$$v = \omega_{\text{rad/s}} \times r = 31.416 \times 0.0325 \approx 1.02\text{ m/s}$$


*Velocidad promedio real en pista:* Debido a pérdidas por fricción y peso total, la velocidad promedio controlada se establece en **$0.85\text{ m/s}$**, garantizando el balance óptimo entre tiempo de vuelta y capacidad de reacción de la cámara.

### Justificación de la Configuración y Desventajas

* **¿Por qué elegimos esta configuración?:** Replicar la conducción Ackermann con un motor de tracción trasera reduce drásticamente las oscilaciones violentas en las rectas (problema común en los carros que giran como tanques) y permite trazar curvas fluidas a alta velocidad, lo que es vital para que la cámara procese líneas estables.
* **Desventajas de no usar diferencial mecánico:** Al tener un eje de propulsión directo sin un diferencial mecánico (el componente que permite que una rueda gire más rápido que otra en las curvas), las ruedas traseras tienden a "pelear" entre sí en giros cerrados.
* **Solución por Software:** Para mitigar esto, el código aplica variaciones dinámicas en el ciclo de trabajo (*Duty Cycle*) de los motores mediante el puente H de la MegaPi en función del ángulo del servo de dirección, simulando un diferencial electrónico.

---

## 2. Electronics (Electrónica y Potencia)

El mayor enemigo de un robot autónomo son los reinicios inesperados causados por caídas de voltaje cuando los motores arrancan. Para resolver esto, diseñamos un sistema con aislamiento total de etapas de potencia y lógica.

### Diagrama General de Conexiones Completo

A continuación se detalla cómo interactúan la energía, el procesamiento de datos de alta velocidad y las señales de control en tiempo real:

```
              [ LiPo Pack A: 11.1V ]                 [ LiPo Pack B: 11.1V ]
                        │                                      │
                        ▼                                      ▼
             ┌─────────────────────┐                ┌─────────────────────┐
             │ Convertidor Buck    │                │ Switch de Potencia  │
             │ (15W / 5V @ 3A)     │                │ Directo             │
             └──────────┬──────────┘                └──────────┬──────────┘
                        │ (5V Limpios)                         │ (11.1V Crudos)
                        ▼                                      ▼
             ┌─────────────────────┐                ┌─────────────────────┐
             │   Raspberry Pi 4    │                │    MegaPi Board     │
             │  (Cerebro/OpenCV)   │                │ (Reflejos/Motores)  │
             └──────────┬──────────┘                └────┬───────────┬────┘
                        │                                │           │
              (MIPI)    │        (USB Serial)            │ (PWM)     │ (Líneas I/O)
              ┌─────────┘       ┌────────────┘           │           │
              ▼                 ▼                        ▼           ▼
       ┌────────────┐    ┌────────────┐           ┌────────────┐┌────────────┐
       │  Arducam   │    │  Conexión  │           │ Servo      ││ Tri-Array  │
       │   IMX219   │    │ UART/USB   │           │ MG996R y   ││ Ultrasonido│
       └────────────┘    └────────────┘           │ Motores DC ││  HC-SR04   │
                                                  └────────────┘└────────────┘
                        ▲                                            ▲
                        │                                            │
                        └──────────────────[ GND ]───────────────────┘
                                         (Masa Común)

```

### Power Supply System y Selección de Componentes

* **Batería Lógica (Pack A):** LiPo de 3 celdas ($11.1\text{V}$, $2200\text{mAh}$). Se conecta a un regulador conmutado (Buck) de alta eficiencia que reduce el voltaje a $5\text{V}$ estables a un máximo de $3\text{A}$. Elegimos esta opción porque la Raspberry Pi 4 es sumamente sensible; si el voltaje cae a $4.7\text{V}$, el procesador se ralentiza o corrompe el sistema operativo.
* **Batería de Potencia (Pack B):** LiPo de 3 celdas ($11.1\text{V}$, $2200\text{mAh}$). Se conecta directamente a la bornera de potencia de la MegaPi para alimentar el puente H integrado y el servo. Los picos de corriente se drenan de este Pack, dejando al Pack A intacto.

> **Regla de Oro de la Masa Común:** Aunque los voltajes positivos están separados, los cables negativos (GND) de ambas baterías y de todos los componentes están rígidamente unidos en un solo punto en la MegaPi. Sin esta referencia unificada de $0\text{V}$, las señales de control de los sensores y el servo flotarían, provocando lecturas fantasma o movimientos erráticos.

### Cálculo de Potencia y Autonomía

#### 1. Consumo Estimado del Sistema

* **Grupo Lógico (Raspberry Pi 4 + Arducam):** 
$$P_{\text{lógica}} = 5\text{V} \times 1.5\text{A} = 7.5\text{W}$$


* **Grupo de Potencia (MegaPi + Motores en marcha promedio + Servo actuando):** 
$$I_{\text{promedio}} \approx 1.8\text{A} \implies P_{\text{potencia}} = 11.1\text{V} \times 1.8\text{A} = 19.98\text{W}$$



#### 2. Duración de la Batería (Autonomía)

Asumiendo que utilizamos baterías de $2200\text{mAh}$ ($2.2\text{Ah}$) y aplicando un factor de seguridad del $80\%$ para no descargar las celdas LiPo por debajo de su límite seguro:

$$\text{Tiempo Lógica} = \frac{2.2\text{Ah} \times 0.8}{1.5\text{A}} \approx 1.17\text{ horas } (70\text{ minutos})$$

$$\text{Tiempo Potencia} = \frac{2.2\text{Ah} \times 0.8}{1.8\text{A}} \approx 0.97\text{ horas } (58\text{ minutos})$$

El robot puede operar en pruebas continuas durante aproximadamente **55 minutos** antes de requerir un cambio de baterías, superando con creces la duración estándar de una ronda de competencia.

---

## 3. 3D Description (Modelado y Estructura)

Para integrar todos los componentes sin comprometer el centro de masa, diseñamos piezas a medida utilizando software CAD e impresión 3D en filamento PLA.

### Desglose de Componentes Modelados

1. **Soporte de Dirección Elevado (Frontal):** Diseñado específicamente para anclar el servo MG996R de forma invertida. Esto eleva los varillajes mecánicos protegiéndolos de impactos directos contra las paredes de la pista.
2. **Mástil de Visión Ajustable (Cámara):** Una torre vertical que posiciona la Arducam IMX219 a una altura de $18\text{ cm}$ respecto al suelo, con un ángulo de inclinación fija de 25° hacia abajo. Esto maximiza el campo de visión, permitiendo ver la línea de la pista y los obstáculos a media distancia simultáneamente.
3. **Parachoques Técnico y Soporte de Sensores:** Una sola pieza rígida en el frente que cumple doble función: amortiguar colisiones y alojar el tri-array de ultrasonido en ángulos mecánicos exactos (Izquierdo: -45°, Centro: 0°, Derecho: 45°).
4. **Carcasa Protectora de Electrónica:** Caja ventilada montada en la parte trasera para proteger la Raspberry Pi 4 de virutas o golpes accidentales durante la manipulación en los talleres.

---

## 4. Space Distribution (Distribución Espacial)

El balance de pesos es crítico: un carro muy pesado atrás se levantará en las curvas; un carro muy pesado al frente perderá tracción en las ruedas motrices traseras.

### Distribución de Componentes en el Chasis

* **Planta Baja (Nivel del Suelo):** Alojamiento de los motores traseros RS380, la caja de engranajes y el servo de dirección delantero. Es la zona de menor altura para mantener el centro de gravedad lo más bajo posible.
* **Planta Intermedia (Distribución de Energía):** Las dos baterías LiPo de $2200\text{mAh}$ se colocan de forma longitudinal en el centro exacto del chasis. Esto concentra la masa pesada entre ambos ejes, reduciendo el momento de inercia y evitando derrapes. El interruptor general de encendido se ubica en el lateral izquierdo para un acceso de emergencia rápido.
* **Planta Alta (Procesamiento y Control):** * La **MegaPi** se sitúa directamente encima de las baterías para acortar los cables de los motores y el servo, minimizando el ruido electromagnético.
* La **Raspberry Pi 4** se monta sobre postes aislantes en la sección posterior alta, garantizando un flujo de aire óptimo para su refrigeración pasiva.


* **Periferia Extrema:** La cámara domina el punto más alto del frente, mientras que los tres sensores de ultrasonido sobresalen en el límite delantero del parachoques para evitar lecturas falsas causadas por la misma estructura del carro.

---

## 5. Considerations (Consideraciones y Mejoras Futuras)

Analizando los datos recolectados en las pruebas de pista, hemos proyectado las siguientes mejoras de ingeniería para la siguiente evolución del prototipo:

* **Migración a Comunicación Industrial Inter-Chip:** Actualmente, la comunicación entre la Raspberry Pi 4 y la MegaPi se realiza mediante un cable USB-Serial estándar. Aunque funciona, los conectores USB son propensos a aflojarse por las vibraciones de la pista. La mejora plantea conectar ambas placas directamente usando los pines del bus **SPI** o cables soldados a los puertos **UART** nativos de los GPIO, asegurando una conexión a prueba de vibraciones.
* **Reemplazo por Sensores de Distancia de Tiempo de Vuelo (ToF):** Los módulos ultrasónicos HC-SR04 tienen un cono de detección ancho ($\approx 15^{\circ}$), lo que a veces causa lecturas erráticas al rebotar contra esquinas anguladas. Cambiar estos sensores por módulos basados en láser **ToF (como el VL53L1X)** permitirá mediciones milimétricas con un haz de luz ultradelgado, optimizando las trayectorias de evasión.
* **Evolución del Chasis a Fibra de Carbono o Alumino Sándwich:** El chasis YFROBOT actual es de acrílico/plástico rígido, lo que añade peso muerto innecesario y es propenso a fisuras ante impactos severos. Sustituir las placas estructurales por fibra de carbono cortada por CNC reducirá el peso total del carro en un $35\%$, aumentando directamente la duración estimada de la batería y la aceleración de respuesta del sistema.
