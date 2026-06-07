Intro
====

This is the official Github repository proporty of The LNM, before known as Ars Machina, conformed by David Wang Wu and Pedro Catamo. This repository contains all the code, documentation and resources for our project. This is our fourth year participating in WRO.

Team Members
====

I am David Wang:

Birth date: 01/04/2011(15y/o)

Studying: 3rd year at U.E.C.Eduardo Blanco

Misc: I speak English,Spanish,Mandarin and Taiwanese

Aspirations: Computer Science at the UGMA Universidad Gran Mariscal de Ayacucho

Gmail: davidwangwu104@gmail.com



I am Pedro Catamo:

Birth date: 01/28/2009(17y/o)

Studying: 5th year at U.E.C.Eduardo Blanco

Misc: I speak English and Spanish

Aspirations: Biomaterials Engineering at the UNC Humberto Fernandez Moran

Gmail: pedrocatamo.2009@gmail.com

Folders Structure
====

Here is our Folder Structure of the repository:

```
LNM/
├── models/
├── schemes/
├── src/
├── t-photos/
├── v-photos/
└── video/

```

Where:

- `models`: Every 3D/CAD file used in the car. [view](./models/README.md)
- `schemes`: Wiring diagram, assembly explanation and components description. [view](./schemes/README.md)
- `src`: All code necessary to control the robot. [view](./src/README.md) 
- `t-photos`: Team photos. [view](./t-photos/README.md)
- `v-photos`: Vehicle photos. [view](./v-photos/README.md)
- `videos`: Performance videos of the robot. [view](./videos/README.md)

Mobility
====

* **Automotive Kinematics (Ackermann Steering):** Rejecting tank-style differential spin turns, the vehicle utilizes true automotive physics based on the Ackermann principle. When cornering, the inner front wheel pivots more sharply than the outer wheel, preventing tire scrubbing and slipping to ensure optimal grip and predictable handling at high speeds. The steering is driven by a high-torque MG996R digital servo stabilized at a rigidly calibrated 90° center via 50Hz hardware PWM pulses.
* **Propulsion and Speed:** Power is delivered by four RS380 DC geared motors operating at 11.1V and delivering approximately 450 RPM. With a wheel diameter of 6.5 cm, the robot reaches a theoretical maximum velocity of 1.53 m/s, resulting in an actual average track operating speed of approximately 1.2 m/s due to friction and weight.
* **Electronic Differential (Software-Managed Cornering):** To avoid a heavy mechanical central differential, wheel speed coordination during turns is handled entirely via software. By altering the duty cycles through H-bridge drivers, the algorithm reduces power to the inner wheels during a turn so they do not fight each other.
* **Mobility Limitations:** Aggressive dynamic braking generates counter-electromotive force (reverse currents) that can overheat the motor drivers if not properly dissipated. Additionally, the lack of a physical differential limits raw traction if a wheel completely loses contact with the track surface.

Software for our WRO autonomous vehicle
====

* **Architecture:** Python 3 code that bridges the Raspberry Pi and the motors via `MegaPiController` in a non-blocking asynchronous loop.
* **Vision (OpenCV):** Optimizes FPS by processing specific Regions of Interest (ROIs)—lateral zones for walls and a central zone for traffic—instead of the full frame.
* **Round 1 (Open Challenge):** Hybrid lane centering controlled by a visual PD based on the area difference between the walls. If the track widens and a wall leaves the camera's view, physical ToF distance sensors automatically kick in as a backup.
* **Round 2 (Obstacle Challenge):** A behavioral state machine bypasses traffic based on color: **Red** blocks force the car to hug the right wall, while **Green** blocks force it to the left (both maintaining a tight 12.0 cm distance).
* **Race Management:** Counts 12 laps by detecting color markers, using a 4-second cooldown to prevent false positives. Upon completion, it executes a 3-second grace period to cross the finish line safely under full autonomous control before shutting down the motors.
