Electromechanical System

Our autonomous vehicle splits its operational workload into two dedicated, coordinated subsystems: **The Mechanical Muscle** (chassis physics, Ackermann steering, and raw propulsion) and **The Electronic Brain** (distributed parallel processing and high-bandwidth sensor perception).

---

## 1. Mechanics (Chassis, Steering, and Propulsion)

To ensure stability at high speeds and predictable handling, the platform rejects tank-style differential spin turns and is built around true automotive physics using a modified **YFROBOT 4WD** chassis.

### Ackermann Steering Mechanism

The vehicle utilizes the **Ackermann Steering Principle** to conquer sharp cornering with minimal tire slip.

* **The Physics Behind It:** When cornering, the inner front wheel must follow a tighter radius than the outer wheel. To prevent the tires from scrubbing and losing grip, the wheels must pivot at different angles.
* **The Mechanical Execution:** An **MG996R** digital servo ($11 \text{ kg}\cdot\text{cm}$ torque) mounted onto an L-shaped aluminum bracket drives a system of mechanical linkages, steering arms, and asymmetrical tie rods. This geometry automatically forces the inner wheel to turn more sharply than the outer one.
* **The Digital Control:** Driven by continuous, jitter-free $50\text{Hz}$ hardware PWM pulses from the MegaPi board, keeping the steering stable at a rigidly calibrated center of $90^\circ$.

### Electronic 4WD Propulsion (Differential-Free)

Propulsion is delivered via a configuration of four **RS380** DC geared motors.

* **Motor Specifications (Per Unit):**
* Nominal Voltage: $12\text{V}$ (Operating at $11.1\text{V}$)
* No-load Current: $0.4\text{A}$ | Stall Current: $4.5\text{A}$
* No-load Speed: $15000\text{ RPM}$ (Output speed after gearbox: approx. $450\text{ RPM}$)


* **Average Vehicle Speed Calculation:**
With a wheel diameter of $6.5\text{ cm}$ ($0.065\text{ m}$), we calculate the wheel circumference ($C$) and the theoretical maximum velocity ($V$):

$$C = \pi \times 0.065\text{ m} \approx 0.2041\text{ m}$$


$$V = \frac{450\text{ RPM}}{60} \times 0.2041\text{ m} \approx 1.53\text{ m/s}$$



*The actual average speed on the track, accounting for friction losses and vehicle weight, is approximately **$1.2\text{ m/s}$**.*

### Configuration Analysis (Pros & Cons)

* **Reason for Selection:** By avoiding a heavy, bulky mechanical central differential, wheel speed coordination during turns is managed entirely in **software**. By applying varied Duty Cycles through the MegaPi's H-bridge drivers, the algorithm reduces power to the inner wheels during a turn so they do not fight each other.
* **Disadvantages:** Aggressive dynamic braking generates reverse currents (counter-electromotive force) that heat up the motor drivers if not dissipated properly. Additionally, lacking a physical differential limits raw mechanical traction if one wheel loses total contact with the track surface.

