``` For better visualization, it is recommended to view the repository on a computer ```

# WRO 2026 Future Engineers – LNM

<div align="center">
	
<img width="840" height="407" alt="WhatsApp Image 2026-06-19 at 11 51 57 PM" src="https://github.com/user-attachments/assets/cee364df-eeba-4338-8f2a-14949adb755b" />

</div>

Welcome to the GitHub repository of **Team LNM**, formerly known as Ars Machina, competing in the **World Robot Olympiad™ (WRO®) Future Engineers 2026** category. Our team consists of David Wang and Pedro Catamo, who have designed a compact and innovative autonomous vehicle to tackle the dynamic challenges of the WRO 2026 competition.

## **Index**

**1. [Folder structure](#folder-structure)**

**2. [The team](#the-team)**

**3. [Our robot](#our-robot)**

**4. [Electronic systems](#electronic-systems)**

**5. [Mechanical systems](#mechanical-systems)**

**5. [Software architecture](#software-architecture)**

---

## **Folder structure** <a id="folder-structure"></a>

This is the folder structure of our repository:

| Folder | Technical content | Detailed documentation |
|---|---|---|
| **models** | **3D Designs**<br>• Car parts| [Explore the 3D models](models/README.md) |
| **schemes** | **Electrical systems**<br>• Wiring diagrams<br>• Power management<br>• Component schematics| [Explore the schemes and wiring documentation](schemes/README.md) |
| **src** | **Software algorithms**<br>• Navigation logic<br>• Sensor fusion<br>• Control systems | [Explore the software and algorithms documentation](src/README.md) |
| **t-photos** | **Team documentation**<br>• Member profiles | [Explore the team photos documentation](t-photos/README.md) |
| **v-photos** | **Vehicle documentation**<br>• Views from multiple angles | [Explore the vehicle photos documentation](v-photos/README.md) |
| **video** | **Performance validation**<br>• Challenge demonstrations<br>• Engineering tests | [Explore the performance videos documentation](video/README.md) |

---

## **The Team** <a id="the-team"></a>

<div align="center">
	
<img width="1280" height="720" alt="Team_pic (1)" src="https://github.com/user-attachments/assets/156c3c29-799e-44e6-a7f0-629da61873b8" />

</div>

### **Members:**

- **David Wang**
   
	Born on: 01/04/2011 (15 years old)

	Studies: 3rd year at U.E.C. Eduardo Blanco

  	Gmail: davidwangwu104@gmail.com
  	  
- **Pedro Catamo**
   
 	Born on: 28/01/2009 (17 years old)
   
  	Studies: 5th year at U.E.C. Eduardo Blanco
   
 	 Gmail: pedrocatamo.2009@gmail.com

- ### **Coach:**

- **Jesús Alcalá**
   
  Born on: 18/11/2005 (21 years old)
   
  Studies: Computer Engineering & Software Engineering
   
  Gmail: Jdam50002@gmail.com

---

### Previous designs:
  
<div align="center">
	
| Photo | Name | Description |
|---|---|---|
| <img width="920" height="920" alt="Captura de pantalla 2026-06-17 185504" src="https://github.com/user-attachments/assets/36166165-a542-42d6-a771-41a60693a399" /> | **Cyber Cooper** | In 2023 we planned to design the car from scratch, modeling and 3D printing our own parts, including the chassis and steering system. Although it seemed like a good idea at first, as we progressed we started running into one problem after another, and realized our current design would bring us more difficulties. In the end, we did everything we could within the time constraints we had. |
| <img width="920" height="920" alt="front2" src="https://github.com/user-attachments/assets/ce130237-cc0b-4aa9-a620-0aea287408c2" /> | **Cooper** | In 2024 we developed a chassis with 3D parts structured in two levels. The lower level housed the sensors and low-level electronics, while the upper level held the batteries and the Raspberry Pi 3 to optimize space. Although we achieved great aesthetic and functional progress, we suffered harsh lessons on the track: the excessive weight caused the rear transmission couplings to bend, which in turn generated severe mechanical friction problems between the 3D printed parts. |
| <img width="920" height="920" alt="front" src="https://github.com/user-attachments/assets/804b3d7f-3500-4351-a917-ccf781029804" /> | **Halbi** | In 2025 taking into account the resources we had at that moment, our main idea was to redesign the Cybercooper, modifying the existing base and strategy and using better electronic components; we started printing the new parts with white material and thinking about better ways to mount the car's steering system. In the end, we decided to use a prefabricated base for the chassis; the main reason was to save time (and headaches) with the mechanical design, which allowed us to spend more time on electronics and programming. |
| <img width="920" height="920" alt="WhatsApp Image 2026-06-18 at 7 39 40 PM" src="https://github.com/user-attachments/assets/ca9f62ff-7b8b-452a-97de-95ebf12dc0ef" /> | **The Fridge** | In 2025 unlike previous models that belonged to our coach, "The Fridge" was a design built entirely by us. Here we made the leap to Ackermann geometry and 3D printed the vast majority of the parts. Motively, we used a DC motor with a coupled gear to drive both wheels. Physically we installed 3 ultrasonic sensors, a Raspberry Pi 4, and an MPU6050 gyroscope, but due to lack of time and severe configuration problems, the Raspberry and IMU remained as dead weight and we ended up controlling everything solely from the MegaPi. We suffered a lot: the 3D printed steering parts broke constantly due to stress, and programming autonomous navigation in Arduino relying purely on ultrasonic bounces was almost impossible. Being honest, it ended up being the worst project of the three. |

</div>

---

# 1- Mobility and design

 - ### Halbi The Green: <a id="our-robot"></a>

    - ### Photos of the vehicle:

	<div align="center">

	| | **Different angles of the car** | |
	|---|---|---|
	| **Top** | **Right** | **Left** |
	| <img width="560" height="580" alt="Upper-Pov" src="https://github.com/user-attachments/assets/74863cc8-5128-49cf-845e-0f087c50bcf1" /> | <img width="560" height="580" alt="RightSide-Pov" src="https://github.com/user-attachments/assets/8b9c2020-cc18-441f-9152-c86d9a233b10" /> | <img width="560" height="580" alt="LeftSide-Pov" src="https://github.com/user-attachments/assets/cdbabe27-6e45-4dab-98e6-e63b24ed7371" /> |
	|**Front** | **Rear** | **Free** |
	| <img width="560" height="580" alt="Front-Pov" src="https://github.com/user-attachments/assets/d9b65dd5-ca97-4087-ba20-77f7cbeb4bf6" /> | <img width="560" height="580" alt="Back-Pov" src="https://github.com/user-attachments/assets/dd1737be-1173-4cae-9229-25821f05dc22" /> | <img width="560" height="580" alt="604003001-cc130bf0-8547-48cc-847e-28dbd9029fba" src="https://github.com/user-attachments/assets/f1dc12a1-dbfc-46f3-9a21-a679aa1aa3db" /> |
	
    </div>

	- ### Main mechanical specifications: <a id="mechanical-systems"></a>

		- **Total dimensions: 24.4 cm (length) × 15.4 cm (width) × 15.9 cm (height).**
		- **Car weight: approximately 1.2kg.**
		- **Traction system: Biphasic Mechanical Rear-Wheel Drive.**
		- **Steering system: Ackermann Geometry.**
	
	- ### Ackermann Steering Mechanism

		The vehicle utilizes precise geometry based on the **Ackermann Steering Principle** to conquer tight corners with zero lateral slip and minimal tire wear.

		* **The Physics Behind the Principle:** When a vehicle enters a curve, the inner front wheel follows a tighter and smaller concentric radius than the outer wheel. If both wheels turned at exactly the same angle, the tires would fight each other, causing the outer tire to drag, lose mechanical grip, and introduce severe structural vibrations that would ruin the visual tracking of the lanes. To resolve this, the mechanical geometry forces the inner wheel to pivot at a deeper angle than the outer wheel, ensuring all four wheels rotate around a single common Instantaneous Center of Curvature (ICC).

		* **The Mechanical Execution:** A high-torque **MG996R** digital servo ($11 \text{ kg}\cdot\text{cm}$ of torque) is anchored to the front bulkhead via a custom-machined L-shaped aluminum bracket to eliminate structural deflection. The servo arm drives a dual-link steering rack connected to asymmetric tie rods and steering knuckles. The steering arms are angled inward, pointing to the center of the rear axle, completing the classic "Ackermann Trapezoid". This exact mechanical design converts the servo's linear displacement into non-linear wheel angles automatically.

		* **Digital Control and Calibration:** The MG996R is controlled by a continuous, jitter-free hardware PWM pulse train at $50\text{Hz}$ directly from the MegaPi microcontroller. The steering is rigidly mapped and calibrated to a software deadband where $80^\circ$ represents absolute geometric center. Mechanical endpoints are software-limited between $40^\circ$ (Maximum Left) and $105^\circ$ (Maximum Right) to prevent the steering links from reaching mechanical lock or forcing the motor's stall limits.

	<div align="center">

	Imagen

	</div>

	- ### What is Ackermann Geometry? 

		Understanding Ackermann Mathematics and Kinematics, in traditional mobile robotics (like the robots in the *RoboMission* category), differential drive is used because it is mathematically simple: you vary the speed of two motors and the robot turns on its own axis. However, at high speeds, differential drive is unstable and unpredictable.

		**Ackermann Geometry** solves this through a purely mechanical principle. For a vehicle to turn without sliding laterally, the extended lines from the axes of all wheels must intersect at a single point in space: the **Instantaneous Center of Rotation (ICR)** or ICC.

		The fundamental mathematical equation governing this kinematics is:
		<div align="center">
	
		$$\cot(\theta_{\text{out}}) - \cot(\theta_{\text{in}}) = \frac{w}{L}$$
		
		</div>
		
		Where:
		
		* $\theta_{\text{in}}$ is the steering angle of the inner wheel.*
		* $\theta_{\text{out}}$ is the steering angle of the outer wheel.*
		* $w$ is the track width (distance between the front wheels).*
		* $L$ is the wheelbase (distance between the front and rear axles).*

		Since the cotangent grows faster at small angles, this relationship mechanically forces $\theta_{\text{in}} > \theta_{\text{out}}$ automatically in any curve, opening the angle of the outer wheel so it draws a larger circle.

		<div align="center">
  
		<img width="567" height="600" alt="17523247_203569336801744_2788986523412924047_n" src="https://github.com/user-attachments/assets/c36a271c-b45c-492a-805e-b107851429cd" />
		
		</div>

	- ### 2WD Electronic Propulsion with Biphasic Mechanical Transmission 

		The platform's driving force is generated by a high-performance rear-wheel drive (2WD) system, which breaks away from traditional direct-drive schemes by integrating a two-speed geared mechanical transmission using spur gears.

		* **Transmission System Architecture:** Unlike common configurations that attach the wheel directly to the motor's gearbox, this design mounts the RS380 motor in a parallel upper arrangement on a rigid support block. Power is transferred from the primary motor shaft to a secondary lower drive shaft via an exposed spur gear train. This interchangeable two-speed mechanical system allows the robot to be configured according to the demands of the track:
  		1. **Force/Torque Ratio (First Gear):** Optimizes the gear reduction to achieve maximum acceleration and millimeter control in tight corners or obstacles, ideal for winding sections. 
  		2. **Top Speed Ratio (Second Gear):** Reduces the loss of revolutions to take advantage of linear inertia on long straights, ensuring a high cruising speed without saturating electrical consumption.

		<div align="center">
  
		<img width="515" height="218" alt="Sistema de transmision de 2 velocidades K-O-M-R-A-D" src="https://github.com/user-attachments/assets/da8175e6-313d-42d6-bd3b-b1318082536f" />
		
		</div>

		* **Motor Technical Specifications (RS380):** The power block relies on brushed DC motors with magnets, selected specifically for their dynamic response curve and tolerance to transient load spikes.

	    * **Nominal Voltage:** $12\text{V}$ (Operating at a nominal cell voltage of $11.1\text{V}$ using a 3S LiPo battery to ensure thermal stability).
   
 		* **No-load Current:** $0.3\text{A}$ | **Stall Current:** $3\text{A}$ protection on the driver.
   
 		* **Factory Rotation Speed:** $15000\text{ RPM}$ at the motor core, internally reduced and finally adjusted by the external gear to deliver an estimated final transfer speed of approx. $450\text{ RPM}$ at the wheel axle.

		* **Kinematic Analysis and Theoretical Absolute Speed Calculation:**
		To determine the chassis performance on the track and calibrate the lap time windows (such as the control parameter `lap_time = 4.3`), the kinematic calculation is performed based on the $6.5\text{ cm}$ ($0.065\text{ m}$) drive wheel diameter. We evaluate the rolling circumference ($C$) and the theoretical maximum linear velocity ($V$):

	<div align="center">
	
	$$C = \pi \times 0.065\text{ m} \approx 0.2041\text{ m}$$

	</div>

	Transforming the revolutions per minute of the transmission's secondary shaft to revolutions per second and multiplying by the circumference development, we obtain the chassis's forward speed:

	<div align="center">
	
	$$V = \frac{450\text{ RPM}}{60} \times 0.2041\text{ m} \approx 1.53\text{ m/s}$$
		
	</div>

	This value of $1.53\text{ m/s}$ represents the ideal limit speed of the platform. In real competition conditions, this vector is modulated by software through speed commands (`speed = 90` or `80`) to absorb the static friction of the floor, the rolling resistance of the bearings, and the instantaneous current demands requested by the MegaPi when managing the change of inertia.


	- ### 3D Printed Parts:

   		- #### **Parts:**

		<div align="center">
			
		| Component & Preview | Design & Geometry | Engineering Purpose |
		|---|---|---|
		| **Battery Case** <br><br><img width="400" height="400" alt="BatteryCase" src="https://github.com/user-attachments/assets/a5362844-dd0e-4073-bef8-bb034bae3ad9" /> | Designed as a vertical tower cage structured with four reinforced pillars on each side, integrated directly onto a solid mounting base with screw eyelets at the corners. The side walls feature large circular cutouts to minimize material weight while allowing maximum passive airflow to prevent thermal stress on the LiPo cells during high discharge rates. The top pillar includes slotted retention eyelets for secure strap fastening. | Centralizes the combined mass of the battery cells vertically along the chassis's geometric center axis. This open-cage design ensures quick access for battery replacement between races while providing rigid structural containment against lateral inertia forces during high-speed turns. |
		| **Camera Case** <br><br><img width="400" height="400" alt="CameraCase" src="https://github.com/user-attachments/assets/7adbc42b-15eb-4677-a0a4-8d9b3c98bab3" /> | A compact rectangular protective housing specifically designed to encapsulate the IMX219 (Arducam) sensor. The lower section integrates a robust cylindrical pivot hinge featuring external locking teeth (spur gear profile) designed to mesh perfectly with a corresponding mounting base for mechanical angle locking. | Protects the delicate camera PCB from external debris or direct impacts on the track. The interlocking geared hinge allows the camera's tilt angle to be adjusted and mechanically locked at a precise 15-degree downward angle, preventing any unwanted shifts in the lens caused by high-frequency chassis vibrations during operation. |
		| **MegaPi Case** <br><br><img width="400" height="400" alt="MegaPiBase (1)" src="https://github.com/user-attachments/assets/8db95bf2-a29a-468c-ace8-e21bb1fae9f6" /> | A sturdy low-profile tray equipped with four heavy-duty integrated vertical standoffs positioned at the corners to secure the main PCB. The base plate features internal routing guides and structural clearance cutouts to avoid components on the bottom of the board, keeping the profile as close to the chassis as possible. | Functions as a rigid mechanical cradle for the low-level power electronics. By elevating the PCB using the integrated 3 mm standoffs, it prevents electrical short circuits with the chassis while dampening vibrations. The fully open perimeter ensures immediate access to motor screw terminals, power rails, and sensor ports for field maintenance. |
		| **RaspberryPi Base** <br><br><img width="400" height="400" alt="RaspberryPiBase (1)" src="https://github.com/user-attachments/assets/2403b708-2e1d-4360-9504-aae68c0027d1" /> | A flat, mid-level modular platform featuring four integrated corner standoffs to securely mount the Raspberry Pi 4. The front section of the base integrates a double-ear hinge mount equipped with internal locking teeth that mate directly with the camera housing hinge (Camera Case). | Serves as a dual-purpose structural bridge. It provides a stable, elevated mount for the high-level onboard computer, ensuring optimal heat dissipation through natural convection to prevent CPU thermal throttling. At the same time, its integrated geared mount firmly locks the camera assembly at the front, eliminating the need for additional components and saving valuable chassis space. |
		| **Ultrasonic Case** <br><br><img width="400" height="400" alt="UltrasonicSensorCase" src="https://github.com/user-attachments/assets/f9696c40-13e6-46b5-9712-2d7849a80005" /> | A custom-made compact double-barrel protective mount to tightly encapsulate the transmitter and receiver cylinders of the ultrasonic sensor module. Features integrated rear mounting tabs and lower flanges for seamless mechanical attachment to the front crossbeams of the chassis structure. | Provides a rigid, vibration-isolated housing that keeps the ultrasonic sensor perfectly perpendicular to the track's horizontal plane. This precise alignment eliminates acoustic signal distortion and wave scattering, ensuring highly accurate real-time distance measurements for obstacle detection and emergency braking maps. |

		</div>

		- #### **Printer:** The Creality Hi and Creality K1 printers were used.

   			- **Creality Hi:** It is one of Creality's most recent proposals, designed with a strong focus on competing directly in the accessible multi-color printing market.
        
        		- **Build volume (what you can print):** $260 \times 260 \times 300\text{ mm}$. It is a medium-high size, excellent for robotics because it allows you to make complete chassis in one piece without having to segment them.
            
          		- **Machine dimensions:** $409 \times 392 \times 477\text{ mm}$ (Weight: $8.75\text{ kg}$).
  
        		It is a high-speed Cartesian printer equipped with step-servo motors on the X/Y axes to prevent step loss. Its greatest strength is its native compatibility with the CFS (Creality Filament System), an external "filament bank" type module that allows you to automatically alternate up to 4 different colors (or up to 16 if you chain 4 modules). Its maximum speed is $500\text{ m/s}$ with an acceleration of $12,000\text{ mm/s}^2$ and it reaches $300^\circ\text{C}$ at the nozzle.
  
        		- **How good is it?**
  
           			* **Strengths:** Extremely rigid cast aluminum structure, 100% automatic calibration and leveling via strain sensor, and smart detection of tangles or filament runout. If you buy the Combo version (with the CFS), it is a brutal machine for parts that need soluble supports or combining rigid and flexible materials.
  
       				* **Weaknesses:** By not being enclosed from the factory (open design), consistently printing technical materials prone to shrinking like ABS or ASA can be complicated without building an external enclosure for it.
          
	   			- **Is it recommended for future use?**
  
   					Yes, absolutely. Being a modern platform, it has the most updated software support (Creality Print 5.1 / OrcaSlicer) and is designed under the automatic filament change ecosystem, which is where the whole industry is moving. It is an excellent long-term investment for a workshop.

			- **Creality K1:** Originally launched as Creality's direct response to Bambu Lab's P1 series, it is a professional-level machine designed for pure speed and demanding materials.

     			- **Build volume (what you can print):** $220 \times 220 \times 250\text{ mm}$. It is a standard space (slightly smaller than the Creality Hi).
        
    			- **Machine dimensions:** $355 \times 355 \times 480\text{ mm}$ (Weight: $12.5\text{ kg}$).
  
        		It uses a CoreXY kinematic system where the print head moves ultra-lightly on the X/Y axes using crossed belts, while the bed only drops on the Z axis. Being completely enclosed with glass and acrylic panels, it retains internal heat in the print chamber. It reaches a speed of $600\text{ mm/s}$ and a massive acceleration of $20,000\text{ mm/s}^2$ thanks to its Klipper-based firmware (Creality OS).
  
   				- **How good is it?**
  
   					* **Strengths:** It is a beast for technical materials. Its enclosed chamber is perfect for printing PETG, ABS, ASA, and Nylon without suffering warping (edge lifting). Its acceleration is almost double that of the Creality Hi, drastically reducing printing times for complex mechanical parts.
  
       				* **Weaknesses:** The first units that hit the market (2023 batches) suffered from problems in the extruder (V1 version) and in the hotend. Creality corrected this in later versions (extruder with shiny lever and Unicorn-type nozzle), so if you acquire one today, you make sure to have the corrected and mature version.
          
	   			- **Is it recommended for future use?**
  
   					Yes, but under certain conditions. It remains an exceptionally fast and robust machine for engineering parts. However, you must keep in mind that the original K1 is not natively compatible with modern multi-thread multi-color printing systems (that feature was reserved for the K2 series with the new CFS).

		- #### **PETG vs PLA:**

		<div align="center">

		|  | PETG | PLA |
		|---|---|---|
		| **Durability and Resistance** | High durability and superior toughness: Being modified with glycol, PETG prevents polymer crystallization, resulting in a highly tough material. Under mechanical impact stresses, its molecular chains have the necessary flexibility to deform elastically and absorb the kinetic energy of the crash. This prevents crack propagation, making it ideal for parts exposed to continuous collisions. | Low durability to dynamic loads: PLA has a rigid and crystalline molecular structure that gives it high surface hardness, but it lacks the ability to dissipate energy elastically. Faced with direct collisions or sudden impacts against track edges, the material stresses its inter-layer bonds and tends to brittle fracture, breaking suddenly and catastrophically instead of flexing. |
		| **Thermal Resistance and Stability** | Excellent thermal immunity: Maintains its structural integrity and mechanical rigidity in working environments up to 75°C to 80°C without experiencing softening or geometric distortion. This property allows it to be safely mounted as a direct support for the drivetrain or electronic boards, resisting the heat generated by mechanical friction and current spikes without yielding. | Vulnerable to thermal stress: Its glass transition temperature (softening point) is critically low, situated between 50°C and 55°C. If used in components in direct contact with DC motors under heavy load or voltage regulators that dissipate heat by conduction, PLA loses its rigidity quickly, suffering permanent geometric deformations that uncalibrate the chassis. |
		| **Structural Rigidity and Flexing** | Moderate elastic modulus (Elastic flexibility): It has a semi-rigid nature that allows it to withstand mechanical vibrations, torsions, and continuous dynamic loads without suffering material fatigue. Although it yields slightly under extreme forces before breaking, this structural flexibility absorbs terrain oscillations, protecting internal components. | Very high elastic modulus (Absolute rigidity): It presents superior flexural strength, meaning it does not bend or deform under moderate static loads. This lack of elastic flexibility is a technical advantage for static robot parts that need to maintain a fixed and invariable position, neutralizing any parasitic bending or buckling. |
		| **Chemical and Environmental Resistance** | High chemical inertness and hydrophobicity: It is chemically inert and exhibits outstanding resistance to oils, greases, mechanical lubricants, and cleaning alcohols. Being completely hydrophobic, it is not weakened by environmental humidity after printing, and its high stability against UV radiation ensures the parts keep their mechanical properties intact. | Sensitive to long-term degradation: Being a biopolymer derived from organic sources, it is prone to accelerated degradation under continuous exposure to UV rays or drastic humidity changes. Furthermore, its chemical resistance against external agents like alcohols, oils, or hardware lubricants is limited, which can weaken the part's walls over time. |
		| **Dimensional Accuracy and Fittings** | Moderate tolerances and prone to stringing: Requiring higher extrusion temperatures, the material experiences greater thermal contraction when cooling, demanding flow calibration to avoid dimensional variations in millimeter fittings. Also, its high viscosity tends to generate stringing (fine threads) that require post-processing in areas of fine mechanical movement. | Perfect geometric tolerances: Due to its extremely low thermal contraction when cooling, PLA stands out for millimeter dimensional stability. It allows printing threads, bearing fits, and fine mechanical joints with practically zero tolerance errors, ensuring parts fit exactly and tightly from the first prototype. |
	
		</div>

# 2. Components <a id="electronic-systems"></a>

- ### Prices:

<div align="center">

| Quantity | Products | Price | Total |
|---|---|---|---|
| 1 | [Raspberry Pi 4 B](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X) | $123.99 | $123.99 |
| 1 | [Yfrobot steering chassis](https://yfrobot.com/products/steering-gear-robot) | $118.50 | $118.50 |
| 2 | [Zeee 3S Lipo Battery 2200mAh 11.1V 50C](https://www.amazon.nl/Zeee-Vrachtwagen-Vliegtuig-Quadcopter-Helikopter/dp/B0C2CHMCC3) | $50.65 | $101.3 |
| 1 | [Arducam 8MP IMX219 175°](https://www.amazon.com/Arducam-IMX219-Degree-Raspberry-Compatible/dp/B09VSVB4DT/ref=sr_1_7?crid=10W18P0RVDUOR&s=electronics&sr=1-7) | $26.99 | $26.99 |
| 4 | [Lever wire connectors](https://www.amazon.com/Conductor-Compact-Connectors-Electrical-Terminals/dp/B0D9Y5XFQC/ref=sr_1_2_sspa?sr=8-2-spons) | $9.99 | $39.96 |
| 1 | [Buck Converter 3A 15W Type-C](https://www.amazon.com/-/es/Convertidor-Impermeable-Adaptador-corriente-compatible/dp/B0D2MTJQK8) | $8.79 | $8.79 |
| 1 | [MAKEBLOCK MegaPi (from mbot mega)](https://www.robotshop.com/products/makeblock-mbot-mega-robot-car-rechargeable-li-po-battery-kit?qd=c181467e2368e663479ab211142e2920) | $148.97 | $148.97 |
| 1 | [Crash Collision Sensor Module](https://www.amazon.com/-/es/Generic-detecci%C3%B3n-colisi%C3%B3n-interruptor-Arduino/dp/B0D6GZDV95) | $5.54 | $5.54 |
| 1 | [LED Traffic Light Module](https://www.amazon.com/Traffic-Light-Module-Board-Arduino/dp/B07R1KJ4DT) | $10.99| $10.99 |
| 2 | [Vl53l0x-v2 Sensor](https://articulo.mercadolibre.com.ve/MLV-724811982-ic-vl53l0x-v2-sensor-tiempo-vuelo-laser-a-distancia-_JM) | $5 | $10 |
| 1 | [HiLetgo DC-DC Step Down XL4015](https://www.amazon.com/-/es/HiLetgo-alimentaci%C3%B3n-ajustable-pilares-volt%C3%ADmetro/dp/B00LTSC1YK) | $7.99 | $7.99 |
| | | | **$603.02** |

</div>

- ### Description:

<div align="center">

| Photo | Description |
|---|---|
| **Yfrobot kit** <div  align="center"> <div  style="width:290 px"> ![halbi](https://funduinoshop.com/media/image/84/6f/82/YFROBOT-chassis-kit-mit-lenkachse-technische-zeichnung_600x600@2x.png) </div> </div>  | The YFROBOT 4WD modular chassis combines four-wheel drive with car-like steering to offer greater stability and precise control. Designed with specific mounts for controllers like Arduino or Raspberry Pi, it simplifies mechanical assembly and allows sensors or accessories to be added easily. By reducing the complexity of designing from scratch, it serves as an ideal platform in education and competitions so teams can focus directly on programming, autonomous navigation, and control systems. |
| **Raspberry PI 4 B** <div align="center"> <img width="293" height="172" alt="images" src="https://github.com/user-attachments/assets/5c007a1e-273e-4ce2-89a7-fa99dd9b069b" /> </div> | The Raspberry Pi 4 Model B is a powerful credit-card-sized single-board computer (SBC) developed by the Raspberry Pi Foundation. It is widely used in robotics, IoT projects, and embedded systems due to its versatility, performance, and affordable price. |
| **Makeblock MegaPi** <div  align="center"> ![nano](https://ardubotics.eu/10754/makeblock-mega-pi-born-to-control.jpg) </div> | The **Makeblock MegaPi** (**ATmega2560**) board was selected as the central microcontroller for its ability to manage multiple motors and sensors simultaneously, outperforming options like Arduino Uno or Nano thanks to its plug-and-play interfaces. Although it is designed to mate directly on top of a Raspberry Pi, we chose to connect it only via **USB** for data transfer. This alternative optimizes chassis space, takes advantage of the MegaPi's own power supply, and avoids exposing the main board to risks during the soldering process. |
| **Zeee 3S Lipo Battery 2200mAh 11.1V 50C** <div  align="center"> <div  style="width:290 px"> ![LX2-BUSB](https://m.media-amazon.com/images/I/71-SIfPk3XL._AC_UF1000,1000_QL80_.jpg) </div> | The robot uses a Zeee 3S LiPo battery (2200mAh, 11.1V, 50C) as a single power source, chosen for its high discharge rate and a compact design that optimizes space in the chassis compared to bulkier options. This configuration simplifies the system by powering both the logic and the motors, although it requires the use of external voltage regulators (like DC-DC converters) to protect sensitive components like the Raspberry Pi. Despite requiring careful handling with specific chargers to avoid risks and prolong its life, it offers an excellent balance between power, size, and performance for robotic applications. |
| **Steering servo mg996r** <div  align="center"> ![L298N](https://cdn-global-hk.hobbyking.com/media/catalog/product/cache/10/image/9df78eab33525d08d6e5fb8d27136e95/6/2/6221_1_high_7_.jpg) </div> | Included in the YFROBOT kit to control the steering axle, the MG996R is a high-torque digital servomotor that operates via PWM signals in a 0° to 180° range. Its metal gearing gives it greater durability and strength compared to plastic servos, allowing it to withstand demanding mechanical loads. With an operating range of 4.8V to 6V, it offers a torque between 9.4 and 11 kg·cm and speeds up to 0.15 seconds per 60°, using a standard three-pin interface fully compatible with microcontrollers like Arduino and Raspberry Pi. |
| **RS380 motor** <div  align="center"> ![motor](https://novatronicec.com/wp-content/uploads/2020/10/Motor-con-caja-reductora-25GA370_2.jpg) </div> | The RS-380 motor assembly with reduction gearbox is a compact and versatile direct current system, ideal for small robotics and light automation. On its own, the RS-380 is a small brushed motor that spins at high revolutions (between 10,000 and over 20,000 RPM depending on voltage) but generates very little torque. The addition of the reduction gearbox solves this limitation by decreasing the rotation speed through a series of gears, significantly increasing the output torque and allowing the system to move heavier mechanical loads practically. |
| **ArduCam IMX219 8MP** <div  align="center"> ![Encorder](https://cdn-arducam.com/wp-content/uploads/2022/04/Arducam_IMX219_MIPI_Pi_B0392-8.jpg) </div> | The 8MP ArduCam IMX219 is a compact camera module based on the Sony IMX219 sensor, the same standard as the Raspberry Pi Camera v2, which balances resolution and performance for computer vision and robotics projects. It connects via the CSI (Camera Serial Interface), ensuring high-speed, low-latency data transfer to computers like Raspberry Pi or Jetson Nano. This design makes it an efficient and easy-to-integrate solution for embedded systems requiring real-time image processing. |
| **Buck Converter 3A 15W Type-C** <div  align="center"> ![camera](https://m.media-amazon.com/images/I/61pOfxNxUnL._AC_UF1000,1000_QL80_.jpg) </div> | The **3A, 15W Type-C buck converter** module is a DC-DC step-down regulator that transforms high input voltages into a low, stable output with an efficiency of 85 to 95%. In this project, it was used to connect the **Zeee 3S LiPo** battery (up to 12.6V) to the **Raspberry Pi 4B**, which demands a constant supply of **5V and up to 3A**. Since the direct battery voltage would damage the board, the converter safely reduces and regulates the voltage, protecting components against overvoltages, minimizing energy losses through heat, and ensuring stable system performance as the battery discharges. |
| **Ultrasonic Sensor HC-SR04** <div  align="center"> <img width="466" height="466" alt="61CXJgLZwUL _SX466_" src="https://github.com/user-attachments/assets/1345b129-76f7-4f39-8ec2-b839398ea61b" /> </div> | The HC-SR04 ultrasonic sensor is a compact distance measurement device that operates on the sonar echo principle, ideal for obstacle avoidance in robotics. It is equipped with two transducers that emit a high-frequency wave burst ($40\text{ kHz}$) and receive its bounce after hitting an object. By accurately calculating the time it takes for the signal to travel back and forth, the module determines the linear distance in an effective range of 2 to 400 centimeters with a precision of 3 millimeters, providing crucial real-time data for vehicle navigation.|
| **Vl53l0x-v2 Sensor** <div  align="center"> <img width="525" height="478" alt="D_NQ_NP_2X_916413-MLV51649751397_092022-F" src="https://github.com/user-attachments/assets/c3c39671-3595-4e15-aefc-0836d1a81e33" /> </div> | It is a Time of Flight (ToF) laser distance sensor that measures distances up to 2 meters with millimeter precision by emitting an invisible 940 nm infrared pulse. Unlike traditional sensors, it calculates the exact time it takes for the light to bounce off the object, allowing it to provide stable readings regardless of the color, reflection, or texture of the surface. It features an I²C communication interface, is compatible with 3.3V and 5V voltages, and is ideal for robotics, presence detection, and obstacle avoidance projects with boards like Arduino or ESP32 |
| **HiLetgo DC-DC Step Down XL4015 <div  align="center"> <img width="522" height="522" alt="61nLVKTcmBL _SX522_" src="https://github.com/user-attachments/assets/efe031ca-68ee-4b13-94fd-374ef5acef26" /> </div> | The HiLetgo XL4015 module stands out for its high conversion efficiency (up to 96%) and a robust design that supports an input voltage of 4V to 38V and an adjustable output from 1.25V to 36V. It features an integrated LED digital voltmeter that displays input or output voltage with an accuracy of ±0.05V, a physical button to toggle the measurement, and status indicator lights. Additionally, it operates at a switching frequency of 180 kHz and incorporates essential safety mechanisms such as short-circuit protection, overtemperature thermal shutdown, and current limiting up to 5A. |


</div>

- ### **Component Layout and Justification:**

	The design of our autonomous vehicle is based on a vertical three-level modular architecture, optimized for efficient center of gravity management, mass balance, and the mitigation of electromagnetic and mechanical interference. This hierarchical configuration by "floors" allows isolating mechanical power elements from logical processing and computer vision modules.

	- **Chassis Architecture by Levels:**

	- **1st Level (Ground Floor):** Constitutes the structural base and drivetrain of the vehicle. This level houses the RS380 Traction Motor, the servo-assisted steering mechanism, the HiLetgo DC-DC Step Down XL4015 voltage regulator, the three HC-SR04 ultrasonic sensors (Front-US and the lateral Left-US / Right-US sensors), and two VL53L0X-V2 Time of Flight (ToF) laser distance sensors located on the flanks of the central ultrasonic sensor.

		- *Technical Justification:* Placing the heavy actuators on the ground floor ensures a center of gravity close to the ground, maximizing traction on the rear wheels. Relocating the XL4015 step-down module to the base is a thermal management decision: it moves its heat dissipation away from the sensitive LiPo cells (Level 2) and the central processor (Level 3). Likewise, integrating the ToF sensors into this base, with a slightly recessed mount relative to the central ultrasonic sensor, uses the latter as a protective shield against impacts, while the lasers expand the detection resolution exactly at the height of collision.
    
	- **2nd Level (Middle Floor):** Located immediately above the transmission, this level houses the low-level control core and power storage. Fixed here are the Makeblock MegaPi expansion board and the vertical cage containing the LiPo Batteries.

		- *Technical Justification:* The MegaPi acts as an intermediate physical bridge to shorten the logical wiring paths to the first level actuators. By freeing this floor of the thermal converter and centralizing only the heavy batteries, aligned horizontally with the center of mass, polar moments of inertia are significantly reduced, preventing understeer or oversteer in tight corners of the track.

	- **3rd Level (Top Floor):** Corresponds to the peak of the structure, dedicated exclusively to high-level processing and geometric perception. It contains the Raspberry Pi 4 B onboard computer (equipped with its heat sink and active fan) and the elevated Arducam IMX219 computer vision camera assembly.

		- *Technical Justification:* Elevating the Raspberry Pi 4 completely isolates it from the direct mechanical vibrations of the traction motor and the current loops of the lower chassis. Furthermore, the top position favors the fan's thermal convection to avoid thermal throttling of the CPU during the execution of detection algorithms.

	**Perception and Spatial Orientation System:**
	This three-dimensional distribution complements our mixed perception system strategy (Vision + Acoustics + Infrared Optics), ensuring optimal coverage zones without mutual interference:

	This three-dimensional distribution complements our mixed perception system strategy, ensuring optimal coverage zones without mutual interference:

	- **Computer Vision Distribution (3rd Level):**
The Arducam IMX219 camera is positioned at the highest and most forward point of the third level, supported by an articulated 3D printed arm with a fixed downward tilt angle of 15 degrees. This elevation is critical to expand the 175° lens's line of sight, allowing the algorithm to cover a wider Region of Interest (ROI) of the track to identify color codes (traffic lights) and guide lines without the car's own structure obstructing the frame.

	- **Front Ultrasonic Distribution (1st Level):**
The front ultrasonic sensor (Front-US) is mounted directly on the chassis base plate in a low and forward position, just below the camera's projection line. It acts on the lower level as a real-time hardware safety bypass, detecting the physical presence of walls mathematically to trigger emergency braking.

	- **ToF Precision Laser Distribution (1st Level, Front Flanking):**
Located on the flanks of the central ultrasonic sensor, the VL53L0X-V2 laser sensors are installed with a slight depth offset. This configuration allows the HC-SR04 to act as a protective bumper, while the ToF infrared beams act as high-resolution directional profilers. This setup guarantees that narrow cylindrical obstacles are detected with millimeter precision, shielding the lateral blind spots of the ultrasound at short distances.

	- **Lateral Ultrasonic Distribution (1st Level):**
The two flank ultrasonic sensors (Left-US and Right-US) are rigidly anchored to the left and right sides of the first level, positioned longitudinally between both wheel axles and aligned vertically to the exact height of the tires. Placing them on the lower floor drastically minimizes false readings caused by the chassis's pitching (braking) or rolling (turning). This ensures the stabilization algorithm receives clean data of the distance to the walls to maintain a straight trajectory.

<div align="center">

<img width="1600" height="1200" alt="WhatsApp Image 2026-06-18 at 11 34 59 PM" src="https://github.com/user-attachments/assets/5bea7abe-f434-4bbd-9ce3-3c26d1443c42" />

</div>

- ### Battery:

	The Zeee 3S LiPo 11.1V 2200mAh 50C is a high-performance lithium polymer battery, designed specifically for radio control (RC) enthusiasts looking for an optimal balance between weight, size, and power. With a 3-cell (3S) configuration and a nominal voltage of 11.1V, this component provides the constant and aggressive energy needed to power a wide variety of models, from racing drones and scale airplanes to RC land vehicles. Its 2200mAh capacity ensures highly competitive playtime or flight time, allowing the motor's performance to be maximized without adding excessive weight that could compromise the model's agility.

	The real strength of this battery lies in its 50C discharge rate, meaning it is capable of safely delivering high current peaks when the throttle demands it, guaranteeing explosive accelerations and an immediate response to controls. Manufactured with high-quality materials and low internal resistance, the Zeee 3S stands out for its extended life cycle and thermal stability during intensive use. It usually comes equipped with high-conductivity connectors (such as the Deans T or XT60) and a JST-XH balance connector, facilitating both safe cell-by-cell charging and direct compatibility with most smart chargers on the market.

<div align="center">

<img width="698" height="718" alt="Captura de pantalla 2026-06-21 185733" src="https://github.com/user-attachments/assets/165be46b-0187-4bd8-9dd5-e95a580baaea" />

</div>

- ### Power Budget:

	To guarantee the operational stability of our car, we have implemented a redundant power architecture by using two independent batteries. This division is fundamental to protect the integrity of our systems:

	- **Power Circuit:** A battery dedicated exclusively to the MegaPi board, which manages the high-demand actuators (the RS380 traction motor and the MG996R steering servomotor), in addition to the three ultrasonic sensors and the start button. This isolation prevents voltage drops (transients) caused by sudden starts or motor stalling from affecting data processing.

	- **Logic and Vision Circuit:** A second independent battery exclusively powers the Raspberry Pi 4 and the Arducam camera. This separation is critical; by not sharing the power bus with the motors, we eliminate the risk of electromagnetic interference (EMI) and voltage spikes that could induce noise in the video signal or, in the worst-case scenario, cause unexpected reboots of the computer vision system during the competition.

	This configuration allows us to operate with maximum safety, ensuring that, even under severe mechanical stress conditions in steering and traction, our "brain" (Raspberry Pi) maintains a constant and clean power supply to process the trajectory with total precision.

<div align="center">

| Components | Quantity | Operating Voltage | Nominal/Peak Consumption | Total Consumption |
|---|---|---|---|---|
| **Raspberry Pi 4 B** | 1 | 5.0 V | 600 mA / 1250 mA | 1250 mA |
| **Arducam 8MP IMX219 (175°)** | 1 | 3.3 V | 250 mA | 250 mA |
| **Makeblock MegaPi (Logic)** | 1 | 5.0 V | 100 mA | 100 mA |
| **HC-SR04 Ultrasonic Sensors** | 3 | 5.0 V | 15 mA each | 45 mA |
| **Collision Sensor Module (Crash)** | 1 | 5.0 V | 10 mA | 10 mA |
| **LED Traffic Light Module** | 1 | 5.0 V | 30 mA | 30 mA |
| **MG996R Steering Servomotor** | 1 | 5.0 V | 500 mA / 2500 mA | 2500 mA |
| **RS380 Traction Motor** | 1 | 11.0 V | 2000 mA | 2000 mA |
| **Vl53l0x-v2 Sensor** | 2 | 5V | 10.0 mA | 20 mA |
| Total | | | 4.175 mA (4.17 A) mA | 6.205 mA (6.2 A) |

</div>

- ### Wiring Diagram:

	Our car's electrical architecture has been designed under a bus isolation principle to guarantee system reliability in a high-vibration, high-current-demand environment. As seen in our connection diagram, the wiring is divided into two clearly differentiated domains:

	- **Power Domain (Power Bus)**
Powered by the dedicated actuator battery, this high-current bus directly powers the MegaPi for the motors and servomotor:

		- **MegaPi:** Acts as the main power distribution center. Receives direct voltage from the power battery (7.2V - 12V) to power the RS380 traction motor and the MG996R steering servomotor on their dedicated ports.

		- **Traction and Steering System:** The RS380 motor and MG996R servo are directly connected to the high-power ports on the MegaPi. We have used higher gauge cables to minimize voltage drop during stall (maximum effort) maneuvers.

		- **Voltage Regulation and Stabilization (Buck Converter):** A 3A, 15W Buck Converter with Type-C output has been integrated. This step-down module efficiently reduces the battery voltage and stabilizes it to a constant 5.0V. Its function is to act as a protective barrier against consumption spikes and residual electrical noise generated by the motors, ensuring a clean and safe power supply for sensitive logic components and ultrasonic sensors, preventing erratic readings.

	- **Logic Domain (Control Bus)**
Powered by the dedicated Raspberry Pi battery, this bus is electrically independent:

	  	- **Data Processing:** The Raspberry Pi 4 B powers the Arducam camera through the CSI port, ensuring a low-latency, high-integrity data stream.

		- **Communications (I2C/UART Bus):** Communication between the Raspberry Pi and the MegaPi is done through a properly shielded serial bridge (USB/UART). To avoid "ground loops" which are the main cause of failures in autonomous robots, we have unified the grounds (GND) only at the MegaPi's entry point, keeping the rest of the sensor wiring with short and direct routes to minimize EMI (Electromagnetic Interference) pickup.

<div align="center">

<img width="2960" height="1625" alt="L-N-M@1 25x" src="https://github.com/user-attachments/assets/13e15df3-6f13-4d22-9dfd-a9a075e6561c" />

</div>

# 3.  Software <a id="software-architecture"></a>

- ### Support tools:

	- **Color Detector:** The lighting environment at robotics competitions is rarely identical to our lab. To prevent the computer vision system from failing due to changes in ambient light (shadows, reflections, or venue LED lights), we designed an interactive graphical application called Color-Detector.py.

	This tool allows us to calibrate in real-time the mathematical thresholds of the track colors (red/green blocks, blue/orange lines, and black walls) and export these parameters directly to the robot's brain.

	1. **Image Processing Architecture (Pipeline)**
	Unlike basic approaches that use the RGB or HSV color space, our script transforms the video stream to the LAB color space (CIE Lab)*. This technical decision is crucial because the LAB space completely isolates luminosity (L Channel) from pure color information (A and B Channels). The internal process before displaying the image follows these steps:

		- **Extraction and Equalization (CLAHE):** After converting the image to LAB, we separate the luminosity channel (L) and apply a CLAHE (Contrast Limited Adaptive Histogram Equalization) algorithm to it. This redistributes contrast locally, mitigating harsh shadows or glare on the track without altering the real color of objects.

		- **Smoothing Filter (Gaussian Blur):** A 7x7 Gaussian blur is applied to diffuse high-frequency noise from the camera sensor, preventing "dead" pixels or artifacts.

		- **Morphological Operations:** Once the user defines the color boundaries with the sliders, the script generates a binary mask (cv.inRange). To clean it, we apply "Erosion" (removes small noisy pixels or false positives) followed by "Dilation" (restores the original size of the detected object).

	2. **User Interface and Workflow (GUI)**
	The graphical interface was built with CustomTkinter to offer a low-contrast dark environment that won't strain the eyes during long calibration sessions in the pits. The usage flow is as follows:

		- **Preset Selection:** The operator starts by selecting a base color from the dropdown menu (e.g. RED, GREEN, BLACK). This loads safe default values (COLOR_PRESETS).

		- **Fine-Tuning via Sliders:** L-min / L-max: Adjusts tolerance to shadows and highlights.

			- **A-min / A-max: Adjusts the Green-Red axis spectrum.**

			- **B-min / B-max: Adjusts the Blue-Yellow axis spectrum.**
  
		*(Note: OpenCV's adapted 0 to 255 scale is used for all channels).*

		- **Combined Visual Telemetry:** The main screen consolidates three real-time views (960x240 pixels):

			- **Left:** The raw original video.

			- **Center:** The binary mask (white on black) showing exactly what the computer "sees" as a valid area.

			- **Right:** The isolated result (the extracted original color on a black background) to verify that elements outside the track are not being captured.

	3. **Configuration File Generation and Export**
	To avoid modifying the main source code (hardcoding) every time we calibrate a color, the "SAVE JSON" button packages the current minimum and maximum thresholds and exports them as a lightweight .json file (e.g. mask_red.json). This file includes a timestamp for version control and is read dynamically by the robot during boot-up at the competition.

   	<div align="center">

	<img width="803" height="447" alt="Gemini_Generated_Image_oe7w1uoe7w1uoe7w" src="https://github.com/user-attachments/assets/8ed55c9c-b1f7-45c8-a92f-bee337e51ff2" />

	</div>

	- **ROI Detector:** To ensure our computer vision system processes images efficiently, we developed an auxiliary script called ROI-Detector.py. This graphical interface tool allows interactively calibrating the camera's Regions of Interest (ROIs), delimiting the exact areas where the algorithm should look for and calibrate the colors of obstacles (red/green) and track walls.

	The script's functionality is designed to be fast and intuitive, allowing the team to readjust visual parameters in the pits before each round if track conditions change:

	1. **Video Initialization:** Upon running the script, a resizable window opens capturing the real-time video stream. The code automatically adjusts the image scale to maintain the aspect ratio without distorting the track's perspective.

	2. **Interactive Drawing (Mouse Callbacks):** Using the cursor, the user can draw rectangles directly on the live video.

		- **By clicking and dragging, a yellow box (temp_rect) is displayed showing a preview of the selected area.**

		- **Upon releasing the click, the region is fixed on the screen with a green box, displaying a label with its exact dimensions in pixels (width x height).**

	3. **Error Management:** If a mistake is made when tracing the zones, the user can press the 'C' (Clear) key on their keyboard to instantly erase all drawn regions from memory and start over.

	4. **Automatic Data Export:** Once the areas for scanning turn lines and color blocks are defined, the 'ESC' key is pressed. This closes the video stream and brings up a system dialog window (via Tkinter).

	5. **Code Generation:** The script takes the spatial coordinates (x1, y1, x2, y2) of each drawn ROI and automatically writes a Python (.py) file. This generated file contains the data structures (using @dataclass) ready to be imported directly by the robot's main brain, without needing to transcribe numbers by hand.

	**Engineering Justification**
	Creating this tool solves two critical problems in the development of autonomous vehicles:

	- **Processing Optimization:** By calibrating precise ROIs, we force the Raspberry Pi to search for colors only in very small portions of the image instead of analyzing the full frame. This drastically reduces CPU load and keeps the control loop at a high frequency.

	- **False Positive Reduction:** By strictly isolating the field of view to the track through this calibration, we prevent the robot from accidentally detecting external objects (like a judge's shoes or room lights) that share the same color as the obstacles.

   	<div align="center">

	<img width="765" height="565" alt="Gemini_Generated_Image_fop2o1fop2o1fop2" src="https://github.com/user-attachments/assets/f9cc3741-7394-4642-af6d-1e69d5f4c231" />


	</div>

- ### MegaPiController:

	This is a complete description of all the attributes and methods of the class, along with their arguments. We recommend that you consult it first before moving on to the other sections and that, when you clone the repository, you use it as a guide to navigate our code.

  	Here is all the technical documentation fully translated into Spanish [English], maintaining exactly the same format and rigorous order of the reference images:

---

 **mega_pi_controller.py (MegaPiController class)**

 **Dependencies**

* `serial`
* `time`
* `threading`
* `pandas`
* `random`
* `json`
* `cv2`
* `src.vision_controller.VisionController`
* `dataclasses.dataclass`

**Constructor method description**

```python
def __init__(self, port='COM9', baudrate=115200):
    """
    Initializes the serial connection with the MegaPi board and registers the subsystems.
    If the connection fails, it terminates the process with a critical error message.
    """
