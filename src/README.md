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
```
git clone https://github.com/JD277/K-O-M-R-A-D.git
```

Move to the project folder:
```
cd K-O-M-R-A-D
```

Install the dependencies:
```
pip install opencv-python numpy pandas picamera pyserial customtkinter
```

Execute the file you want using this structure:
(Remember to upload arduino_controller.ino or StandardFirmata to your board first!)
```
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

<div align="center">

<img width="200" height="700" alt="untitled@1 25x" src="https://github.com/user-attachments/assets/477382e0-c876-448b-9bd1-81d4c36f85eb" />

</div>

### Key Software Components

### 1. High-Performance Graphical Interface (`VisionApp`)

Built on a responsive design using dark panels (`ctk.set_appearance_mode("Dark")`), the interface is divided into two main sections:

-   **Side Control Panel:** Contains a drop-down menu with presets (`COLOR_PRESETS`) to quickly start searching for specific colours (Red, Green, Blue, Purple, Orange and Black). It features 6 high-precision linear sliders (`CTkSlider`) that dynamically control the minimum and maximum limits of the **L**, **A** and **B** channels.
    
-   **Horizontal Multi-tab Display Panel:** To provide accurate feedback during calibration, the script uses the `np.hstack()` method to combine three separate image matrices into a single real-time video strip:
    
    **Original Frame:** The captured raw stream, geometrically corrected in reverse to correspond to the physical position of the camera.
    
    **Binary Mask:** A black-and-white image that shows exactly which pixels are passing through the filter based on the current slider settings.
    
    **Segmented Result:** The matrix operation (`cv.bitwise_and`) that isolates the filtered objects whilst retaining their actual colours, allowing you to see immediately whether ground noise is being captured.

### 2. Mask Processing and Morphological Filtering (`find_mask`)

When the sliders are moved, the `VisionController` class evaluates the Region of Interest (ROI) and calculates the binary segmentation using `cv.inRange`. To clean the signal of external factors or track imperfections, a morphological filtering loop for spatial cleaning is applied:

Python

```
mask = cv.erode(mask, kernel, iterations=1)
mask = cv.dilate(mask, kernel, iterations=1)

```

### 3. Dynamic Region of Interest Selector (`ROI-Detector`)

To accurately limit the camera's field of view to specific zones of the track and optimize processing resources, we implemented a lightweight geometric calibration utility called `ROI-Detector.py`.

This script uses standard native libraries (`tkinter` and `dataclasses`) alongside **OpenCV** to allow developers to interactively draw, label, and export bounding boxes directly from a live video feed.

Python

```
import cv2
from dataclasses import dataclass
import tkinter as tk
from tkinter import filedialog

# --- DATA STRUCTURES ---
@dataclass
class ROI:
    x1: int; y1: int
    x2: int; y2: int

