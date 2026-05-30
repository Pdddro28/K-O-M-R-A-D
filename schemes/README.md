Electromechanical diagrams
====

# Hardware Architecture and Mechanical Engineering

Our autonomous vehicle splits its operational workload into two dedicated subsystems: The Mechanical Muscle and Geometry (chassis physics, Ackermann steering, and raw propulsion) and The Electronic Brain and Perception (dual controllers and high-bandwidth sensor feedback).

---

## Subsystem 1: Mechanical Muscle and Geometry

Instead of standard differential (tank-style) spin turns, this platform is engineered around true automotive physics using a modified YFROBOT 4WD chassis.

### Ackermann Steering Mechanism
The vehicle utilizes the Ackermann Steering Principle to conquer sharp cornering with minimal tire slip.

* **The Physics:** When cornering, the inner front wheel must follow a tighter radius than the outer wheel.
* **The Execution:** An MG996R digital servo (11 kg·cm torque) is mounted onto an L-shaped bracket. It drives a system of mechanical linkages, rudder arms, and asymmetrical connecting rods. This geometry forces the inner wheel to turn more sharply than the outer one automatically.
* **The Control:** Driven by a continuous, jitter-free 50Hz hardware PWM pulse from the MegaPi, keeping the steering stable at a calibrated center of 84°.

### Electronic 4WD Propulsion (Differential-Free)
Propulsion is delivered via a high-speed RS380 DC geared motor configuration.

* **The Setup:** Instead of a complex, heavy mechanical differential, power is routed directly to the wheels.
* **The Challenge:** Without a mechanical differential, wheels can slip or fight each other during tight turns.
* **The Software Solution:** Wheel speed coordination is managed entirely via code by applying varied Duty Cycles through an onboard H-bridge driver on MegaPi's Port 1. This bypasses delicate micro-traces and draws raw surges straight from the motor battery rail.

---

## Subsystem 2: Electronic Brain and Perception

To eliminate latency and prevent system crashes, high-level computational tasks and real-time hardware execution are completely isolated.


```

[ Arducam IMX219 ] ──(MIPI CSI-2)──►  [ Raspberry Pi 4 ]  (High-Level Vision / OpenCV)
│
(Isolated USB Serial)
▼
[ Actuators & Sensors ] ◄───────────  [ MegaPi Board ]    (Low-Level Real-Time Core)

```

### Dual-Controller Split
1. **The Brain (Raspberry Pi 4):** A high-performance single-board computer running Python and OpenCV algorithms to analyze the track ahead.
2. **The Reflexes (Makeblock MegaPi):** Powered by an ATmega2560 core (16 MHz), handling time-critical hardware tasks, instantaneous motor movements, and sensor reads.
3. **The Link:** Connected via a high-speed USB Serial connection (115200 baud) to optimize chassis space and isolate sensitive processing cores.

### Dual-Battery Isolation and Power Distribution
To survive massive current spikes when accelerating from a dead stop, the robot completely separates logic power from mechanical loads:

| Power Source | System Group | Regulation Layer | Engineering Purpose |
| :--- | :--- | :--- | :--- |
| **11.1V LiPo Pack A** | Logic & Vision | **15W Type-C Buck Converter** (Steps down to 5V @ 3A) | Keeps the Raspberry Pi 4 fed with rock-solid power; guards against data corruption. |
| **11.1V LiPo Pack B** | Motors & Servos | **Direct Power Jack** (Raw 11.1V input) | Feeds high-current inductive loads directly so they do not drain the microprocessors. |

> **The Ground Rule:** Every single component shares a unified Common Ground (GND) path back to the MegaPi. Without this zero-volt reference, control signals would float, causing erratic steering, corrupted ultrasonic echoes, and catastrophic signal noise.

---

## Sensor Array and Spatial Awareness

### High-Bandwidth Vision
* **Hardware:** Arducam IMX219 8-Megapixel wide-angle camera.
* **Pipeline:** Connected directly to the Raspberry Pi's GPU via a native MIPI CSI-2 15-pin ribbon cable.
* **Why it matters:** Eliminates external power wiring and bypasses the microcontroller entirely. It streams raw image data at high frame rates with zero latency, completely shielded from electromagnetic interference (EMI) from the motors below.

### Ultrasonic Tri-Array Spatial Awareness
Three HC-SR04 ultrasonic sensors are arranged in a strategic tri-array configuration (Left, Center, Right) to handle obstacle avoidance.

* **5V CMOS Logic:** Powered by a clean 5V rail to ensure maximum acoustic transducer strength.
* **Independent Routing:** Each sensor is assigned its own dedicated Trigger (Output) and Echo (Input) pins on the MegaPi.
* **Cross-Talk Prevention:** The navigation code fires and samples each sensor independently in sequence, creating an overlapping web of spatial awareness without signal collision.


<img width="2960" height="1625" alt="L-N-M@1 25x" src="https://github.com/user-attachments/assets/13e15df3-6f13-4d22-9dfd-a9a075e6561c" />
