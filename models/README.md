### 3D Printed Components & Attachments

During the development of the vehicle, structural space constraints on the stock chassis made it unfeasible to mount all electronic and mechanical components directly to the base plate. To maximize spatial efficiency and maintain a low center of gravity, we designed and 3D-printed several custom modular attachments. 

These components extend the chassis vertically and provide secure, vibration-resistant housings for our specialized hardware.

---

<img width="3060" height="4080" alt="20260530_162359" src="https://github.com/user-attachments/assets/cc130bf0-8547-48cc-847e-28dbd9029fba" />


### Component Specifications and Layout

The detailed engineering specifications, design purposes, and spatial distribution for each custom 3D-printed base are detailed below:

Battery Case
===

- ``` Design & Geometry:``` Designed as a vertical tower cage structured with four reinforced pillars on each side, integrated directly onto a solid mounting base with corner screw eyelets. The side walls feature large circular cutouts to minimize material weight while allowing maximum passive airflow to prevent thermal stress on the LiPo cells during high discharge rates. The top pillars include slotted retention eyelets for secure strap fastening.

- ```Engineering Purpose:``` Centralizes the combined mass of the battery cells vertically along the central geometric axis of the chassis. This open-cage design ensures quick access for battery replacement between runs while providing rigid structural containment against lateral inertia forces during high-speed cornering.

<img width="605" height="648" alt="BatteryCase" src="https://github.com/user-attachments/assets/b3e6554a-211a-4241-bda4-a5d5db77534f" />

Canera Case
===

- ```Design & Geometry:``` A compact, rectangular protective enclosure specifically tailored to encapsulate the IMX219 (Arducam) sensor. The bottom section integrates a robust cylindrical pivot hinge featuring external locking teeth (spur gear profile) designed to mesh perfectly with a matching mounting base for mechanical angle locking.

- ```Engineering Purpose:``` Shields the delicate camera PCB from external debris or direct track impacts. The interlocking geared hinge allows the camera's pitch to be adjusted and mechanically locked at a precise 15-degree downward tilt angle, preventing any unwanted lens shifting caused by high-frequency chassis vibrations during operation.

<img width="308" height="395" alt="Camera" src="https://github.com/user-attachments/assets/21c54df1-dd10-4c78-a3e6-093260773084" />

MegaPi Case
===

- ```Design & Geometry:``` A robust low-profile tray equipped with four integrated, heavy-duty vertical standoffs positioned at the corners to secure the main PCB. The base plate features internal layout guides and structural clearance cuts to avoid components on the underside of the board while keeping the profile as close to the chassis as possible.

- ```Engineering Purpose:``` Functions as a rigid mechanical cradle for the low-level power electronics. By elevating the PCB via the 3mm integrated standoffs, it prevents electrical short-circuits with the chassis while dampening vibrations. The completely open perimeter guarantees immediate access to the motor screw terminals, power rails, and sensor ports for field maintenance.

<img width="698" height="515" alt="MegaPiBase" src="https://github.com/user-attachments/assets/1998a856-5af4-434d-878d-18f04e4c0457" />

RaspberryPi Base
===

- ```Design & Geometry:``` A flat, mid-level modular platform featuring four integrated corner standoffs to mount the Raspberry Pi 4 safely. The front section of the base integrates a dual-ear hinge mount equipped with internal locking teeth that mate directly with the Camera Case hinge.

- ```Engineering Purpose:``` Serves as a dual-purpose structural bridge. It provides a stable, elevated mount for the high-level on-board computer, ensuring optimal heat dissipation via natural convection to prevent CPU thermal throttling. Concurrently, its integrated geared mount firmly locks the camera assembly at the front, eliminating the need for extra components and saving valuable chassis space.

<img width="698" height="515" alt="MegaPiBase" src="https://github.com/user-attachments/assets/74d4b89d-c859-4a69-b3b7-ce7326d4601a" />
