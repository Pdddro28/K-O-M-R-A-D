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

To ensure that our autonomous vehicle maintains optimal tracking accuracy under any changes in ambient track lighting, we designed and implemented an interactive calibration application with a **Graphical User Interface (GUI)** using the `customtkinter` library.

This tool allows the team to tune threshold ranges in the **CIELAB** colour space in real time and export the results directly to standardised configuration files in **JSON** format.

The application implements an event-driven architecture by combining real-time processing from **OpenCV** and **Picamera2** with the main rendering loop (`mainloop`) of the graphical interface.

<img width="212" height="692" alt="untitled@1 25x" src="https://github.com/user-attachments/assets/477382e0-c876-448b-9bd1-81d4c36f85eb" />

### Key Software Components

### 1. High-Performance Graphical Interface (`VisionApp`)

Built on a responsive design using dark panels (`ctk.set_appearance_mode("Dark")`), the interface is divided into two main sections:

-   **Side Control Panel:** Contains a drop-down menu with presets (`COLOR_PRESETS`) to quickly start searching for specific colours (Red, Green, Blue, Purple, Orange and Black). It features 6 high-precision linear sliders (`CTkSlider`) that dynamically control the minimum and maximum limits of the **L**, **A** and **B** channels.

-   **Horizontal Multi-tab Display Panel:** To provide accurate feedback during calibration, the script uses the `np.hstack()` method to combine three separate image matrices into a single real-time video strip:
    
    1.  **Original Frame:** The captured raw stream, geometrically corrected in reverse to correspond to the physical position of the camera.
        
    2.  **Binary Mask:** A black-and-white image that shows exactly which pixels are passing through the filter based on the current slider settings.
        
    3.  **Segmented Result:** The matrix operation (`cv.bitwise_and`) that isolates the filtered objects whilst retaining their actual colours, allowing you to see immediately whether ground noise is being captured.


       ### 2. Mask Processing and Morphological Filtering (`find_mask`)

When the sliders are moved, the `VisionController` class evaluates the Region of Interest (ROI) and calculates the binary segmentation using `cv.inRange`. To clean the signal of external factors or track imperfections, a morphological filtering loop for spatial cleaning is applied:

```
mask = cv.erode(mask, kernel, iterations=1)
mask = cv.dilate(mask, kernel, iterations=1)

```

## Structure of the JSON Configuration File

When the operator clicks **"SAVE JSON"**, the application opens a native file browser and saves a structured object that the main navigation script reads when the vehicle starts up. This means you don’t have to touch a single line of source code before running a race.

Example of the automatically generated output format:

```
{
    "color": "BLUE",
    "timestamp": "2026-06-02T10:13:21.286307",
    "bounds": {
        "lower": [
            30,
            110,
            0
        ],
        "upper": [
            255,
            184,
            95
        ]
    },
    "space": "LAB"
}

```

## Technical Procedure for the Competition

This is the procedure our team follows at the test bench before each official attempt:

**1. Select the Target:**

Launch the software and select the item to be calibrated from the drop-down menu (for example, `GREEN` for the avoidance blocks or `BLACK` for the boundary lines).

**2. Adjust the Colour Thresholds:**

Move the **A** (green-red axis) and **B** (blue-yellow axis) sliders. Because the LAB colour space decouples brightness, colour can be isolated very intuitively. Adjust the **L** (Luminance) slider to include or exclude the intensity of the ceiling lights.

**3. Check the Video Strip:**

Look at the third image on the screen (Segmented Result). The target should be clearly defined and the background of the track should be completely dark (pure black).

**4. Save the settings:**

Press the green **SAVE JSON** button. The system permanently saves the calibration with a timestamp for version control.

Open challenge
====

### Strategy

Our navigation strategy is based on a hybrid approach that combines visual lane detection with telemetry to optimize speed on straight sections and ensure stability when cornering:

*   **Vision-Based Lane Segmentation:** The front camera captures the surroundings and applies a perspective filter (bird's-eye view). Using HSV color spaces, we isolate the lane boundary lines. The algorithm calculates the midpoint of the drivable lane.
*   **Steering Control (PID):** The difference between the vehicle’s center and the calculated center of the lane is fed as the error signal into a Proportional-Integral-Derivative (PID) controller that continuously adjusts the steering servo’s angle.
*   **Dynamic Speed Management:** The system analyzes the road curvature. On long straightaways, the PWM of the drive motors is increased to maximum asynchronously; when approaching a sharp turn detected by the vision system or the front distance sensor, the system applies predictive engine braking to prevent understeer.
*   **Turn Counting and Inertia:** The IMU gyroscope tracks accumulated turns of 90° and 360°. Upon registering the third complete rotation cycle coordinated with the run time, the robot executes the controlled stop routine.

### Flowchart



### Recommendations

*   **Light Immunity:** Do not rely on fixed color threshold values. Use pre-calibration to generate a dynamic parameter file or implement histogram normalization (CLAHE) in image processing to prevent failures caused by shadows on the track.
*   **Drift Effect:** The IMU accumulates error over time. Use distance sensors on straights to verify that the IMU’s angular readings have not become misaligned due to chassis vibrations.

Obstacle challenge
====

### Strategy

*   **Object Detection and Classification:** The system simultaneously segments three color masks in OpenCV: Black/White (lane), Red (mandatory obstacle on the right), and Green (mandatory obstacle on the left). The pixel size of the detected outline determines the estimated distance to the object (Bounding Box).
*   **Evasion Routine (Swerve Maneuver):** When a block enters the critical “collision zone” (validated by the front ToF sensor for millimeter-level precision):
    *   **Red Block:** The PID controller introduces an artificial *offset* to the right of the lane, forcing the servo to change course, and maintains lateral visual tracking to return to the center once the block leaves the field of view.
    *   **Green Block:** The controller introduces an *offset* to the left, executing the internal swerve maneuver.
*   **Lane Recovery (Re-entry):** After clearing the obstacle (confirmed by the side proximity sensors), the robot exits the evasion subroutine and restores the line-following PID setpoints to avoid colliding with the outer wall.

### Flowchart



### Recommendations

*   **Visual False Positives:** Sometimes, track lines or reflections from the environment can be mistaken for blocks in the distance. Implement a minimum contour size filter (`cv2.contourArea`) so that the robot ignores distant visual noise and reacts only to actual blocks.
*   **Actuator Synchronization:** When dodging, the drive motor speed must be reduced proportionally to the steering angle. If you maintain maximum PWM while turning sharply to avoid a block, the car’s inertia will cause it to skid, lose its IMU reference, and collide with the obstacle.
