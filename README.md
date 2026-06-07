Intro
====

This is the official Github repository proporty of The LNM, before known as Ars Machina, conformed by David Wang Wu and Pedro Catamo. This repository contains all the code, documentation and resources for our lil carrito. This is our fourth year participating in WRO.

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

Our vehicle utilizes an Ackermann steering geometry to optimize cornering stability and eliminate tire scrubbing. By dynamically adjustments the front wheels, this configuration ensures the inner wheel turns at a sharper angle than the outer wheel to match their respective turning radii. Propulsion is managed via an electronic differential setup, which is broken down in full detail below.

Software for our WRO autonomous vehicle
====

* **Architecture:** Python 3 code that bridges the Raspberry Pi and the motors via `MegaPiController` in a non-blocking asynchronous loop.
* **Vision (OpenCV):** Optimizes FPS by processing specific Regions of Interest (ROIs)—lateral zones for walls and a central zone for traffic—instead of the full frame.
* **Round 1 (Open Challenge):** Hybrid lane centering controlled by a visual PD based on the area difference between the walls. If the track widens and a wall leaves the camera's view, physical ToF distance sensors automatically kick in as a backup.
* **Round 2 (Obstacle Challenge):** A behavioral state machine bypasses traffic based on color: **Red** blocks force the car to hug the right wall, while **Green** blocks force it to the left (both maintaining a tight 12.0 cm distance).
* **Race Management:** Counts 12 laps by detecting color markers, using a 4-second cooldown to prevent false positives. Upon completion, it executes a 3-second grace period to cross the finish line safely under full autonomous control before shutting down the motors.