![Yfrobot Steering Chassis](https://yfrobot.com/cdn/shop/products/800-800_faf268ef-ce45-4bb0-930f-424f8070b6ff.jpg?v=1609730313&width=1445)

---

## 2. Electronics (Power System and Computational Control)

The most common issue in competition robotics is unexpected micro-controller resetting ("brownouts") caused by voltage drops when motors draw massive startup current. To solve this, the car completely isolates processing logic from inductive motor loads.

### Processing Workflow Redesign

To optimize performance and drastically reduce latency, high-level computer vision tasks and low-level real-time hardware execution run asynchronously:

```
                  ┌─────────────────────────────────────────┐
                  │       ARDUCAM IMX219 CAMERA (8 MP)      │
                  └────────────────────┬────────────────────┘
                                       │ Native MIPI CSI-2 Link (Low Noise)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │            RASPBERRY PI 4               │
                  │   - High-Level Computation Core         │
                  │   - RGB / BGR / LAB Image Segmentation  │
                  │   - OpenCV Vision Algorithm Pipeline    │
                  └────────────────────┬────────────────────┘
                                       │
                                       │ Isolated USB Serial Link (115200 baud)
                                       │ High-speed cinematic movement commands
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │             MAKEBLOCK MEGAPI            │
                  │   - ATmega2560 Microcontroller (16MHz)  │
                  │   - Real-Time Critical Interrupts Core  │
                  │   - Hardware PWM Generation for Motors  │
                  └────────────────────┬────────────────────┘
                                       │
             ┌─────────────────────────┴─────────────────────────┐
             ▼                                                   ▼
┌─────────────────────────┐                         ┌─────────────────────────┐
│    HC-SR04 SENSORS      │                         │ ACTUATORS & DC MOTORS   │
│ (Sequential Sampling)   │                         │  (H-Bridge Port Control)│
└─────────────────────────┘                         └─────────────────────────┘

```

### Power Supply System

| Power Source | System Group | Regulation Layer | Engineering Purpose |
| :--- | :--- | :--- | :--- |
| **LiPo Battery Pack A**<br>(11.1V - 3 Cells, 2200mAh) | Logic & Vision | **15W Type-C Buck Converter**<br>(Steps down to 5V $\pm$ 0.1V @ 3A) | Feeds the Raspberry Pi 4 with clean, linear power. Prevents voltage drops and SD card data corruption. |
| **LiPo Battery Pack B**<br>(11.1V - 3 Cells, 2200mAh) | Motors & Servo | **Direct Injected Rail**<br>(MegaPi Power Terminals) | Delivers massive current spikes demanded by the RS380 motors without dropping logic rails. |

### Electrical Calculations: Power and Battery Life
* **Total Required Power ($P_{\text{total}}$):**
  * *Stationary Logic Consumption:* The Raspberry Pi 4 draws approx. 1.2A @ 5V = 6W.
  * *Dynamic Power Consumption:* Four RS380 motors under race conditions draw an average of 1.5A each at 11.1V, and the MG996R servo averages 0.5A under continuous motion.
  $$I_{\text{power\_total}} = (4 \times 1.5\text{A}) + 0.5\text{A} = 6.5\text{A}$$
  $$P_{\text{power\_rail}} = 6.5\text{A} \times 11.1\text{V} = 72.15\text{W}$$
  $$P_{\text{total}} = 6\text{W} + 72.15\text{W} = \mathbf{78.15\text{W}}$$

* **Battery Autonomy Calculation:**
  Since the battery packs are rated at 2200mAh (2.2Ah) and applying a standard 20% safety margin to protect the LiPo cell chemistry (never discharging past 80%):
  $$\text{Runtime}_{\text{Logic}} = \frac{2.2\text{Ah} \times 0.8}{1.2\text{A}} \approx 1.46\text{ hours} \approx \mathbf{88\text{ minutes}}$$
  $$\text{Runtime}_{\text{Power}} = \frac{2.2\text{Ah} \times 0.8}{6.5\text{A}} \approx 0.27\text{ hours} \approx \mathbf{16.2\text{ minutes}}$$
  *The critical battery life during a race is dictated entirely by the motor power battery, guaranteeing **16 minutes of non-stop, high-demand running**.*

> **⚠️ The Golden Rule of Grounding:** Both batteries must share a unified **Common Ground (GND)** rail on the MegaPi board. Without this single 0V reference point, PWM control signals would float, creating devastating electromagnetic interference (EMI), corrupted ultrasonic readings, and erratic servo twitches.

<img width="2960" height="1625" alt="L-N-M@1 25x" src="https://github.com/user-attachments/assets/13e15df3-6f13-4d22-9dfd-a9a075e6561c" />

---

## 3. Space Distribution (Chassis Layout)

To maximize mechanical traction grip and lower the vehicle's moment of inertia during fast cornering, all heavy components are strategically arranged across multiple levels:

```
+-------------------------------------------------------------------+
| [UPPER LEVEL(Cam Base)]   IMX219 Camera (Elevated front mount for clear FOV)
+-------------------------------------------------------------------+
| [MID LEVEL]     Raspberry Pi 4  |  MegaPi Core  | Buck Regulator
|                 Logic LiPo Pack |  Power LiPo Pack
+-------------------------------------------------------------------+
| [LOWER LEVEL]   4x RS380 Motors |  MG996R Servo | Ultrasonic Tri-Array
+-------------------------------------------------------------------+

```

* **Battery Placement:** Slotted into the lowest and most central portion of the chassis to pull the center of gravity as low as possible, preventing high-speed body rolls or flipping in tight turns.
* **Camera Isolation:** The Arducam is housed on an elevated front tower. By routing its native MIPI CSI-2 ribbon cable directly into the Raspberry Pi's GPU, the pixel data travels completely shielded from the electromagnetic noise (EMI) radiating from the motors below.
* **Ultrasonic Tri-Array:** The three HC-SR04 sensors are locked into the front bumper at specific angles ($0^\circ, -45^\circ, +45^\circ$). This spatial layout creates an overlapping field of view without cross-talk interference, because our navigation code pings and samples them sequentially one by one.

---

## 4. Considerations & Future Enhancements

By benchmarking our vehicle against top international competition strategies, we have identified key areas for future development:

1. **Closed-Loop Speed Control (Quadrature Encoders):**
* *Current Issue:* The software adjusts motor speed by scaling voltage blindly based on estimated track requirements. If a wheel slips over a low-friction patch, the vehicle drifts off course.
* *Solution:* Install magnetic quadrature encoders on the rear motor shafts to implement a feedback PID controller, ensuring the wheels rotate at the exact RPM requested by the navigation script.


2. **Upgraded Communication Interface (SPI / Direct GPIO UART):**
* *Current Issue:* The physical USB-to-Serial cable occupies chassis space, adds dead weight through bulky connectors, and is vulnerable to disconnecting under high-frequency mechanical vibration.
* *Solution:* Rewire the interface to utilize the native GPIO pins directly via SPI or a soldered direct UART bus, cutting data transmission latency in half.


3. **Hardware-Level Automatic Regenerative Braking:**
* *Current Issue:* Excess kinetic energy from sudden braking dumps directly back into the MegaPi's H-bridge MOSFETs as heat.
* *Solution:* Design a protection circuit equipped with fast-switching Schottky diodes to channel residual voltage back into the power battery pack, shielding the IC chips and extending overall race runtime.nal collision.
