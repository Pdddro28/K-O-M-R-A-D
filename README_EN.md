``` For better viewing, it is recommended to view the repository on a computer ```

# WRO 2026 Future Engineers – LNM

Bienvenidos al repositorio de GitHub del **Equipo LNM**, anteriormente conocido como Ars Machina, que compite en la categoría **World Robot Olympiad™ (WRO®) Future Engineers 2026**. Nuestro equipo está formado por David Wang y Pedro Catamo que han diseñado un vehículo autónomo compacto e innovador para hacer frente a los retos dinámicos de la competición WRO 2026.

El Equipo
====

<div align="center">
	
<img width="1280" height="720" alt="Team_pic (1)" src="https://github.com/user-attachments/assets/156c3c29-799e-44e6-a7f0-629da61873b8" />

</div>

- ### Members:

	- **David Wang**
		Born on: 01/04/2011 (15 years old)
		Education: 3rd year at U.E.C. Eduardo Blanco
  		Gmail: davidwangwu104@gmail.com
  	  
	- **Pedro Catamo**
 	  	Born on: 28/01/2009 (17 years old)
   		Education: 5th year at U.E.C. Eduardo Blanco
   		Gmail: pedrocatamo.2009@gmail.com

 - ### Coach:

	- **Jesús Alcalá**
  		Born on: 18/11/2005 (21 Years old)
   		Education: Computer Engineering & Informatics Engineering
   		Gmail: Jdam50002@gmail.com

Car Photo
====

<div align="center">

<img width="3060" height="4080" alt="604003001-cc130bf0-8547-48cc-847e-28dbd9029fba" src="https://github.com/user-attachments/assets/f1dc12a1-dbfc-46f3-9a21-a679aa1aa3db" />

</div>

Folder Structure
====

This is the folder structure of our repository:

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

- `models`: All 3D/CAD files used in the car. [view](./models/README.md)
- `schemes`: Wiring diagram, assembly instructions, and component descriptions. [view](./schemes/README.md)
- `src`: All the code required to control the robot. [view](./src/README.md) 
- `t-photos`: Team photos. [view](./t-photos/README.md)
- `v-photos`: Vehicle photos. [view](./v-photos/README.md)
- `videos`: Videos of the robot's performances. [view](./videos/README.md)

# 1- Mobility and Design

- ### Design Choices:
  
<div align="center">
	
| Photo | Name |
|---|---|
| <img width="420" height="320" alt="Captura de pantalla 2026-06-17 185504" src="https://github.com/user-attachments/assets/36166165-a542-42d6-a771-41a60693a399" /> | **Cyber Cooper** |
| <img width="420" height="320" alt="front2" src="https://github.com/user-attachments/assets/ce130237-cc0b-4aa9-a620-0aea287408c2" /> | **Cooper** |
| <img width="420" height="320" alt="front" src="https://github.com/user-attachments/assets/804b3d7f-3500-4351-a917-ccf781029804" /> | **Halbi** |
| <img width="420" height="320" alt="WhatsApp Image 2026-06-18 at 7 39 40 PM" src="https://github.com/user-attachments/assets/ca9f62ff-7b8b-452a-97de-95ebf12dc0ef" /> | **The Fridge** |

