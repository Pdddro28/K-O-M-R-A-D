### 3D Printed Components & Attachments

During the development of the vehicle, structural space constraints on the stock chassis made it unfeasible to mount all electronic and mechanical components directly to the base plate. To maximize spatial efficiency and maintain a low center of gravity, we designed and 3D-printed several custom modular attachments. 

These components extend the chassis vertically and provide secure, vibration-resistant housings for our specialized hardware.

---

### Component Specifications and Layout

The detailed engineering specifications, design purposes, and spatial distribution for each custom 3D-printed base are detailed below:

Battery Case
===

- ```Design & Geometry:``` Designed as a low-profile dual compartment located on the central geometric axis of the lower chassis. It features 2.5 mm thick reinforced walls and passive side ventilation slots to prevent thermal stress on the LiPo cells during high discharge rates (C-rate).

- ```Engineering Purpose:``` Centralises the combined mass of the two battery packs (2200 mAh each) at the lowest point of the vehicle. This drastically reduces the polar moment of inertia and prevents body roll in tight corners. It includes a quick-release tab fastening system and integrated guides for the secure routing of high-current wiring to the MegaPi terminals.

Canera Case
===

- ```Design & Geometry:``` An elevated tower structure rigidly attached to the front bumper using an M3 bolt pattern. The housing head features a precision-machined slot to house the IMX219 (Arducam) camera sensor and a 15-degree downward tilt angle optimised in Blender.

- ```Engineering Purpose:``` Raises the camera’s line of sight to maximise the field of view (FOV) towards the ground, ensuring that OpenCV algorithms can detect track lines and obstacles in advance. By isolating the camera in a dedicated structure, chassis micro-vibrations are mitigated and the delicate MIPI CSI-2 ribbon cable is routed away from electromagnetic interference (EMI) from the rear motors.

MegaPi Case
===

- ```Design & Geometry:``` A sealed module with 3 mm internal support towers (standoffs) integrated directly into the base plate to suspend the PCB and prevent contact with the chassis. It features calibrated perimeter openings to provide full access to the motor screw terminals, the ultrasonic sensor ports and the main power interface.

- ```Engineering Purpose:``` It acts as a protective shield for low-level power electronics. It protects the H-bridges and microcontroller pins from accidental mechanical impacts or dislodgement caused by track vibrations. It also includes top grilles designed for the optional mounting of a passive heat sink or a 40 mm fan.

RaspberryPi Base
===

- ```Design & Geometry:``` A mid-level modular mounting platform that acts as a structural ‘bridge’ over the chassis. It uses elongated expansion slots that allow its longitudinal position to be adjusted with millimetre precision to calibrate the car’s centre of gravity.

- ```Engineering Purpose:``` Provides a rigid mount for the on-board computer (Raspberry Pi 4), keeping the computer vision processing hardware perfectly level. Its open design ensures optimal thermal dissipation via natural convection for the Broadcom processor, preventing thermal throttling during the execution of real-time detection models.
