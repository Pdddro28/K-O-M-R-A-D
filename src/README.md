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

Note: To run any file of the project, you have to follow these steps:

Clone the repository:
```bash
git clone https://github.com/JD277/K-O-M-R-A-D.git
```

Move to the project folder:
```bash
cd K-O-M-R-A-D
```

Install the dependencies:
```bash
pip install opencv-python numpy pandas picamera pyserial customtkinter
```

Execute the file you want using this structure:
(Remember to upload arduino_controller.ino or StandardFirmata to your board first!)
```bash
python3 -m src.open_challenge
```

Note on execution: This specific way to execute the files (python3 -m) is required so Python can read the directories as structural modules. The __init__.py files inside the directories allow Python to correctly resolve and handle the imported files as packages.

Core Libraries Used
====
```OpenCV (opencv-python):``` Used for real-time computer vision, image processing, and color segmentation.

```NumPy:``` Handles heavy matrix operations and mathematical calculations for vision coordinates and masks.

```Pandas:``` Utilized for data handling, logging, or managing calibration datasets.

```PiCamera:``` Direct interface to capture high-frame-rate video feeds from the Raspberry Pi camera module.

```PySerial (Serial):``` Establishes serial communication between the master controller (Raspberry Pi) and the Arduino micro-controller.

```CustomTkinter:``` Used to develop a modern graphical user interface (GUI) for calibration and manual testing tools.

```Dataclasses:``` (Built-in) Used to create structured data models for clean coordinate and ROI handling.

Table of contents
====

* [Code description](#code-description)

* [Calibration](#calibration)

* [Open challenge](#open-challenge)
 
* [Obstacle challenge](#obstacle-challenge)

Code description
====

This document provides a detailed and comprehensive description of all class attributes and methods, including the specifications of their respective arguments. We strongly recommend reviewing this section before exploring the rest of the documentation.

If you plan to clone this repository, we suggest using this section as a reference map or navigation guide. It will help you understand the project’s structure, speed up your workflow, and help you quickly locate key components within the source code.

Calibration
====

Computer Vision Calibration (camera_calibration.py): Since lighting conditions at the event can vary drastically due to artificial lighting or nearby windows, the OpenCV-based vision system implements dynamic calibration.

* **Perspective Matrix (Bird’s Eye View):** Geometric camera correction to transform the perspective view into an aerial plan view. This allows for the precise measurement of actual distances to the track lines and blocks.

* **HSV Color Thresholds (Color Thresholding):** Adjustment of the color mask ranges for accurate detection of lines (Black/White) and traffic elements (Red and Green Blocks).

* **Code Operation:** The script uses runtime sliders (cv2.createTrackbar) to find the optimal values for H (Hue), S (Saturation), and V (Value), which are automatically exported to a .json or .yaml configuration file that the main script reads upon startup.


Mechanical Steering Calibration (`steering_calibration.py`)
The mechanical components of the steering system (servo links and Ackermann geometry) are rarely perfectly symmetrical by design. 

* **Neutral Point Adjustment (Trim):** Defines the exact pulse width (in microseconds or degrees) that forces the vehicle to move in a perfect straight line.
* **Maximum Limit Mapping (Endpoints):** Configuration of the maximum left and right turning angles. This prevents the servo motor from being overloaded, avoiding mechanical jams or excessive current draw that could reset the electronics.
    * *Operation in the code:* When this module is executed, the servo oscillates between its critical points, allowing the operator to visually verify the alignment of the front wheels before setting the parameters in the software constants.


Calibration of Kinematic and Distance Sensors (`sensor_calibration.py`)
Module responsible for stabilizing the proximity and telemetry sensors before allowing the chassis to move.

* **Gyroscope/IMU Calibration (Offset Reset):** When the robot is powered on, it must remain stationary for approximately 2 to 3 seconds. The script calculates the average white noise of the sensor (magnetic/gyroscopic drift) on the X, Y, and Z axes to establish the relative zero degree of orientation.
* **Distance Sensor Filtering:** Initialization and calculation of the error threshold for ultrasonic sensors or time-of-flight (ToF/LiDAR) sensors, ensuring accurate detection of the track’s side walls.

Open challenge
====

### Strategy

### Flowchart

### Recommendations

Obstacle challenge
====

### Strategy

### Flowchart

### Recommendations