</div>

 - ### Halbi The Green:

    - ### Photo:

	<div align="center">

	<img width="260" height="280" alt="604003001-cc130bf0-8547-48cc-847e-28dbd9029fba" src="https://github.com/user-attachments/assets/f1dc12a1-dbfc-46f3-9a21-a679aa1aa3db" />
	<img width="260" height="280" alt="Upper-Pov" src="https://github.com/user-attachments/assets/74863cc8-5128-49cf-845e-0f087c50bcf1" />
	<img width="260" height="280" alt="RightSide-Pov" src="https://github.com/user-attachments/assets/8b9c2020-cc18-441f-9152-c86d9a233b10" />
	<img width="260" height="280" alt="LeftSide-Pov" src="https://github.com/user-attachments/assets/cdbabe27-6e45-4dab-98e6-e63b24ed7371" />
	<img width="260" height="280" alt="Front-Pov" src="https://github.com/user-attachments/assets/d9b65dd5-ca97-4087-ba20-77f7cbeb4bf6" />
	<img width="260" height="280" alt="Back-Pov" src="https://github.com/user-attachments/assets/dd1737be-1173-4cae-9229-25821f05dc22" />

    </div>

	- ### Main Mechanical Specifications:

		- **Total dimensions: 24.4 cm (length) × 15.4 cm (width) × 15.9 cm (height).**
		- **Total mass: approximately 1.2 kg.**
		- **Drive configuration: Biphasic Mechanical Rear-Wheel Drive.**
		- **Steering system: Ackermann Geometry.**
	
	- ### Ackermann Steering Mechanism

		The vehicle utilizes a precise geometry based on the **Ackermann Steering Principle** to conquer tight corners with zero lateral slippage and minimal tire wear.

		* **The Physics Behind the Principle:** When a vehicle enters a turn, the inner front wheel follows a tighter and smaller concentric radius than the outer wheel. If both wheels turned at the exact same angle, the tires would fight against each other, causing the outer tire to drag, lose mechanical grip, and introduce severe structural vibrations that would ruin visual lane tracking. To resolve this, the mechanical geometry forces the inner wheel to pivot at a deeper angle than the outer wheel, ensuring that all four wheels rotate around a single common Instantaneous Center of Curvature (ICC).

		* **The Mechanical Execution:** An **MG996R** high-torque digital servo ($11 \text{ kg}\cdot\text{cm}$ of torque) is anchored to the front bulkhead using a custom-machined L-shaped aluminum bracket to eliminate structural deflection. The servo horn drives a dual-link steering rack connected to asymmetric tie rods and steering knuckles. The steering arms are angled inward, pointing toward the center of the rear axle, completing the classic "Ackermann Trapezoid". This exact mechanical design automatically converts the linear displacement of the servo into non-linear wheel angles.

		* **Digital Control and Calibration:** The MG996R is controlled by a continuous, jitter-free hardware PWM pulse train at $50\text{Hz}$ directly from the MegaPi microcontroller. The steering is rigidly mapped and calibrated to a software deadband where $80^\circ$ represents the absolute geometric center. The mechanical endpoints are software-limited between $40^\circ$ (Maximum Left) and $105^\circ$ (Maximum Right) to prevent the steering linkages from reaching a mechanical lock or straining the motor's stall limits.

	- ### What is Ackermann Geometry? 

		Understanding Ackermann Mathematics and Kinematics, traditional mobile robotics (such as robots in the *RoboMission* category) use differential drive because it is mathematically simple: you vary the speed of two motors and the robot turns on its own axis. However, at high speeds, differential drive is unstable and unpredictable.

		**Ackermann Geometry** resolves this through a purely mechanical principle. For a vehicle to turn without slipping laterally, the extended lines from the axles of all wheels must intersect at a single point in space: the **Instantaneous Center of Rotation (ICR)** or ICC.

		The fundamental mathematical equation governing this kinematics is:
		<div align="center">
	
		$$\cot(\theta_{\text{out}}) - \cot(\theta_{\text{in}}) = \frac{w}{L}$$
		
		</div>
		Where:
		* $\theta_{\text{in}}$ is the steering angle of the inner wheel.
		* $\theta_{\text{out}}$ is the steering angle of the outer wheel.
		* $w$ is the track width (*track width* or distance between the front wheels).
		* $L$ is the wheelbase (*wheelbase* or distance between the front and rear axles).

		Since the cotangent grows faster at small angles, this relationship mechanically forces $\theta_{\text{in}} > \theta_{\text{out}}$ automatically in any curve, opening the angle of the outer wheel so that it draws a larger circle.

		<div align="center">
  
		<img width="567" height="600" alt="17523247_203569336801744_2788986523412924047_n" src="https://github.com/user-attachments/assets/c36a271c-b45c-492a-805e-b107851429cd" />
		
		</div>

	- ### 2WD Electronic Propulsion with Biphasic Mechanical Transmission 

		The driving force of the platform is generated by a high-performance rear-wheel-drive (2WD) system, which breaks away from traditional direct-coupling schemes by integrating a desmultiplied two-speed spur gear transmission.

		* **Transmission System Architecture:** Unlike common configurations that couple the wheel directly to the motor's gearbox, this design mounts the RS380 motor in an upper parallel layout on a rigid support block. Power is transferred from the primary shaft of the motor to a lower secondary drive shaft through an exposed straight-toothed gear train. This system of two interchangeable mechanical speeds allows configuring the robot according to the demands of the track:
  		1. **Force/Torque Ratio (First Gear):** Optimizes the reduction to obtain maximum acceleration and millimeter control in tight corners or obstacles, ideal for twisting sections. 
  		2. **Final Speed Ratio (Second Gear):** Reduces RPM loss to take advantage of linear inertia on long straights, guaranteeing a high cruising speed without saturating power consumption.

		<div align="center">
  
		<img width="515" height="218" alt="Sistema de transmision de 2 velocidades K-O-M-R-A-D" src="https://github.com/user-attachments/assets/da8175e6-313d-42d6-bd3b-b1318082536f" />
		
		</div>

		* **Technical Specifications of the Motors (RS380):** The power block relies on brushed DC motors with permanent magnets, specifically selected for their dynamic response curve and tolerance to transient load peaks.

	    * **Nominal Voltage:** $12\text{V}$ (Operating at a nominal cell voltage of $11.1\text{V}$ via a 3S LiPo battery to ensure thermal stability).
   
 		* **No-load Current:** $0.4\text{A}$ | **Stall/Starting Current:** $4.5\text{A}$ of protection in the driver.
   
 		* **Factory Rotation Speed:** $15000\text{ RPM}$ at the motor core, internally reduced and finally adjusted by the external gear to deliver an estimated final transfer speed of approx. $450\text{ RPM}$ at the wheel shaft.

		* **Kinematic Analysis and Calculation of Absolute Theoretical Speed:**
		To determine the chassis performance on the track and calibrate the lap time windows (such as the control parameter `lap_time = 4.3`), a kinematic calculation is performed based on the $6.5\text{ cm}$ ($0.065\text{ m}$) diameter of the drive wheels. We evaluate the rolling circumference ($C$) and the maximum theoretical linear speed ($V$):

	<div align="center">
	
	$$C = \pi \times 0.065\text{ m} \approx 0.2041\text{ m}$$

	</div>

	Transforming the revolutions per minute of the transmission's secondary shaft into revolutions per second and multiplying by the development of the circumference, we obtain the advance speed of the chassis:

	<div align="center">
	
	$$V = \frac{450\text{ RPM}}{60} \times 0.2041\text{ m} \approx 1.53\text{ m/s}$$
		
	</div>

	This value of $1.53\text{ m/s}$ represents the ideal limit speed of the platform. In real competition conditions, this vector is modulated via software through speed commands (`speed=90` or `80`) to absorb the static friction of the ground, the rolling resistance of the bearings, and the instantaneous current demands requested by the MegaPi when managing the change of inertia.


	- ### 3D Printed Parts:

		- **Printer:** Creality Hi and Creality K1 printers were used.

   			- **Creality Hi:** This is one of Creality's most recent proposals, designed with a strong focus on competing directly in the affordable multicolor printing market.
        
        		- Build volume (what you can print): $260 \times 260 \times 300\text{ mm}$. It is an intermediate-to-high size, excellent for robotics because it allows you to make full chassis in a single piece without having to segment them.
            
          		- Machine dimensions: $409 \times 392 \times 477\text{ mm}$ (Weight: $8.75\text{ kg}$).
  
        		It is a high-speed Cartesian printer equipped with step-servo motors on the X/Y axes to prevent step loss. Its great strength is native compatibility with the CFS (Creality Filament System), an external "filament bank" module that allows you to automatically alternate up to 4 different colors (or up to 16 if you chain 4 modules). Its maximum speed is $500\text{ m/s}$ with an acceleration of $12,000\text{ mm/s}^2$ and reaches $300^\circ\text{C}$ at the nozzle.
  
        		- **How good is it?**
  
           			* **Strengths:** Extremely rigid cast aluminum structure, 100% automatic calibration and leveling via strain sensor, and intelligent detection of tangles or filament runout. If you buy the Combo version (with the CFS), it is a brutal machine for parts that need soluble supports or combining rigid and flexible materials.
  
       				* **Weaknesses:** Since it is not enclosed from the factory (open design), printing technical materials prone to shrinking like ABS or ASA consistently can be difficult without building an external enclosure.
          
	   			- **Is it recommended for future use?**
  
   					Yes, absolutely. Being a modern platform, it has the most updated software support (Creality Print 5.1 / OrcaSlicer) and is designed under the automatic filament changing ecosystem, which is where the entire industry is heading. It is an excellent long-term investment for a workshop.

			- **Creality K1:** Originally launched as Creality's direct response to Bambu Lab's P1 series, it is a professional-grade machine designed for pure speed and demanding materials.

     			- Build volume (what you can print): $220 \times 220 \times 250\text{ mm}$. It is a standard space (slightly smaller than the Creality Hi).
        
    			- Machine dimensions: $355 \times 355 \times 480\text{ mm}$ (Weight: $12.5\text{ kg}$).
  
        		It uses a CoreXY kinematic system where the print head moves in an ultra-light manner on the X/Y axes using crossed belts, while the bed only moves down on the Z axis. Being fully enclosed with glass and acrylic panels, it retains internal heat in the print chamber. It reaches a speed of $600\text{ mm/s}$ and a massive acceleration of $20,000\text{ mm/s}^2$ thanks to its Klipper-based firmware (Creality OS).
  
   				- **How good is it?**
  
   					* **Strengths:** It is a beast for technical materials. Its enclosed chamber is perfect for printing PETG, ABS, ASA, and Nylon without suffering from warping (edge peeling). Its acceleration is almost double that of the Creality Hi, drastically reducing print times for complex mechanical parts.
  
       				* **Weaknesses:** The first units that hit the market (2023 batches) suffered from extruder (V1 version) and hotend issues. Creality corrected this in later versions (extruder with a shiny lever and Unicorn-type nozzle), so if you acquire one today, you ensure you get the corrected and mature version.
          
	   			- **Is it recommended for future use?**
  
   					Yes, but under certain conditions. It remains an exceptionally fast and robust machine for engineering parts. However, you must keep in mind that the original K1 is not natively compatible with modern multi-thread multicolor printing systems (that feature was reserved for the K2 series with the new CFS).

		- **PETG vs PLA:**

		<div align="center">

		| PETG | PLA |
		|---|---|
		| Polyethylene Terephthalate Glycol (PETG) is a petroleum-derived thermoplastic, modified with glycol to prevent crystallization and brittleness common to standard PET. It combines the printing ease of PLA with the mechanical resistance of ABS. It is characterized by its excellent toughness, chemical wear resistance, and ability to absorb impacts through slight elastic flexion, making it ideal for functional components. | Polylactic Acid (PLA) is a biodegradable thermoplastic of natural origin (derived from corn starch or sugarcane) widely used in 3D printing due to its ease of use. Stands out for its high structural rigidity and minimal thermal contraction upon cooling, which allows manufacturing parts with highly precise geometric tolerances and no deformations. However, its molecular nature makes it brittle under direct impacts. |
		| It presents high impact resistance and notable mechanical fatigue resistance. It features an elastic modulus that grants it certain structural flexibility, allowing it to withstand torsions, mechanical vibrations, and dynamic loads without suffering catastrophic fractures. It is the ideal material for robot parts exposed to collisions, tensile forces, or constant mechanical movements. | It offers excellent tensile strength and superior mechanical rigidity, meaning it does not deform or bend easily under static loads. Its main disadvantage is extreme brittleness; under abrupt mechanical stresses or continuous vibrations, it tends to crack or break suddenly instead of flexing, limiting its use in areas of high dynamic tension. |
		| It stands out for superior thermal stability, withstanding working temperatures up to 75°C or 80°C without losing its rigidity or suffering structural deformations. This allows it to be placed directly next to heatsinks, DC motors, or voltage regulators. Additionally, it possesses hydrophobic properties and high chemical resistance against alcohols, oils, greases, and degradation from weathering. | It has low thermal resistance, with a softening point (glass transition temperature) located between 50°C and 55°C. This makes it vulnerable to geometric deformation if exposed to heat dissipated by high-power motors or if the robot operates in warm environments. Likewise, its resistance to degradation by UV rays and chemical agents is limited in the long term. |
		| It requires stricter printing conditions, with nozzle temperatures from 230°C to 250°C and a mandatory heated bed between 70°C and 90°C. It is prone to generating fine strings (stringing) and requires rigorous moisture control, as it is highly hygroscopic and absorbs water from the environment quickly, degrading part quality if the filament is not stored dry. | It is the simplest material to process in the robotics workshop, requiring low nozzle temperatures (190°C - 220°C) and a moderate (50°C - 60°C) or even zero bed temperature. It does not generate harmful gases, does not suffer from warping (edge peeling), and tolerates high printing speeds with 100% layer fan ventilation, facilitating rapid prototyping of complex parts. |
		| It is used with priority in critical components subjected to physical and thermal stress. It is the right choice for front bumpers exposed to collisions, supports for DC motors that generate heat through friction, internal structures that hold heavy batteries (withstanding sudden inertia when braking or turning), and moving parts of the steering system linkage. | It is applied in the manufacturing of fixed components that demand maximum dimensional accuracy and absolute rigidity, where geometric tolerances of fittings must be millimetric. It is ideal for optical or line sensor brackets (which must not oscillate), computer vision camera cases, static mounting brackets, and test mockups where weight and screw fitment are critical. |
	
		</div>

		- **Parts:**

		<div align="center">
			
		| Component & Preview | Design & Geometry | Engineering Purpose |
		|---|---|---|
		| Battery Case <br><br><img width="400" height="400" alt="BatteryCase" src="https://github.com/user-attachments/assets/a5362844-dd0e-4073-bef8-bb034bae3ad9" /> | Designed as a vertical tower cage structured with four reinforced pillars on each side, integrated directly onto a solid mounting base with corner screw eyelets. The side walls feature large circular cutouts to minimize material weight while allowing maximum passive airflow to prevent thermal stress on the LiPo cells during high discharge rates. The top pillars include slotted retention eyelets for secure strap fastening. | Centralizes the combined mass of the battery cells vertically along the central geometric axis of the chassis. This open-cage design ensures quick access for battery replacement between runs while providing rigid structural containment against lateral inertia forces during high-speed cornering. |
		| Camera Case <br><br><img width="400" height="400" alt="CameraCase" src="https://github.com/user-attachments/assets/7adbc42b-15eb-4677-a0a4-8d9b3c98bab3" /> | A compact, rectangular protective enclosure specifically tailored to encapsulate the IMX219 (Arducam) sensor. The bottom section integrates a robust cylindrical pivot hinge featuring external locking teeth (spur gear profile) designed to mesh perfectly with a matching mounting base for mechanical angle locking. | Shields the delicate camera PCB from external debris or direct track impacts. The interlocking geared hinge allows the camera's pitch to be adjusted and mechanically locked at a precise 15-degree downward tilt angle, preventing any unwanted lens shifting caused by high-frequency chassis vibrations during operation. |
		| MegaPi Case <br><br><img width="400" height="400" alt="MegaPiBase (1)" src="https://github.com/user-attachments/assets/8db95bf2-a29a-468c-ace8-e21bb1fae9f6" /> | A robust low-profile tray equipped with four integrated, heavy-duty vertical standoffs positioned at the corners to secure the main PCB. The base plate features internal layout guides and structural clearance cuts to avoid components on the underside of the board while keeping the profile as close to the chassis as possible. | Functions as a rigid mechanical cradle for the low-level power electronics. By elevating the PCB via the 3mm integrated standoffs, it prevents electrical short-circuits with the chassis while dampening vibrations. The completely open perimeter guarantees immediate access to the motor screw terminals, power rails, and sensor ports for field maintenance. |
		| RaspberryPi Base <br><br><img width="400" height="400" alt="RaspberryPiBase (1)" src="https://github.com/user-attachments/assets/2403b708-2e1d-4360-9504-aae68c0027d1" /> | A flat, mid-level modular platform featuring four integrated corner standoffs to mount the Raspberry Pi 4 safely. The front section of the base integrates a dual-ear hinge mount equipped with internal locking teeth that mate directly with the Camera Case hinge. | Serves as a dual-purpose structural bridge. It provides a stable, elevated mount for the high-level on-board computer, ensuring optimal heat dissipation via natural convection to prevent CPU thermal throttling. Concurrently, its integrated geared mount firmly locks the camera assembly at the front, eliminating the need for extra components and saving valuable chassis space. |
		| Ultrasonic Case <br><br><img width="400" height="400" alt="UltrasonicSensorCase" src="https://github.com/user-attachments/assets/f9696c40-13e6-46b5-9712-2d7849a80005" /> | A compact, dual-barrel protective bracket custom-tailored to snugly encapsulate the transmitter and receiver cylinders of the ultrasonic sensor module. It features integrated rear mounting tabs and lower flanges for seamless mechanical coupling to the forward crossbeams of the chassis frame. | Provides a rigid, vibration-isolated housing that keeps the ultrasonic sensor perfectly perpendicular to the track's horizontal plane. This precise alignment eliminates acoustic signal distortion and wave scattering, ensuring highly accurate real-time distance measurements for obstacle detection and emergency braking maps. |

		</div>

