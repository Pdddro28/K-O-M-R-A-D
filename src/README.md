Software documentation
====
This section provides an overview of the software architecture used in our autonomous vehicle for the WRO 2026 Future Engineers competition. It includes:

- The programming languages and tools used

- A high-level description of the system's modules

- How the robot processes sensor data, camera data, makes decisions, and controls hardware

- Integration with vision systems (e.g., line detection, obstacle recognition)

- Communication between controllers (e.g., Raspberry Pi ↔ MegaPi)

Folders structure
====

```
K-O-M-R-A-D/src/
├── Colors/ 
├── visiontesters/
|    ├── Color-Detector.py
|    └── ROI-Detector.py
├── PID_class.py
├── arduino_controller.ino
├── constants.py
├── mega_pi_controller.py
├── obstacle_challenge.py
├── open_challenge.py
└── vision_controller.py
```

Where:

- `Colors/`: Directory containing configuration files or specific color-space data used for calibration and image segmentation.

- `visiontesters/Color-Detector.py`: An OpenCV-based utility script designed to calibrate and test the color masks (such as LAB color-space masks) to ensure proper object detection.

- `visiontesters/ROI-Detector.py`: A testing tool used to visualize and adjust the specific Regions of Interest (ROI) coordinates on the camera feed.

- `PID_class.py`: Implements the Proportional-Integral-Derivative (PID) controller algorithm to handle precise steering corrections and smooth track alignment.

- `arduino_controller.ino`: The Arduino low-level firmware responsible for reading sensor inputs and directly managing actuators like servos, DC motors, and indicator LEDs.

- `constants.py`: Contains all the hardcoded configuration values that remain unchanged during execution, including Arduino pin maps, target steering angles, ROI definitions, and LAB color-space masks.

- `mega_pi_controller.py`: The high-level Python script that establishes communication with the Arduino hardware, translating strategic commands into direct motor and servo movements.

- `obstacle_challenge.py`: The final, production-ready code designed to execute the logic, avoidance, and navigation required for the second challenge (Obstacle Challenge).

- `open_challenge.py`: The final, production-ready code designed to handle high-speed tracking and standard navigation for the first challenge (Open Challenge).

- `vision_controller.py`: The core image processing module responsible for capturing the video feed, applying color masks, and analyzing the defined ROIs to detect path elements and targets.

Table of contents
====

ped ped ped ped ped ped

Code description
====

ped ped ped ped ped ped

Calibration
====

ped ped ped ped ped ped

Open challenge
====

ped ped ped ped ped ped

Obstacle challenge
====

ped ped ped ped ped ped

Recomendations
====

ped ped ped ped ped ped