```

-   **Event-Driven Interaction:** The application hooks into the mouse pipeline via `cv2.setMouseCallback()`. When the operator clicks and drags on the interface, the script updates a temporary visual guide (`EVENT_MOUSEMOVE`) and permanently appends the coordinate pairs to a global configuration array upon release (`EVENT_LBUTTONUP`).
    
-   **Proportional Pillarboxing:** To guarantee that coordinate selection remains accurate across different camera hardware, the display loop applies a letterbox/pillarbox transformation using `cv2.copyMakeBorder`. This keeps the original aspect ratio perfectly centered inside a fixed $800 \times 600$ viewport.
    
-   **On-Screen Feedback:** Every selected region is drawn dynamically onto the frame using `cv2.rectangle()`, accompanied by a telemetry label showing the bounding box index and its precise resolution in pixels:
    

Python

```
label = f"ROI {i+1}: {width}x{height}"
cv2.putText(display, label, (x1_, y1_ - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

```

### Structure of the Exported Configuration Files

#### A. JSON Color Calibration Format

When the operator clicks **"SAVE JSON"** in the main interface, the application opens a native file browser and saves a structured object that the main navigation script reads when the vehicle starts up. This means you don’t have to touch a single line of source code before running a race.

Example of the automatically generated output format:

JSON

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

#### B. Python ROI Blueprint Format

When the execution of `ROI-Detector.py` is finished, the application automatically invokes a native file explorer via `filedialog.asksaveasfilename`. Instead of using an external data parsing format, it exports a directly importable, native Python script containing an array of serialized `ROI` objects.

Example of the automatically generated output format:

Python

```
from dataclasses import dataclass

@dataclass
class ROI:
    x1: int; y1: int
    x2: int; y2: int


rois = [
    ROI(120, 200, 340, 450),
    ROI(450, 200, 680, 450),
]

```

### Technical Procedures for the Competition

This is the procedure our team follows at the test bench before each official attempt:

#### Phase 1: Tracking Area Isolation (`ROI-Detector`)

**1. Initialize the Window:**

Launch the script. The system will open a standardized $800 \times 600$ window displaying the live feed from the camera, automatically padded with black borders if needed to maintain aspect ratio.

**2. Draw the Regions:**

Click and drag the left mouse button (`LBUTTONDOWN`) across the target zones. A yellow tracking box will show the real-time bounds. Releasing the button locks the green box and updates the pixel layout label.

**3. Clear or Reset (Optional):**

If a tracking area is misplaced during the session, press the **'c'** key on the keyboard to wipe the array clean and start drawing the coordinates fresh.

**4. Export the Python Blueprint:**

Press the **'ESC'** key or close the application window. A file manager window will pop up prompting you to name and save your compiled `.py` coordinate script, which will be loaded directly by the vehicle’s high-level navigation code.

#### Phase 2: Color Space Thresholding (`VisionApp`)

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
---

To navigate without relying on continuous lines, the robot measures the free space on either side using two lateral Regions of Interest (`roi` and `roi2`).

-   **Error Calculation:** Error = Left Area - Right Area
    
-   **PD Controller:** Controls an Ackermann servo using parameters K_p = 0.015 and K_d = 0.005 (centre at 80°)
    
-   **Stability Filters (Anti-Zigzag):**

    -   `DEAD_PIXEL_THRESHOLD = 150`: Ignores insignificant variations in area.
        
    -   `ANGLE_TOLERANCE = 3`: If the correction is minimal 77° and 83°, forces the heading to 80° (straight ahead) to avoid oscillations and save energy.

The vehicle makes decisions by combining computer vision and forward ultrasonic distance sensing.

### A. Track Identification (Track Type)

On start-up, the robot detects the colour of the first finish line (area > 1200) to determine the turning direction:

- Orange line: Locks in a counter-clockwise direction.

- Blue Line: Locks clockwise direction.

### B. Corner Turning Algorithm Entry Trigger:

If the distance to the front is < 55cm and the black area of the walls is > 11000, the robot calls LNM.turn_direction() and locks into turning mode (turning = True). Exit Trigger: When the track is clear in front > 80cm and the wall area falls below 8000, the robot returns to PID centring.

- Emergency Braking and Active EvasionIf the proximity sensor detects a frontal obstacle within DIST_MIN_CHOQUE (20.0 cm), an immediate hardware response is triggered: Braking: Complete shutdown of the rear motor (LNM.stop()).

- Inverse Calculation: Calculates an evasion angle symmetrically opposite to the previous turn 160°. Manoeuvre: Reverses at high power (speed = 85) for 0.75 seconds to clear the obstruction, clears the PID history and resumes driving.

- Lap Counter and Technical Finish: The rules require the car to stop exactly after completing 3 laps (12 control lines/corners).

- Debounce Filter: When a line is crossed, the reading is held for 1.7s (orange/blue_timer). This prevents the same line from being counted multiple times as the chassis passes over it.

- Non-Blocking Finish: Upon reaching lap 12, a 1s grace period timer is activated. The robot continues to navigate in a controlled manner to cross the finish line completely before shutting down definitively with LNM.stop().

### Flowchart
---


### Recommendations
---

- Reducing Video Latency: In the main loop, comment out or remove the lines for `cv2.imshow` and `cv2.waitKey` entirely during official rounds. Rendering video on screen consumes critical CPU resources and reduces the FPS of the control loop.

- Quick On-Site Calibration: Bring at least three pre-configured JSON files from home (“High Light”, “Medium Light”, “Low Light”). If the practice time at the event is very short, simply load the one that most closely matches the environment rather than calibrating from scratch.

- Protection against visual false positives: Strictly limit the size of the lateral ROIs (roi and roi2) so that they face only the floor and do not detect the walls of the category or other robots in the background.

Obstacle challenge
====

### Strategy
---

When the robot is travelling along straight sections or open bends, it evaluates three logical scenarios in sequence to determine its direction using independent PID controllers:

#### CASE A: Active Obstacle Avoidance (Priority 1)
If the camera detects a coloured block within its front ROI, the system ignores visual centring and uses the side ToF sensors to manoeuvre around it:

- RED block (Avoidance to the Left): The robot activates pid_dist_der, sets its target distance to DIST_PEGADO (12.0 cm) relative to the right wall, and moves away from the obstacle.

- GREEN block (Avoidance to the Right): pid_dist_izq is activated, aiming to stay 12.0 cm from the left wall.


#### CASE B: Backing Up Due to Wall Loss (Priority 2)
If one of the two black walls on the track moves out of the field of view of the side ROIs (area < MIN_VALID_WALL), the robot uses the physical ToF sensors to avoid collision, guiding itself according to the direction of the circuit:

- Orange Direction: Follows the left wall as a reference using the left ToF.

- Blue Direction: Follows the right wall as a reference using the right ToF.

#### CASE C: Pure Comfort Centring (Priority 3)

If the track is clear and both walls are visible, pid_vision is activated. The system seeks symmetrical balance by calculating:Error = Left Area - \Right AreaThe loop calculates the direction required to maintain an error of 0.

- Steering Stability Filters
To prevent the servo from overheating or experiencing unnecessary vibrations, the outputs of the three PIDs pass through a hysteresis filter: Deadband (ANGLE_TOLERANCE = 3): If the calculated angle is between $77^\circ$ and $83^\circ$, the car forces the servo to $80^\circ$ (straight). This maintains linear inertia on clear stretches and saves battery power.

- Emergency Evasive Manoeuvre
To mitigate collisions caused by blind spots or loss of traction during tight manoeuvres, the system features an autonomous safety response:

```
if (Front Distance < 20 cm) and (No coloured block detected)
      ACTION: Stop motors + Reverse with Inverse Angle for 0.75 seconds
This mechanism dynamically calculates an escape angle opposite to the last recorded turn ($160 - \text{steering\_angle}$), freeing the chassis from the jam before restarting the main control loop.

```

### Flowchart
---


### Recommendations
---

-   **Data Synchronisation (Vision vs. ToF):** Please disable `cv2.imshow` and `cv2.waitKey` completely during official rounds. Rendering video on screen consumes critical CPU resources and causes delays (latency) between camera readings and ToF sensor readings.

-   **Hysteresis and False Positives:** Implement a voting filter for colour (detect the block over 2 or 3 consecutive frames before taking action). Reduce the front ROI vertically to ignore floor reflections or ceiling lights that mimic real blocks.

-   **Smooth PID Transitions:** Reset the controllers’ numerical history (previous error = 0 and integral = 0) every time the code switches between vision-based centring and ToF-based avoidance. This prevents sudden jerks and skidding.

-   **Dynamic Speed:** Don’t keep the power set at 65. Reduce your speed during sharp turns (when dodging blocks) to maintain grip, and automatically increase it on straight, clear stretches to improve your lap times.