# 2. Components

- ### Prices:

<div align="center">

| Quantity | Products | Price | Total |
|---|---|---|---|
| 1 | [Raspberry Pi 4 B](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X) | $123.99 | $123.99 |
| 1 | [Yfrobot steering chassis](https://yfrobot.com/products/steering-gear-robot) | $118.50 | $118.50 |
| 2 | [Zeee 3S Lipo Battery 2200mAh 11.1V 50C](https://www.amazon.nl/Zeee-Vrachtwagen-Vliegtuig-Quadcopter-Helikopter/dp/B0C2CHMCC3) | $50.65 | $50.65 |
| 1 | [Arducam 8MP IMX219 175°](https://www.amazon.com/Arducam-IMX219-Degree-Raspberry-Compatible/dp/B09VSVB4DT/ref=sr_1_7?crid=10W18P0RVDUOR&s=electronics&sr=1-7) | $26.99 | $26.99 |
| 4 | [Lever wire connectors](https://www.amazon.com/Conductor-Compact-Connectors-Electrical-Terminals/dp/B0D9Y5XFQC/ref=sr_1_2_sspa?sr=8-2-spons) | $9.99 | $9.99|
| 1 | [Buck Converter 3A 15W Type-C](https://www.amazon.com/-/es/Convertidor-Impermeable-Adaptador-corriente-compatible/dp/B0D2MTJQK8) | $8.79 | $8.79 |
| 1 | [MAKEBLOCK MegaPi (from mbot mega)](https://www.robotshop.com/products/makeblock-mbot-mega-robot-car-rechargeable-li-po-battery-kit?qd=c181467e2368e663479ab211142e2920) | $148.97 | $148.97 |
| 1 | [Crash Collision Sensor Module](https://www.amazon.com/-/es/Generic-detecci%C3%B3n-colisi%C3%B3n-interruptor-Arduino/dp/B0D6GZDV95) | $5.54 | $5.54 |
| 1 | [LED Traffic Light Module](https://www.amazon.com/Traffic-Light-Module-Board-Arduino/dp/B07R1KJ4DT) | $10.99| $10.99 |
| | | | **$504.41** |

</div>

- ### Description:

<div align="center">

| Photo | Description |
|---|---|
| Yfrobot kit <div  align="center"> <div  style="width:290 px"> ![halbi](https://funduinoshop.com/media/image/84/6f/82/YFROBOT-chassis-kit-mit-lenkachse-technische-zeichnung_600x600@2x.png) </div> </div>  | The modular YFROBOT 4WD chassis combines four-wheel drive with a car-like steering system to offer increased stability and precise control. Designed with dedicated mounts for controllers like Arduino or Raspberry Pi, it simplifies mechanical assembly and allows for easy integration of sensors or accessories. By reducing the complexity of designing from scratch, it serves as an ideal platform in education and competitions, allowing teams to focus directly on programming, autonomous navigation, and control systems. |
| Raspberry PI 4 B <div align="center"> <img width="293" height="172" alt="images" src="https://github.com/user-attachments/assets/5c007a1e-273e-4ce2-89a7-fa99dd9b069b" /> </div> | The Raspberry Pi 4 Model B is a powerful, credit card-sized single-board computer (SBC) developed by the Raspberry Pi Foundation. It is widely used in robotics, IoT projects, and embedded systems due to its versatility, performance, and affordable price. |
| Makeblock MegaPi <div  align="center"> ![nano](https://ardubotics.eu/10754/makeblock-mega-pi-born-to-control.jpg) </div> | The **Makeblock MegaPi** (**ATmega2560**) board was selected as the central microcontroller due to its ability to manage multiple motors and sensors simultaneously, surpassing simpler options like the Arduino Uno or Nano thanks to its plug-and-play interfaces. Although designed to stack directly on top of a Raspberry Pi, it was decided to connect it exclusively via **USB** for data transfer. This alternative optimizes space within the chassis, utilizes the MegaPi’s own power supply, and avoids exposing the main board to risks during the soldering process. |
| Zeee 3S Lipo Battery 2200mAh 11.1V 50C <div  align="center"> <div  style="width:290 px"> ![LX2-BUSB](https://m.media-amazon.com/images/I/71-SIfPk3XL._AC_UF1000,1000_QL80_.jpg) </div> | The robot utilizes a Zeee 3S LiPo battery (2200mAh, 11.1V, 50C) as a single power source, chosen for its high discharge rate and compact design that optimizes space within the chassis compared to bulkier options. This setup simplifies the system by powering both logic and motors, though it requires external voltage regulators (such as DC-DC converters) to protect sensitive components like the Raspberry Pi. Despite requiring careful handling with specific chargers to prevent hazards and extend its lifespan, it offers an excellent balance between power, size, and performance for robotics applications. |
| Steering servo mg996r <div  align="center"> ![L298N](https://cdn-global-hk.hobbyking.com/media/catalog/product/cache/10/image/9df78eab33525d08d6e5fb8d27136e95/6/2/6221_1_high_7_.jpg) </div> | Included in the YFROBOT kit to control the steering axle, the MG996R is a high-torque digital servomotor that operates via PWM signals within a range of 0° to 180°. Its metal gears grant it higher durability and strength compared to plastic servos, allowing it to withstand demanding mechanical loads. With an operating voltage range of 4.8V to 6V, it offers torque between 9.4 and 11 kg·cm and speeds up to 0.15 seconds per 60°, utilizing a standard three-pin interface fully compatible with microcontrollers like Arduino and Raspberry Pi. |
| RS380 motor <div  align="center"> ![motor](https://novatronicec.com/wp-content/uploads/2020/10/Motor-con-caja-reductora-25GA370_2.jpg) </div> | The **RS-380 motor with gearbox** assembly is a compact and versatile DC system, ideal for small robotics and light automation. On its own, the RS-380 is a small brushed motor that spins at high revolutions (between 10,000 and over 20,000 RPM depending on the voltage) but generates very little torque. The addition of the gearbox addresses this limitation by decreasing rotational speed through a series of gears, which significantly increases output torque and allows the system to move heavier mechanical loads practically. |
| ArduCam IMX219 8MP <div  align="center"> ![Encorder](https://cdn.arducam.com/wp-content/uploads/2022/04/Arducam_IMX219_MIPI_Pi_B0392-8.jpg) </div> | The **ArduCam IMX219 8MP** is a compact camera module based on the Sony IMX219 sensor—the same standard as the Raspberry Pi Camera v2—balancing resolution and performance for artificial vision and robotics projects. It connects via the **CSI** (Camera Serial Interface) interface, which guarantees high-speed, low-latency data transfer to computers like the Raspberry Pi or Jetson Nano. This design makes it an efficient and easy-to-integrate solution for embedded systems requiring real-time image processing. |
| Buck Converter 3A 15W Type-C <div  align="center"> ![camera](https://m.media-amazon.com/images/I/61pOfxNxUnL._AC_UF1000,1000_QL80_.jpg) </div> | The **3A 15W Type-C buck converter module** is a DC-DC step-down regulator that transforms high input voltages into a low, stable output with an efficiency of 85% to 95%. In this project, it was used to connect the **Zeee 3S LiPo battery** (up to 12.6V) to the **Raspberry Pi 4B**, which requires a constant supply of **5V and up to 3A**. Since direct battery voltage would damage the board, the converter safely steps down and regulates tension, protecting components against overvoltages, minimizing energy loss as heat, and ensuring stable system performance as the battery discharges. |
| Ultrasonic Sensor HC-SR04 <div  align="center"> <img width="466" height="466" alt="61CXJgLZwUL _SX466_" src="https://github.com/user-attachments/assets/1345b129-76f7-4f39-8ec2-b839398ea61b" /> </div> | The HC-SR04 ultrasonic sensor is a compact distance measurement device that operates on the sonar echo principle, ideal for obstacle avoidance in robotics. It is equipped with two transducers that emit a burst of high-frequency waves ($40\text{ kHz}$) and receive their bounce after hitting an object. By precisely calculating the time the signal takes to go and return, the module determines the linear distance in an effective range of 2 to 400 centimeters with an accuracy of 3 millimeters, providing crucial real-time data for vehicle navigation.|

</div>

- ### Sensor Arrangement and Justification:

	The design of our autonomous vehicle implements a mixed perception system composed of an artificial vision camera and three ultrasonic sensors, strategically located to cover critical navigation points on the WRO track. At the front, an ultrasonic sensor has been placed in an advanced position relative to the camera. This configuration allows for ideal synchronization between both components: while the camera processes visual information from the environment (such as detecting colors on lines and recognizing objects at medium range), the front ultrasonic sensor acts as a real-time safety and precision measure, accurately measuring the distance to obstacles immediately ahead of the vehicle before executing a braking or dodging action.

	On the other hand, for lateral control and vehicle stabilization, two additional ultrasonic sensors have been integrated, one on each side of the chassis. These side sensors are positioned longitudinally between the front and rear wheels, and vertically aligned at the height of the wheel axle. This placement is essential for the navigation algorithm, as it allows constant and symmetrical measurement of the distance to the track walls. By maintaining this height and central position, disturbances caused by chassis roll movements are minimized, ensuring that the vehicle can optimally calculate the center of the lane and maintain a straight, smooth, and precise trajectory throughout the competition.

- ### Battery:

	The Zeee 3S LiPo 11.1V 2200mAh 50C is a high-performance lithium polymer battery, designed specifically for radio control (RC) enthusiasts looking for an optimal balance between weight, size, and power. With a 3-cell (3S) configuration and a nominal voltage of 11.1V, this component provides the constant and aggressive energy needed to drive a wide variety of models, from racing drones and scale airplanes to RC land vehicles. Its 2200mAh capacity ensures a highly competitive run or flight time, allowing maximum motor performance to be squeezed out without adding excessive weight that could compromise the model's agility.

	The true strength of this battery lies in its 50C discharge rate, meaning it is capable of delivering high current peaks safely when the throttle demands it, guaranteeing explosive acceleration and immediate command response. Manufactured with high-quality materials and low internal resistance, the Zeee 3S stands out for its extended lifecycle and thermal stability during intensive use. It usually comes equipped with high-conductivity connectors (such as Deans T or XT60) and a JST-XH balance connector, facilitating safe cell-by-cell charging and direct compatibility with most smart chargers on the market.

- ### Power Budget:

<div align="center">

| Components | Quantity | Operating Voltage | Nominal/Peak Consumption | Total Consumption |
|---|---|---|---|---|
| Raspberry Pi 4 B | 1 | 5.0 V | 600 mA / 1250 mA | 1250 mA |
| Arducam 8MP IMX219 (175°) | 1 | 3.3 V (via RPi) | 250 mA | 250 mA |
| Makeblock MegaPi (Logic) | 1 | 5.0 V | 100 mA | 100 mA |
| HC-SR04 Ultrasonic Sensors | 3 | 5.0 V | 15 mA (each) | 45 mA |
| Crash Collision Sensor Module | 1 | 5.0 V | 10 mA | 10 mA |
| LED Traffic Light Module | 1 | 5.0 V | 30 mA | 30 mA |
| MG996R Steering Servomotor | 1 | 5.0 V - 6.0 V | 500 mA / 2500 mA (Stall) | 2500 mA |
| RS380 Traction Motor | 1 | 7.2 V - 12.0 V | 1200 mA / 2000 mA (Stall) | 2000 mA |
| | | | | 6,185 mA (6.18 A) |

</div>

- ### Wiring Diagram:

<div align="center">

<img width="2960" height="1625" alt="L-N-M@1 25x" src="https://github.com/user-attachments/assets/13e15df3-6f13-4d22-9dfd-a9a075e6561c" />

</div>

# 3.  Software

- ### Utilities:

	- **Color Detector:** It is an interactive visual calibration tool designed to segment and isolate specific colors in real time using the LAB color space (Luminance, A, and B) and Gaussian blur filters. The system captures the video stream from a Picamera2, applies morphological transformations of erosion and dilation to clean image noise, and generates a binary mask based on maximum and minimum thresholds adjustable via sliders in a graphical user interface (GUI) built with CustomTkinter. Its main function is to preset color signatures (such as red, green, blue, or black) and export these optimal ranges to a JSON configuration file so that the robot can recognize objects or lines stably under different lighting conditions.

	- **ROI Detector:** It is a spatial configuration utility based on OpenCV that allows delimiting custom "Regions of Interest" (ROI) over the camera's video transmission through mouse clicks and drags. The script scales the original frame proportionally within a centered canvas with constant black borders, allowing the user to draw multiple quadrants and dynamically view their dimensions in pixels. Its primary purpose is to clear the cache with the 'C' key or end the capture with the 'ESC' key to trigger a Tkinter popup window that automatically exports the coordinates $(x_1, y_1, x_2, y_2)$ structured as a list of objects into a native Python file (.py), isolating the specific visual analysis zones where the robot must process information (such as the floor line) and ignoring environment noise.

- ### MegaPiController:

- ### Arduino Controller:

	- Open Challenge:

		- Strategy:
  
		    To meet the Open Challenge requirements, a software architecture based on a high-frequency control loop was designed and implemented, divided into four strategic pillars: Visual Perception, Trajectory Control (PID), Corner Navigation, and Active Safety.
		
		- ROIS:
 
    		To optimize computational processing and avoid false positives from the surroundings, the camera segments the space into two specific lateral ROIs (roi and roi2). These regions actively look for the black lines that delimit the track walls or lanes.

		- Loop Counter:
 
   			The area of key colors is processed in the first instances. If an orange color area larger than a critical threshold of 200px is detected, the robot assumes a right turn orientation; if the color is blue, it configures to turn left.

		- Flowchart:

	- Obstacle Challenge:

		- Strategy:
		
		- ROIS:

		- Loop Counter:

		- Flowchart:

# 4. Challenges:

- ### Hardware Problems

	**Objective:** Complete three laps autonomously in dynamically configured circuits.

	### Spacing Problems
	During the early development of *Halbi the Green*, issues arose regarding component positioning within the base chassis (unmodified). Because the components occupied more space than available, the problem was temporarily resolved by securing them 	with electrical tape. While this worked provisionally, it was not a viable long-term solution. 

	Therefor, it was decided to implement a series of 3D-printed bases designed to add **two additional levels** to the vehicle and **three complementary supports** (two lateral and one frontal) to position the ultrasonic sensors, which originally had no assigned place.

	More specifically, the spacing issues and their respective solutions were as follows:
	
	* **Space occupied by batteries:** * *Problem:* They occupied too much volume in the chassis and did not leave room to position components comfortably.
  
    	* *Solution:* A custom base was designed to position them in the center of the robot, and the upper floor was constructed on top of this structure.
      
	* **Ultrasonic sensor anchoring:** * *Problem:* They had no designated mounting points on the original chassis.
  
    	* *Solution:* 3 printed bases were designed to attach to 3 sides of the chassis.
      
    	* *Technical note:* This solution was not completely ideal, as these bases protrude slightly from the structure, causing mechanical jams when the vehicle passes very close to a corner.
      
	* **Camera and Controller Location:** * *Problem:* There was no physical space to place the camera or the processing board.
  
    	* *Solution:* A dedicated support for the Raspberry Pi and the camera was designed on top of the battery base. The camera includes a base with an adjustable angle to tweak the lens viewpoint comfortably and precisely.

	### Connection Problems (Wiring)

	* **Problem:** Having loose and exposed wires caused them to get stuck constantly in the environment and even knock down circuit obstacles on some occasions.
  
	* **Solution:** Connections were completely reorganized to eliminate wire loops and protruding parts.
  
- ### Software Problems:

	- a
