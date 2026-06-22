```For best viewing, we recommend viewing the repository on your computer```

# WRO 2026 Future Engineers – LNM

<div align="center">
	
<img width="840" height="407" alt="WhatsApp Image 2026-06-19 at 11:51:57 PM" src="https://github.com/user-attachments/assets/cee364df-eeba-4338-8f2a-14949adb755b" />

</div>

Welcome to the GitHub repository of the **LNM Team**, formerly known as Ars Machina, which is competing in the **World Robot Olympiad™ (WRO®) Future Engineers 2026** category. Our team consists of David Wang and Pedro Catamo, who have designed a compact and innovative autonomous vehicle to tackle the dynamic challenges of the WRO 2026 competition.

## **Table of Contents**

**1. [Folder Structure](#folder-structure)**

**2. [The Team](#the-team)**

**3. [Our Robot](#our-robot)**

**4. [Electronic Systems](#electronic-systems)**

**5. [Mechanical Systems](#mechanical-systems)**

**5. [Software Architecture](#software-architecture)**

---

## **Folder Structure** <a id="folder-structure"></a>

This is the folder structure of our repository:

| Folder | Technical content | Detailed documentation |
|---|---|---|
| **models** | **3D Designs**<br>• Car Parts| [Explore the 3D models](models/README.md) |
| **schemes** | **Electrical Systems**<br>• Wiring diagrams<br>• Power management<br>• Component schematics| [Explore the schematics and wiring documentation](schemes/README.md) |
| **src** | **Software Algorithms**<br>• Navigation Logic<br>• Sensor Fusion<br>• Control Systems | [Explore the software and algorithms documentation](src/README.md) |
| **t-photos** | **Team Documentation**<br>• Team Member Profiles | [Explore the team photo documentation](t-photos/README.md) |
| **v-photos** | **Vehicle Documentation**<br>• Views from multiple angles | [Explore the vehicle photo documentation](v-photos/README.md) |
| **video** | **Performance validation**<br>• Challenge demonstrations<br>• Engineering tests | [Explore the performance video documentation](video/README.md) |

---

## **The Team** <a id="the-team"></a>

<div align="center">
	
<img width="1280" height="720" alt="Team_pic (1)" src="https://github.com/user-attachments/assets/156c3c29-799e-44e6-a7f0-629da61873b8" />

</div>

### **Members:**

- **David Wang**
   
	Born: April 1, 2011 (15 years old)

	School: 3rd year at U.E.C. Eduardo Blanco

  	Gmail: davidwangwu104@gmail.com
  	  
- **Pedro Catamo**
   
 	Born: January 28, 2009 (17 years old)
   
  	Education: 5th year at U.E.C. Eduardo Blanco
   
 	Gmail: pedrocatamo.2009@gmail.com

- ### **Coach:**

- **Jesús Alcalá**
   
  Born: November 18, 2005 (21 years old)
   
  Field of Study: Computer Engineering & Information Technology Engineering
   
  Gmail: Jdam50002@gmail.com

---

### Previous Designs:
  
<div align="center">
	
| Photo | Name | Description |
|---|---|---|
| <img width="920" height="920" alt="Screenshot 2026-06-17 185504" src="https://github.com/user-attachments/assets/36166165-a542-42d6-a771-41a60693a399" /> | **Cyber Cooper** | In 2023, we planned to design the car from scratch, modeling and 3D-printing our own parts, including the chassis and steering system. Although it seemed like a good idea at first, as we moved forward we began to encounter one problem after another, and we realized that our current design would cause us even more difficulties. In the end, we did everything we could within the time constraints we faced. |
| <img width="920" height="920" alt="front2" src="https://github.com/user-attachments/assets/ce130237-cc0b-4aa9-a620-0aea287408c2" /> | **Cooper** | In 2024, we developed a chassis with 3D-printed parts structured on two levels. The lower level housed the sensors and low-level electronics, while the upper level held the batteries and the Raspberry Pi 3 to optimize space. Although we made significant aesthetic and functional strides, we learned some hard lessons on the track: the excessive weight caused the couplings in the rear drivetrain to bend, which, in turn, led to severe mechanical friction issues between the 3D-printed parts. |
| <img width="920" height="920" alt="front" src="https://github.com/user-attachments/assets/804b3d7f-3500-4351-a917-ccf781029804" /> | **Halbi** | In 2025, given the resources we had available at the time, our main idea was to redesign the Cybercooper by modifying the existing base and strategy and using better electronic components; we began printing the new parts with white material and thinking of better ways to assemble the car’s steering system. In the end, we decided to use a prefabricated chassis base; the main reason was to save time (and headaches) with the mechanical design, which allowed us to devote more time to the electronics and programming. |
| <img width="920" height="920" alt="WhatsApp Image 2026-06-18 at 7:39:40 PM" src="https://github.com/user-attachments/assets/ca9f62ff-7b8b-452a-97de-95ebf12dc0ef" /> | **The Fridge** | In 2025, unlike the previous models that belonged to our coach, "The Fridge" was a design built entirely by us. Here we made the leap to Ackermann geometry and 3D-printed the vast majority of the parts. For the drive system, we used a DC motor with a gearbox to drive both wheels. We physically installed three ultrasonic sensors, a Raspberry Pi 4, and an MPU6050 gyroscope, but due to time constraints and severe configuration issues, the Raspberry Pi and the IMU ended up as dead weight, and we ended up controlling everything solely from the MegaPi. We struggled a lot: the 3D-printed steering parts kept breaking under stress, and programming autonomous navigation on the Arduino based solely on ultrasonic bounces was nearly impossible. |

</div>

---

# 1- Mobility and Design

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

	- ### Main Mechanical Specifications: <a id="sistemas-mecanicos"></a>

		- **Overall dimensions: 24.4 cm (length) × 15.4 cm (width) × 15.9 cm (height).**
		- **Car weight: approximately 1.2 kg.**
		- **Drivetrain: Two-phase mechanical rear-wheel drive.**
		- **Steering system: Ackermann geometry.**
	
	- ### Ackermann Steering Mechanism

		The vehicle uses precise geometry based on the **Ackermann Steering Principle** to navigate tight turns with zero lateral slip and minimal tire wear.

		* **The Physics Behind the Principle:** When a vehicle enters a curve, the inner front wheel follows a tighter, smaller concentric radius than the outer wheel. If both wheels turned at exactly the same angle, the tires would interfere with each other, causing the outer tire to drag, lose mechanical grip, and introduce severe structural vibrations that would disrupt visual tracking of the lanes. To resolve this, the mechanical geometry forces the inner wheel to pivot at a steeper angle than the outer wheel, ensuring that all four wheels rotate around a single common instantaneous center of curvature (ICC).

		* **Mechanical Implementation:** A high-torque **MG996R** digital servo ($11 \text{ kg}\cdot\text{cm}$ of torque) is mounted to the front bulkhead via a custom-machined L-shaped aluminum bracket to eliminate structural deflection. The servo arm drives a double-link steering rack connected to asymmetrical tie rods and steering knuckles. The steering arms are angled inward, pointing toward the center of the rear axle, completing the classic “Ackermann trapezoid.” This precise mechanical design automatically converts the servo’s linear displacement into nonlinear wheel angles.

		* **Digital Control and Calibration:** The MG996R is controlled by a continuous, jitter-free hardware PWM pulse train at $50\text{Hz}$ directly from the MegaPi microcontroller. The steering is rigidly mapped and calibrated to a software deadband where $80^\circ$ represents the absolute geometric center. The mechanical end points are limited by software between $40^\circ$ (Maximum Left) and $105^\circ$ (Maximum Right) to prevent the steering links from reaching a mechanical lock or exceeding the motor’s loss limits.

	- ### What Is Ackermann Geometry? 

		Understanding Ackermann’s mathematics and kinematics, in traditional mobile robotics (such as robots in the *RoboMission* category), differential drive is used because it is mathematically simple: you vary the speed of two motors, and the robot turns on its own axis. However, at high speeds, differential drive is unstable and unpredictable.

		**Ackermann Geometry** solves this using a purely mechanical principle. For a vehicle to turn without sliding sideways, the lines extended from the axles of all the wheels must intersect at a single point in space: the **Instantaneous Center of Rotation (ICR)** or ICC.

		The fundamental mathematical equation governing this kinematics is:
		<div align="center">
	
		$$\cot(\theta_{\text{out}}) - \cot(\theta_{\text{in}}) = \frac{w}{L}$$
		
		</div>
		
		Where:
		
		* $\theta_{\text{in}}$ is the angle of rotation of the inner wheel.*
		* $\theta_{\text{out}}$ is the angle of rotation of the outer wheel.*
		* $w$ is the track width (the distance between the front wheels).*
		* $L$ is the wheelbase (the distance between the front and rear axles).*

		Since the cotangent increases more rapidly at small angles, this relationship mechanically ensures that $\theta_{\text{in}} > \theta_{\text{out}}$ automatically occurs in any turn, causing the outer wheel’s angle to open so that it traces a larger circle.

		<div align="center">
  
		<img width="567" height="600" alt="17523247_203569336801744_2788986523412924047_n" src="https://github.com/user-attachments/assets/c36a271c-b45c-492a-805e-b107851429cd" />
		
		</div>

	- ### 2WD Electric Drive with Two-Speed Mechanical Transmission 

		The platform’s driving force is generated by a high-performance rear-wheel-drive (2WD) system, which breaks with traditional direct-coupling designs by integrating a two-speed mechanical reduction transmission using straight-cut cylindrical gears.

		* **Transmission System Architecture:** Unlike common configurations that couple the wheel directly to the motor’s reduction gearbox, this design mounts the RS380 motor in an upper parallel arrangement on a rigid support block. Power is transferred from the motor’s primary shaft to a lower drive shaft via an exposed straight-toothed gear train. This system of two interchangeable mechanical speeds allows the robot to be configured according to track conditions:
  		1. **Power/Torque Ratio (First Speed):** Optimizes the gear ratio to achieve maximum acceleration and precise control in tight turns or around obstacles, ideal for twisty sections. 
  		2. **Final Drive Ratio (Second Speed):** Reduces speed loss to take advantage of linear inertia on long straights, ensuring high cruising speed without excessive power consumption.

		<div align="center">
  
		<img width="515" height="218" alt="K-O-M-R-A-D 2-Speed Transmission System" src="https://github.com/user-attachments/assets/da8175e6-313d-42d6-bd3b-b1318082536f" />
		
		</div>

		* **Technical Specifications of the Motors (RS380):** The drive unit relies on magnetically brushed DC motors, specifically selected for their dynamic response curve and tolerance to transient load spikes.

	    * **Nominal Voltage:** $12\text{V}$ (Operating at a nominal cell voltage of $11.1\text{V}$ using a 3S LiPo battery to ensure thermal stability).
   
 		* **No-Load Current:** $0.3\text{A}$ | **Start-Up/Stall Current:** $3\text{A}$ protection in the driver.
   
 		* **Factory Rated Speed:** $15000\text{ RPM}$ at the motor core, internally reduced and finally adjusted by the external gearing to deliver an estimated final output speed of approximately $450\text{ RPM}$ at the wheel shaft.

		* **Kinematic Analysis and Calculation of Theoretical Absolute Speed:**
		To determine the chassis’s on-track performance and calibrate the per-lap time windows (such as the control parameter `lap_time = 4.3`), a kinematic calculation is performed based on the drive wheel diameter of $6.5\text{ cm}$ ($0.065\text{ m}$). We evaluate the rolling circumference ($C$) and the theoretical maximum linear velocity ($V$):

	<div align="center">
	
	$$C = \pi \times 0.065\text{ m} \approx 0.2041\text{ m}$$

	</div>

	By converting the revolutions per minute of the transmission’s secondary shaft to revolutions per second and multiplying by the circumference, we obtain the chassis’s forward speed:

	<div align="center">
	
	$$V = \frac{450\text{ RPM}}{60} \times 0.2041\text{ m} \approx 1.53\text{ m/s}$$
		
	</div>

	This value of $1.53\text{ m/s}$ represents the platform’s ideal limit speed. Under actual competition conditions, this value is modulated by software via speed commands (`speed = 90` or `80`) to account for static ground friction, rolling resistance from the bearings, and the instantaneous current demands placed on the MegaPi as it manages changes in inertia.


	- ### 3D-Printed Parts:

   		- #### **Parts:**

		<div align="center">
			
		| Component & Preview | Design & Geometry | Engineering Purpose |
		|---|---|---|
		| **Battery Case** <br><br><img width="400" height="400" alt="BatteryCase" src="https://github.com/user-attachments/assets/a5362844-dd0e-4073-bef8-bb034bae3ad9" /> | Designed as a vertical tower cage with four reinforced pillars on each side, integrated directly onto a solid mounting base with screw holes at the corners. The side walls feature large circular cutouts to minimize material weight while allowing for maximum passive airflow to prevent thermal stress on the LiPo cells during high discharge rates. The top pillar includes slotted retention eyelets for secure strap attachment. | It centers the combined mass of the battery cells vertically along the chassis’s central geometric axis. This open-cage design ensures quick access for battery replacement between races, while providing rigid structural containment against lateral inertial forces during high-speed turns. |
		| **Camera Case** <br><br><img width="400" height="400" alt="CameraCase" src="https://github.com/user-attachments/assets/7adbc42b-15eb-4677-a0a4-8d9b3c98bab3" /> | A compact, rectangular protective case designed specifically to house the IMX219 (Arducam) sensor. The lower section features a robust cylindrical pivot hinge with external locking teeth (straight-tooth profile) designed to mesh perfectly with a corresponding mounting base for mechanical angle locking. | Protects the camera’s delicate PCB from external debris or direct impacts on the track. The interlocking gear hinge allows you to mechanically adjust and lock the camera’s tilt angle to a precise 15-degree downward angle, preventing any unwanted shifts in the lens caused by high-frequency vibrations from the chassis during operation. |
		| **MegaPi Case** <br><br><img width="400" height="400" alt="MegaPiBase (1)" src="https://github.com/user-attachments/assets/8db95bf2-a29a-468c-ace8-e21bb1fae9f6" /> | A rugged, low-profile tray equipped with four integrated, heavy-duty vertical supports positioned at the corners to secure the main PCB. The base plate features internal routing channels and structural clearance cutouts to prevent components from extending beneath the plate, keeping the profile as close to the chassis as possible. | It functions as a rigid mechanical cradle for low-level power electronics. By raising the PCB via the integrated 3-mm supports, it prevents electrical short circuits with the chassis while dampening vibrations. The fully open perimeter ensures immediate access to the motor screw terminals, power rails, and sensor ports for field maintenance. |
		| **RaspberryPi Base** <br><br><img width="400" height="400" alt="RaspberryPiBase (1)" src="https://github.com/user-attachments/assets/2403b708-2e1d-4360-9504-aae68c0027d1" /> | A flat, mid-level modular platform featuring four integrated corner mounts for securely mounting the Raspberry Pi 4. The front section of the base incorporates a dual-ear hinge assembly equipped with internal locking teeth that engage directly with the hinge of the camera case. | It serves as a dual-purpose structural bridge. It provides a stable, elevated mount for the high-end onboard computer, ensuring optimal heat dissipation through natural convection to prevent CPU thermal throttling. At the same time, its integrated interlocking mount securely locks the camera assembly in place at the front, eliminating the need for additional components and saving valuable space in the chassis.|
		| **Ultrasonic Case** <br><br><img width="400" height="400" alt="UltrasonicSensorCase" src="https://github.com/user-attachments/assets/f9696c40-13e6-46b5-9712-2d7849a80005" /> | A compact, dual-barrel protective housing custom-designed to securely encapsulate the transmitter and receiver cylinders of the ultrasonic sensor module. It features integrated rear mounting tabs and bottom flanges for a continuous mechanical connection to the front crossbeams of the chassis frame. | It provides a rigid, vibration-isolated housing that keeps the ultrasonic sensor perfectly perpendicular to the horizontal plane of the track. This precise alignment eliminates acoustic signal distortion and wave scattering, ensuring highly accurate real-time distance measurements for obstacle detection and emergency braking maps. |

		</div>

		- #### **Printer:** The Creality Hi and Creality K1 printers were used.

   			- **Creality Hi:** This is one of Creality’s most recent offerings, designed with a strong focus on competing directly in the affordable multicolor printing market.
        
        		- **Build volume (what you can print):** $260 \times 260 \times 300\text{ mm}$. This is a mid-to-large size, excellent for robotics because it allows you to print complete chassis in a single piece without having to segment them.
            
          		- **Machine dimensions:** $409 \times 392 \times 477\text{ mm}$ (Weight: $8.75\text{ kg}$).
  
        		It is a high-speed Cartesian printer equipped with stepper-servo motors on the X/Y axes to prevent missed steps. Its greatest strength is its native compatibility with the CFS (Creality Filament System), an external “filament bank” module that allows you to automatically switch between up to 4 different colors (or up to 16 if you chain 4 modules together). Its maximum speed is $500\text{ m/s}$ with an acceleration of $12,000\text{ mm/s}^2$, and it reaches $300^\circ\text{C}$ at the nozzle.
  
        		- **How good is it?**
  
           			* **Strengths:** Extremely rigid cast aluminum frame, 100% automatic calibration and leveling via a strain gauge, and smart detection of tangles or filament end. If you buy the Combo version (with the CFS), it’s an incredible machine for parts that require soluble supports or combine rigid and flexible materials.
  
       				* **Weaknesses:** Since it isn’t factory-sealed (open design), consistently printing technical materials prone to shrinkage—such as ABS or ASA—can be challenging without building an external enclosure.
          
	   			- **Is it recommended for future use?**
  
   					Yes, absolutely. As a modern platform, it features the latest software support (Creality Print 5.1 / OrcaSlicer) and is designed around the automatic filament-changing ecosystem, which is where the entire industry is headed. It’s an excellent long-term investment for a workshop.

			- **Creality K1:** Originally launched as Creality’s direct response to Bambu Lab’s P1 series, it’s a professional-grade machine designed for pure speed and demanding materials.

     			- **Build volume (what you can print):** $220 \times 220 \times 250\text{ mm}$. This is a standard build volume (slightly smaller than the Creality Hi).
        
    			- **Machine dimensions:** $355 \times 355 \times 480\text{ mm}$ (Weight: $12.5\text{ kg}$).
  
        		It uses a CoreXY kinematic system where the print head moves ultra-lightly along the X/Y axes using crossed belts, while the print bed only moves down along the Z axis. Since it is completely enclosed with glass and acrylic panels, it retains internal heat within the print chamber. It reaches a speed of $600\text{ mm/s}$ and a massive acceleration of $20,000\text{ mm/s}^2$ thanks to its Klipper-based firmware (Creality OS).
  
   				- **How good is it?**
  
   					* **Strengths:** It’s a beast when it comes to technical materials. Its enclosed chamber is perfect for printing PETG, ABS, ASA, and Nylon without warping (edge peeling). Its acceleration is nearly double that of the Creality Hi, drastically reducing print times for complex mechanical parts.
  
       				* **Weaknesses:** The first units released (2023 batches) suffered from issues with the extruder (V1 version) and the hotend. Creality fixed these issues in later versions (extruder with a shiny lever and Unicorn-style nozzle), so if you buy one today, you can be sure you’re getting the improved, mature version.
          
	   			- **Is it recommended for future use?**
  
   					Yes, but under certain conditions. It remains an exceptionally fast and robust machine for engineering parts. However, keep in mind that the original K1 isn’t natively compatible with modern multicolor, multi-filament printing systems (that feature was reserved for the K2 series with the new CFS).

		- #### **PETG vs. PLA:**

		<div align="center">

		|  | PETG | PLA |
		|---|---|---|
		| **Durability and Strength** | High durability and superior toughness: Because it is glycol-modified, PETG prevents polymer crystallization, resulting in a highly tough material. Under mechanical impact, its molecular chains have the flexibility needed to deform elastically and absorb the kinetic energy of the impact. This prevents crack propagation, making it ideal for parts exposed to continuous collisions. | Low durability under dynamic loads: PLA has a rigid, crystalline molecular structure that gives it high surface hardness, but it lacks the ability to dissipate energy elastically. Upon direct collisions or sudden impacts against the edges of the track, the material stresses its interlaced layer bonds and tends toward brittle fracture, breaking suddenly and catastrophically rather than flexing. |
		| **Thermal Resistance and Stability** | Excellent thermal resistance: It maintains its structural integrity and mechanical rigidity in operating environments up to 75°C to 80°C without softening or geometric distortion. This property allows it to be safely mounted as a direct support for the powertrain or electronic circuit boards, withstanding the heat generated by mechanical friction and current spikes without yielding. | Vulnerable to thermal stress: Its glass transition temperature (softening point) is critically low, ranging between 50°C and 55°C. If used in components in direct contact with heavy-duty DC motors or voltage regulators that dissipate heat through conduction, PLA rapidly loses its rigidity, suffering permanent geometric deformations that throw the chassis out of alignment. |
		| **Structural Rigidity and Flexure** | Moderate elastic modulus (elastic flexibility): It has a semi-rigid nature that allows it to withstand mechanical vibrations, torsion, and continuous dynamic loads without suffering material fatigue. Although it yields slightly under extreme forces before breaking, this structural flexibility absorbs ground oscillations, protecting internal components. | Very high elastic modulus (Absolute Rigidity): It exhibits superior resistance to bending, meaning it does not bend or deform under moderate static loads. This lack of elastic flexibility is a technical advantage for static robot parts that must maintain a fixed, unchanging position, neutralizing any parasitic bending or buckling. |
		| **Chemical and Environmental Resistance** |  High chemical inertness and hydrophobicity: It is chemically inert and exhibits outstanding resistance to oils, greases, mechanical lubricants, and cleaning alcohols. Because it is completely hydrophobic, it is not weakened by ambient humidity after printing, and its high stability against UV radiation ensures that the parts retain their mechanical properties intact. | Susceptible to long-term degradation: As a biopolymer derived from organic sources, it is prone to accelerated degradation under continuous exposure to UV rays or drastic changes in humidity. Additionally, its chemical resistance to external agents such as alcohols, oils, or hardware lubricants is limited, which can weaken the part’s walls over time. |
		| **Dimensional Accuracy and Fits** | Moderate tolerances and prone to stringing: Because it requires higher extrusion temperatures, the material experiences greater thermal shrinkage as it cools, which requires calibrating the flow rate to prevent dimensional variations in millimeter-level fits. Additionally, its high viscosity tends to cause stringing (fine threads) that require post-processing in areas of fine mechanical movement. | Perfect Geometric Tolerances: Due to its extremely low thermal shrinkage upon cooling, PLA stands out for its millimeter-level dimensional stability. It allows for the printing of threads, bearing seats, and fine mechanical joints with virtually zero tolerance errors, ensuring that parts fit precisely and without play from the very first prototype. |
	
		</div>

# 2. Components <a id="sistemas-electronicos"></a>

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
| 1 | [LED Traffic Light Module](https://www.amazon.com/Traffic-Light-Module-Board-Arduino/dp/B07R1KJ4DT) | $10.99 | $10.99 |
| 2 | [Vl53l0x-v2 Sensor](https://articulo.mercadolibre.com.ve/MLV-724811982-ic-vl53l0x-v2-sensor-tiempo-vuelo-laser-a-distancia-_JM) | $5 | $10 |
| 1 | [HiLetgo DC-DC Step-Down XL4015](https://www.amazon.com/-/es/HiLetgo-alimentaci%C3%B3n-ajustable-pilares-volt%C3%ADmetro/dp/B00LTSC1YK) | $7.99 | $7.99 |
| | | | **$603.02** |

</div>

- ### Description:

<div align="center">

| Photo | Description |
|---|---|
| **Yfrobot kit** <div  align="center"> <div  style="width:290 px"> ![halbi](https://funduinoshop.com/media/image/84/6f/82/YFROBOT-chassis-kit-mit-lenkachse-technische-zeichnung_600x600@2x.png) </div> </div>  | The YFROBOT 4WD modular chassis combines four-wheel drive with a car-style steering system to provide greater stability and precise control. Designed with specific mounts for controllers such as Arduino or Raspberry Pi, it simplifies mechanical assembly and allows for easy addition of sensors or accessories. By reducing the complexity of designing from scratch, it serves as an ideal platform for education and competitions, allowing teams to focus directly on programming, autonomous navigation, and control systems. |
| **Raspberry Pi 4 B** <div align="center"> <img width="293" height="172" alt="images" src="https://github.com/user-attachments/assets/5c007a1e-273e-4ce2-89a7-fa99dd9b069b" /> </div> | The Raspberry Pi 4 Model B is a powerful single-board computer (SBC) the size of a credit card developed by the Raspberry Pi Foundation. It is widely used in robotics, IoT projects, and 	embedded systems due to its versatility, performance, and affordable price. |
| **Makeblock MegaPi** <div  align="center"> ![nano](https://ardubotics.eu/10754/makeblock-mega-pi-born-to-control.jpg) </div> | The **Makeblock MegaPi** board (**ATmega2560**) board was selected as the central microcontroller due to its ability to manage multiple motors and sensors simultaneously, outperforming options like the Arduino Uno or Nano thanks to its plug-and-play interfaces. Although it is designed to be mounted directly on a Raspberry Pi, we chose to connect it solely via **USB** for data transfer. This approach optimizes chassis space, takes advantage of the MegaPi’s built-in power supply, and prevents the main board from being exposed to risks during the soldering process. |
| **Zeee 3S LiPo Battery 2200mAh 11.1V 50C** <div  align="center"> <div  style="width:290 px"> ![LX2-BUSB](https://m.media-amazon.com/images/I/71-SIfPk3XL._AC_UF1000,1000_QL80_.jpg) </div> | The robot uses a Zeee 3S LiPo battery (2200mAh, 11.1V, 50C) as its sole power source, chosen for its high discharge rate and compact design, which optimizes space in the chassis compared to bulkier options. This configuration simplifies the system by powering both the logic and the motors, although it requires the use of external voltage regulators (such as DC-DC converters) to protect sensitive components like the Raspberry Pi. Despite requiring careful handling with specific chargers to avoid risks and extend its service life, it offers an excellent balance between power, size, and performance for robotic applications. |
| **MG996R steering servo** <div  align="center"> ![L298N](https://cdn-global-hk.hobbyking.com/media/catalog/product/cache/10/image/9df78eab33525d08d6e5fb8d27136e95/6/2/6221_1_high_7_.jpg) </div> | Included in the YFROBOT kit to control the steering axis, the MG996R is a high-torque digital servo motor that operates via PWM signals within a range of 0° to 180°. Its metal gear train provides greater durability and strength compared to plastic servos, allowing it to withstand demanding mechanical loads. With an operating range of 4.8V to 6V, it delivers torque between 9.4 and 11 kg·cm and speeds of up to 0.15 seconds per 60°, using a standard three-pin interface that is fully compatible with microcontrollers such as Arduino and Raspberry Pi. |
| **RS380 motor** <div  align="center"> ![motor](https://novatronicec.com/wp-content/uploads/2020/10/Motor-con-caja-reductora-25GA370_2.jpg) </div> | The RS-380 motor assembly with gearhead is a compact and versatile DC system, ideal for small-scale robotics and light automation. On its own, the RS-380 is a small brushed motor that spins at high speeds (between 10,000 and over 20,000 RPM depending on the voltage) but generates very little torque. The addition of the gearhead overcomes this limitation by reducing the rotational speed through a series of gears, which significantly increases the output torque and allows the system to move heavier mechanical loads effectively. |
| **ArduCam IMX219 8MP** <div  align="center"> ![Encorder](https://cdn.arducam.com/wp-content/uploads/2022/04/Arducam_IMX219_MIPI_Pi_B0392-8.jpg) </div> | The 8MP ArduCam IMX219 is a compact camera module based on the Sony IMX219 sensor—the same sensor used in the Raspberry Pi Camera v2—which balances resolution and performance for machine vision and robotics projects. It connects via the CSI (Camera Serial Interface), ensuring high-speed, low-latency data transfer to computers such as the Raspberry Pi or Jetson Nano. This design makes it an efficient and easily integrable solution for embedded systems that require real-time image processing. |
| **3A 15W Type-C Buck Converter** <div  align="center"> ![camera](https://m.media-amazon.com/images/I/61pOfxNxUnL._AC_UF1000,1000_QL80_.jpg) </div> | The **3A, 15W Type-C Buck Converter** module is a DC-DC step-down regulator that converts high input voltages to a low, stable output with an efficiency of 85 to 95%. In this project, it was used to connect the **Zeee 3S LiPo battery** (up to 12.6V) to the **Raspberry Pi 4B**, which requires a constant supply of **5V and up to 3A**. Since the battery’s full voltage would damage the board, the converter safely steps down and regulates the voltage, protecting components from overvoltage, minimizing energy loss due to heat, and ensuring stable system performance as the battery discharges. |
| **HC-SR04 Ultrasonic Sensor** <div  align="center"> <img width="466" height="466" alt="61CXJgLZwUL _SX466_" src="https://github.com/user-attachments/assets/1345b129-76f7-4f39-8ec2-b839398ea61b" /> </div> | The HC-SR04 ultrasonic sensor is a compact distance-measuring device that operates on the principle of sonar echo, ideal for obstacle avoidance in robotics. It is equipped with two transducers that emit a burst of high-frequency waves ($40\text{ kHz}$) and receive the echo after the waves bounce off an object. By accurately calculating the time it takes for the signal to travel back and forth, the module determines the linear distance within an effective range of 2 to 400 centimeters with an accuracy of 3 millimeters, providing real-time data crucial for vehicle navigation.|
| **Vl53l0x-v2 Sensor** <div  align="center"> <img width="525" height="478" alt="D_NQ_NP_2X_916413-MLV51649751397_092022-F" src="https://github.com/user-attachments/assets/c3c39671-3595-4e15-aefc-0836d1a81e33" /> </div> | This is a Time-of-Flight (ToF) laser distance sensor that measures distances of up to 2 meters with millimeter-level precision by emitting an invisible 940 nm infrared pulse. Unlike traditional sensors, it calculates the exact time it takes for the light to bounce off the object, allowing it to provide stable readings that are independent of the surface’s color, reflectivity, or texture. It features an I²C communication interface, is compatible with 3.3V and 5V voltages, and is ideal for robotics projects, presence detection, and obstacle avoidance using boards such as Arduino or ESP32 |
| **HiLetgo DC-DC Step-Down XL4015 <div  align="center"> <img width="522" height="522" alt="61nLVKTcmBL _SX522_" src="https://github.com/user-attachments/assets/efe031ca-68ee-4b13-94fd-374ef5acef26" /> </div> | The HiLetgo XL4015 module stands out for its high conversion efficiency (up to 96%) and a robust design that supports an input voltage of 4V to 38V and an adjustable output of 1.25V to 36V. It features a built-in digital LED voltmeter that displays the input or output voltage with an accuracy of ±0.05V, a physical button to switch between measurement modes, and status indicator lights. Additionally, it operates at a switching frequency of 180 kHz and incorporates essential safety mechanisms such as short-circuit protection, thermal shutdown due to overheating, and current limiting up to 5A. |


</div>

- ### **Component Layout and Rationale:**

	The design of our autonomous vehicle is based on a modular architecture with three vertical levels, optimized for efficient management of the center of gravity, mass balance, and mitigation of electromagnetic and mechanical interference. This hierarchical “floor” configuration allows us to isolate the mechanical power components from the logic processing and computer vision modules.

	- **Tiered Chassis Architecture:**

	- **1st Level (Lower Deck):** This constitutes the vehicle’s structural base and undercarriage. Located on this level are the RS380 traction motor, the servomotor-assisted steering mechanism, the HiLetgo DC-DC Step Down XL4015 voltage regulator, the three HC-SR04 ultrasonic sensors (Front-US and the side sensors Left-US / Right-US), and two VL53L0X-V2 time-of-flight (ToF) laser distance sensors positioned on either side of the central ultrasonic sensor.

		- *Technical Rationale:* Placing the heavy actuators on the lower deck ensures a center of gravity close to the ground, maximizing rear-wheel traction. Relocating the XL4015 gearhead module to the base is a thermal management decision: it moves its heat dissipation away from the sensitive LiPo cells (Level 2) and the central processor (Level 3). Likewise, integrating the ToF sensors into this base—mounted slightly behind the central ultrasonic sensor—uses the latter as a protective shield against impacts, while the lasers extend detection resolution precisely to the collision height.
    
	- **2nd Level (Middle Level):** Located immediately above the transmission, this level houses the low-level control core and power storage. The Makeblock MegaPi expansion board and the vertical cage containing the LiPo batteries are mounted here.

		- *Technical Justification:* The MegaPi acts as an intermediate physical bridge to shorten the logical wiring paths to the first-level actuators. By freeing this level from the thermal converter and centralizing only the heavy batteries—aligned horizontally with the center of mass—the polar moments of inertia are significantly reduced, preventing understeer or oversteer in sharp turns.

	- **3rd Level (Upper Deck):** This corresponds to the apex of the structure, dedicated exclusively to high-level processing and geometric perception. It contains the Raspberry Pi 4 B onboard computer (equipped with its heat sink and active fan) and the elevated Arducam IMX219 machine vision camera assembly.

		- *Technical Rationale:* Elevating the Raspberry Pi 4 completely isolates it from direct mechanical vibrations from the drive motor and current loops in the lower chassis. Additionally, the elevated position enhances thermal convection from the fan to prevent thermal throttling of the CPU during the execution of detection algorithms.

	**Spatial Perception and Orientation System:**
	This three-dimensional layout complements the strategy of our hybrid perception system (Vision + Acoustics + Infrared Optics), ensuring optimal coverage areas without mutual interference:

	This three-dimensional layout complements the strategy of our hybrid perception system, ensuring optimal coverage areas without mutual interference:

	- **Computer Vision Distribution (3rd Level):**
The Arducam IMX219 camera is positioned at the highest and most forward point of the third level, supported by a 3D-printed articulated arm with a fixed downward tilt angle of 15 degrees. This elevation is critical for expanding the lens’s 175° field of view, allowing the algorithm to cover a wider Region of Interest (ROI) on the track to identify color codes (traffic lights) and guide lines without the cart’s own structure obstructing the frame.

	- **Front Ultrasonic Sensor (1st Level):**
The front ultrasonic sensor (Front-US) is mounted directly on the chassis’s base plate in a low, forward position, just below the camera’s line of sight. It functions at the lower level as a real-time hardware safety bypass, mathematically detecting the physical presence of walls to trigger emergency braking.

	- **Precision ToF Laser Sensors (1st Level, Front Flanking):**
Located on either side of the central ultrasonic sensor, the VL53L0X-V2 laser sensors are installed with a slight depth offset. This configuration allows the HC-SR04 to act as a protective bumper, while the ToF’s infrared beams serve as high-resolution directional profilers. This configuration ensures that narrow cylindrical obstacles are detected with millimeter-level precision, eliminating the ultrasonic sensor’s lateral blind spots at close range.

	- **Lateral Ultrasonic Sensors (1st Level):**
The two side ultrasonic sensors (Left-US and Right-US) are rigidly mounted to the left and right sides of the first level, positioned longitudinally between the two wheel axles and vertically aligned at the exact height of the tires. Placing them low on the floor drastically minimizes false readings caused by the chassis pitching (braking) or rolling (turning). This ensures that the stabilization algorithm receives clean data on the distance to the walls to maintain a straight path.

<div align="center">

<img width="1600" height="1200" alt="WhatsApp Image 2026-06-18 at 11:34:59 PM" src="https://github.com/user-attachments/assets/5bea7abe-f434-4bbd-9ce3-3c26d1443c42" />

</div>

- ### Battery:

	The Zeee 3S LiPo 11.1V 2200mAh 50C is a high-performance lithium polymer battery, specifically designed for radio-controlled (RC) enthusiasts seeking an optimal balance between weight, size, and power. With a 3-cell (3S) configuration and a nominal voltage of 11.1V, this battery provides the consistent, aggressive power needed to power a wide variety of models, from racing drones and scale airplanes to RC land vehicles. Its 2200mAh capacity ensures extremely competitive play or flight time, allowing you to maximize motor performance without adding excessive weight that could compromise the model’s agility.

	The true strength of this battery lies in its 50C discharge rate, meaning it can safely deliver high current spikes when the throttle demands it, ensuring explosive acceleration and immediate response to controls. Manufactured with high-quality materials and low internal resistance, the Zeee 3S stands out for its long cycle life and thermal stability during intensive use. It typically comes equipped with high-conductivity connectors (such as Deans T or XT60) and a JST-XH balancing connector, which facilitates both safe cell-by-cell charging and direct compatibility with most smart chargers on the market.

<div align="center">

<img width="698" height="718" alt="Screenshot 2026-06-21 185733" src="https://github.com/user-attachments/assets/165be46b-0187-4bd8-9dd5-e95a580baaea" />

</div>

- ### Power Budget:

	To ensure the operational stability of our car, we have implemented a redundant power architecture using two independent batteries. This setup is essential to protect the integrity of our systems:

	- **Power Circuit:** A battery dedicated exclusively to the MegaPi board, which manages the high-demand actuators (the RS380 drive motor and the MG996R steering servomotor), as well as the three ultrasonic sensors and the start button. This isolation prevents voltage drops (transients) caused by sudden starts or motor lockups from affecting data processing.

	- **Logic and Vision Circuit:** A second independent battery powers only the Raspberry Pi 4 and the Arducam camera. This separation is critical; by not sharing the power bus with the motors, we eliminate the risk of electromagnetic interference (EMI) and voltage spikes that could induce noise in the video signal or, in the worst-case scenario, cause unexpected reboots of the computer vision system during the competition.

	This configuration allows us to operate with maximum safety, ensuring that, even under severe mechanical stress on the steering and drive systems, our “brain” (Raspberry Pi) maintains a constant, clean power supply to process the trajectory with complete precision.

<div align="center">

| Components | Quantity | Operating Voltage | Nominal/Peak Power Consumption | Total Power Consumption |
|---|---|---|---|---|
| **Raspberry Pi 4 B** | 1 | 5.0 V | 600 mA / 1250 mA | 1250 mA |
| **Arducam 8MP IMX219 (175°)** | 1 | 3.3 V | 250 mA | 250 mA |
| **Makeblock MegaPi (Logic)** | 1 | 5.0 V | 100 mA | 100 mA |
| **HC-SR04 Ultrasonic Sensors** | 3 | 5.0 V | 15 mA each | 45 mA |
| **Crash Sensor Module** | 1 | 5.0 V | 10 mA | 10 mA |
| **LED Traffic Light Module** | 1 | 5.0 V | 30 mA | 30 mA |
| **MG996R Steering Servo** | 1 | 5.0 V | 500 mA / 2500 mA | 2500 mA |
| **RS380 Drive Motor** | 1 | 11.0 V | 2000 mA | 2000 mA |
| **Vl53l0x-v2 Sensor** | 2 | 5V | 10.0 mA | 20 mA |
| Total | | | 4.175 mA (4.17 A) | 6.205 mA (6.2 A) |

</div>

- ### Wiring Diagram:

	The electrical architecture of our car has been designed based on the principle of bus isolation to ensure system reliability in an environment with high vibration and high current demand. As shown in our wiring diagram, the wiring is divided into two clearly distinct domains:

	- **Power Domain (Power Bus)**
Powered by the battery dedicated to actuators, this high-current bus directly powers the MegaPi for the motors and the servomotor:

		- **MegaPi:** Acts as the main power distribution hub. It receives direct voltage from the power battery (7.2V–12V) to power the RS380 traction motor and the MG996R steering servomotor through their dedicated ports.

		- **Drive and Steering System:** The RS380 motor and MG996R servo are connected directly to the MegaPi’s high-power ports. We have used heavier-gauge wires to minimize voltage drop during stall maneuvers (maximum load).

		- **Voltage Regulation and Stabilization (Buck Converter):** A 3A, 15W buck converter with a Type-C output has been integrated. This step-down module efficiently reduces the battery voltage and stabilizes it at a constant 5.0V. Its function is to act as a protective barrier against power spikes and residual electrical noise generated by the motors, ensuring a clean and safe power supply for sensitive logic components and ultrasonic sensors, thereby preventing erratic readings.

	- **Logic Domain (Control Bus)**
Powered by the Raspberry Pi’s dedicated battery, this bus is electrically independent:

	  	- **Data Processing:** The Raspberry Pi 4 B powers the Arducam camera via the CSI port, ensuring a low-latency, high-integrity data stream.

		- **Communications (I2C/UART Bus):** Communication between the Raspberry Pi and the MegaPi is carried out via a properly shielded serial bridge (USB/UART). To prevent "ground loops," which are the leading cause of failures in autonomous robots, we have unified the ground (GND) connections only at the MegaPi's input point, keeping the rest of the sensor wiring short and direct to minimize EMI (electromagnetic interference) pickup.

<div align="center">

<img width="2960" height="1625" alt="L-N-M@1 25x" src="https://github.com/user-attachments/assets/13e15df3-6f13-4d22-9dfd-a9a075e6561c" />

</div>

# 3.  Software <a id="software-architecture"></a>

- ### Utils:

	- **Color Detector:** The lighting conditions at robotics competitions are rarely identical to those in our lab. To prevent the computer vision system from failing due to changes in ambient light (shadows, reflections, or LED lights in the venue), we have designed an interactive graphical application called Color-Detector.py.

	This tool allows us to calibrate the mathematical thresholds for the track colors (red/green blocks, blue/orange lines, and black walls) in real time and export these parameters directly to the robot’s control unit.

	1. **Image Processing Architecture (Pipeline)**
	Unlike basic approaches that use the RGB or HSV color space, our script transforms the video stream into the LAB (CIE Lab)* color space. This technical decision is crucial because the LAB color space completely isolates luminance (L channel) from pure color information (A and B channels). The internal process before displaying the image follows these steps:

		- **Extraction and Equalization (CLAHE):** After converting the image to LAB, we separate the luminance channel (L) and apply a CLAHE (Contrast-Limited Adaptive Histogram Equalization) algorithm to it. This redistributes contrast locally, mitigating harsh shadows or glare on the track without altering the actual color of the objects.

		- **Smoothing Filter (Gaussian Blur):** A 7x7 Gaussian blur is applied to smooth out high-frequency noise from the camera sensor, preventing “dead” pixels or artifacts.

		- **Morphological Operations:** Once the user defines the color boundaries using the sliders, the script generates a binary mask (cv.inRange). To clean it up, we apply “Erosion” (removes small noisy pixels or false positives) followed by “Dilation” (restores the original size of the detected object).

	2. **User Interface and Workflow (GUI)**
	The graphical interface was built using CustomTkinter to provide a low-contrast, dark environment that is easy on the eyes during long calibration sessions in the pits. The workflow is as follows:

		- **Preset Selection:** The operator begins by selecting a base color from the drop-down menu (e.g., RED, GREEN, BLACK). This loads safe default values (COLOR_PRESETS).

		- **Fine-Tuning with Sliders:** L-min / L-max: Adjusts the tolerance for shadows and highlights.

			- **A-min / A-max: Adjusts the Green-Red axis spectrum.**

			- **B-min / B-max: Adjusts the Blue-Yellow axis spectrum.**
  
		*(Note: The adapted OpenCV scale from 0 to 255 is used for all channels).*

		- **Combined Visual Telemetry:** The main screen consolidates three real-time views (960x240 pixels):

			- **Left:** The original raw video.

			- **Center:** The binary mask (white on black) showing exactly what the computer “sees” as a valid area.

			- **Right:** The isolated result (the original color extracted against a black background) to verify that no elements outside the track are being captured.

	3. **Generating and Exporting Configuration Files**
	To avoid modifying the main source code (hardcoding) every time we calibrate a color, the “SAVE JSON” button packages the current minimum and maximum thresholds and exports them as a lightweight .json file (e.g., mask_red.json). This file includes a timestamp for version control and is dynamically read by the robot during startup at the competition.

   	<div align="center">

	<img width="803" height="447" alt="Gemini_Generated_Image_oe7w1uoe7w1uoe7w" src="https://github.com/user-attachments/assets/8ed55c9c-b1f7-45c8-a92f-bee337e51ff2" />

	</div>

	- **ROI Detector:** To ensure that our computer vision system processes images efficiently, we have developed a helper script called ROI-Detector.py. This graphical interface tool allows for interactive calibration of the camera’s Regions of Interest (ROIs), defining the exact areas where the algorithm should search for and calibrate the colors of obstacles (red/green) and the track walls.

	The script is designed to be fast and intuitive, allowing the team to readjust the visual parameters in the pits before each round if track conditions change:

	1. **Video Initialization:** When the script is run, a resizable window opens that captures the video stream in real time. The code automatically adjusts the image scale to maintain the aspect ratio without distorting the track’s perspective.

	2. **Interactive Drawing (Mouse Callbacks):** Using the cursor, the user can draw rectangles directly on the live video.

		- **When clicking and dragging, a yellow box (temp_rect) appears, showing a preview of the selected area.**

		- **When the mouse button is released, the region is fixed on the screen with a green box, displaying a label with its exact dimensions in pixels (width x height).**

	3. **Error Handling:** If an error occurs while drawing the areas, the user can press the 'C' (Clear) key on the keyboard to instantly clear all drawn regions from memory and start over.

	4. **Automatic Data Export:** Once the relevant areas for scanning the rotation lines and color blocks have been defined, press the 'ESC' key. This stops the video stream and displays a system dialog box (via Tkinter).

	5. **Code Generation:** The script takes the spatial coordinates (x1, y1, x2, y2) of each drawn ROI and automatically generates a Python file (.py). This generated file contains data structures (using @dataclass) ready to be imported directly by the robot’s main controller, without the need to transcribe numbers by hand.

	**Engineering Rationale**
	The creation of this tool solves two critical problems in the development of autonomous vehicles:

	- **Processing Optimization:** By calibrating precise ROIs, we force the Raspberry Pi to search for colors only in very small portions of the image rather than analyzing the entire frame. This drastically reduces the CPU load and keeps the control loop running at a high frequency.

	- **Reduction of False Positives:** By strictly limiting the field of view to the track through this calibration, we prevent the robot from accidentally detecting external objects (such as a judge’s shoes or lights in the room) that share the same color as obstacles.

   	<div align="center">

	<img width="765" height="565" alt="Gemini_Generated_Image_fop2o1fop2o1fop2" src="https://github.com/user-attachments/assets/f9cc3741-7394-4642-af6d-1e69d5f4c231" />


	</div>

- ### MegaPiController:

	This is a complete description of all the class’s attributes and methods, along with their arguments. We recommend that you review it first before moving on to the other sections and that, when you clone the repository, you use it as a guide to navigate our code.

  	Here is all the technical documentation, fully translated into Spanish, maintaining exactly the same format and strict order of the reference images:

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

**Description of the constructor method**

```python
def __init__(self, port='COM9', baudrate=115200):
    """
    Initializes the serial connection with the MegaPi board and registers the subsystems.
    If the connection fails, terminates the process with a critical error message.
    """

```

The constructor establishes a communication channel via the hardware serial port with the MegaPi microcontroller. It automatically starts a background listening thread (`_read_telemetry`) to capture incoming hardware metrics asynchronously, initializes the computer vision subsystem (`VisionController`), loads predefined color masks from specific JSON structures, and prepares the internal registers, state variables, and Regions of Interest (ROIs) for spatial and line tracking.

<div align="center">

**Attribute Description:**

| Attribute | Data Type | Functionality |
| --- | --- | --- |
| `ser` | `serial.Serial` | Represents the low-level hardware serial communication channel with the MegaPi. |
| `dist_front` | `int` | Stores the real-time distance value (cm) captured by the central ultrasonic sensor. |
| `dist_left` | `int` | Stores the real-time distance value (cm) captured by the left ultrasonic sensor. |
| `dist_right` | `int` | Stores the real-time distance value (cm) captured by the right ultrasonic sensor. |
| `ir_left` | `int` | Stores the raw reflectance percentage ($0\%$ to $100\%$) from the left TCRT5000 IR sensor. |
| `ir_right` | `int` | Stores the raw reflectance percentage value ($0\%$ to $100\%$) from the right TCRT5000 IR sensor. |
| `data_log` | `list[dict]` | A volatile in-memory log used to concatenate telemetry steps intended for saving training data. |
| `log_index` | `int` | Continuous, auto-incrementing step counter for the telemetry log dataframe. |
| `vision` | `VisionController` | Instantiated central module responsible for frame capture and LAB/HSV contour mapping. |
| `running` | `bool` | High-level execution control boolean variable used to safely terminate background thread operations. |
| `reader_thread` | `threading.Thread` | An asynchronous daemon thread dedicated to polling incoming serial payload packets. |
| `button_value` | `int` | Binary representation of the state of the physical button integrated into the board for system startup. |
| `turning_direction` | `int` | Tracks the track layout configuration ($0$: Unassigned, $1$: Clockwise/Blue, $2$: Counterclockwise/Orange). |
| `rois` | `list[ROI]` | Defines hard-coded processing regions for analyzing the front wall area and track lines. |

</div

**Method Descriptions:**

<div align="center">

| Method | Arguments | Return | Description |
| --- | --- | --- | --- |
| `_read_telemetry()` | None | `None` | Continuous polling thread. Decodes a fixed 8-byte payload format prefixed by a `0xAA` header byte. |
| `_send_command()` | `action: int`, `v1: int`, `v2: int` | `None` | Packages and transmits 5-byte low-level control protocol commands prefixed with a `0xFF` command flag. |
| `get_masks()` | `color: str` | `list` | Opens the local color matrix configuration files and extracts the arrays of numerical limits. |
| `load_masks()` | None | `None` | Sequential startup method that maps the boundaries of the red, green, blue, orange, and black colors within the object. |
| `get_frontal_area()` | None | `None` | Queries the mass volumes of black contours along the upper frontal horizon ROI. |
| `get_blue_line()` | None | `None` | Segments and evaluates the profile of the tracking line pattern by searching for blue track triggers. |
| `get_orange_line()` | None | `None` | Segments and evaluates the profile of the tracking line pattern by searching for orange track triggers. |
| `debug_UI()` | None | `None` | A graphical overlay engine that displays dynamic computer vision tracking loops in a local frame window. |
| `log_step()` | `action_code: int` | `None` | Adds real-time variable values (ultrasonic, infrared) to the local log array. |
| `move_forward()` | `speed: int`, `log: bool` | `None` | Invokes low-level traction actuators to set forward motion at the selected speeds. |
| `move_backward()` | `angle: int`, `speed: int`, `log: bool` | `None` | Activates reverse motion vectors while setting the steering links to a turn-off angle. |
| `turn_direction()` | None | `None` | Reactive control macro that routes turning steps based on current steering states. |
| `turn_left()` | `angle: int`, `speed: int`, `log: bool` | `None` | Sets the Ackermann servo links to angles turned to the left at fixed drive speeds. |
| `turn_right()` | `angle: int`, `speed: int`, `log: bool` | `None` | Sets the mechanical Ackermann servo links to closed angles to the right at fixed traction speeds. |
| `turn_center()` | `log: bool` | `None` | Recalibrates the active steering servo pulses back to the geometric center coordinates. |
| `stop()` | `log: bool` | `None` | Immediately disables active speed controls to cut power to the motors and stop the vehicle. |
| `get_distances()` | None | `tuple[int, int, int]` | Standard telemetry getter that returns a tuple consisting of the current sensor readings (front, left, right). |
| `get_ir_reflectance()` | None | `tuple[int, int]` | Returns a real-time tuple containing the localized infrared reflectance percentages ($0–100\%$). |
| `save_data_to_csv()` | `filename: str` | `None` | Compiles queued data dumps directly into index-mapped structures on disk using Pandas. |
| `close()` | None | `None` | Releases process handles, sends a shutdown command, and safely closes open serial ports. |
| `start()` | None | `bool` | Evaluates the button states. Returns `True` if the button is released (HIGH/0), keeping the loop running. |

</div>

- ### Arduino Controller:

	- Open Challenge:
  
		- **Open Challenge Video:**

		<div align="center">
			
		[![Open Challenge Video](https://img.youtube.com/vi/WPSj0BXfQ5U/0.jpg)](https://youtu.be/WPSj0BXfQ5U)

		*Demonstration of autonomous navigation and speed control on a dynamic track.*

		</div>

		- **Strategy:** The strategy designed to tackle the Open Challenge is based on a fast, highly predictable navigation system. The goal is to maximize constant speed (BASE_SPEED = 130) while keeping the chassis stable using a "Sensor Fusion" approach (camera + ultrasonic sensors). 

			The vehicle’s dynamic behavior is governed by a finite-state machine that switches between linear navigation, sharp turns, and race finish.

			- **Cornering State (90° Turns)**
			At high speeds, a standard PID control loop lacks the physical responsiveness to take right-angle turns without skidding or crashing. Therefore, an 	interruption state. When the camera detects track saturation (a black area larger than 6500 px) and the system already knows the direction of the circuit (`LNM.turning_direction != 0`), the robot assumes a 90° turn. 

			At this critical moment, the software immediately suspends visual PID control, resets the error and integral variables to zero to prevent windup, and executes the subroutine `LNM.turn_direction()`, locking the steering at its maximum mechanical angle. The vehicle maintains this blind turn until the sensors confirm the exit: the black area must fall below 6500 px, and the front ultrasonic sensor must measure a clear space greater than 80 cm. When both conditions are met simultaneously, lateral PID centering resumes.

			- **Lap Counting and Asynchronous Timing**
Telemetry for lap counting is performed by detecting the transverse colored markings in the finish zone, which we refer to as **loops** (orange or blue).

			At startup, the direction of rotation is unknown. On the first pass through the finish line, if a large-area color pattern (greater than 1200 px) is detected, the robot permanently stores its running direction in memory. From that point on, non-blocking count control is activated. When the robot crosses the loop with an area greater than 500 px, the general counter is incremented. 

			To eliminate false positives caused by the microcontroller’s high reading frequency when passing over the same mark, a 1.1-second hold timer was implemented. The internal logic flows as follows:

			```
                  Finish Line Detected (Area > 500 px)
                             [ loops += 1 ]
                                   |
                                   v
                       Activate Fixed State (n=1)
                    Start Guard Timer
                                   |
                                   v
                      Time Elapsed > 1.1s?
                       +--- YES          NO ---+
                       |                      |
                       v                      v
             Release State (n=0)     Maintain Lock
            Ready for New Cycle  (Prevents False Counts)
	 		```
  
			- **Safe Stop Mechanism**
			The rules require that the robot complete its run after the 12th lap. Abruptly cutting power to the motors right at the finish line would cause severe skidding or the robot to veer off the track due to the high inertia carrying the chassis at a speed of 130.

			To mitigate this mechanical stress, the software initiates a controlled stopping procedure. Upon detecting the 12th loop, the `end_game_triggered` flag is set and the clock time is captured in `end_game_timer`. The vehicle continues to actively execute its PID loops for centering, wall avoidance, and traction control for exactly 1 additional second of grace period. Once this mathematical grace period expires, the system breaks out of the main loop and calls the LNM.stop() function, ensuring that the robot smoothly dissipates its inertia and comes to a legal stop within the circuit boundaries.

		- **Flowchart:**

	<div align="center">

	<img width="4382" height="6096" alt="untitled@1 25x (3)" src="https://github.com/user-attachments/assets/2e304801-5b9d-4e67-b87a-4c6e3bc34b9a" />

	</div>

	- **Obstacle Challenge:**

	- **Strategy:** The strategy designed to address the second challenge (obstacle avoidance) is built modularly on the architectural foundation of the open round. The lateral Regions of Interest (`roi_izq` and `roi_der`), the camera resolution, and the base color segmentation filters are retained.

		The core of this challenge lies in the semantic interpretation of the environment according to the official competition rules: the pillars act as directional signs indicating the correct lane. To robustly follow this navigation logic at a constant speed (`VELOCIDAD_BASE = 68`), the software was structured around three fundamental pillars:

		- **Open Challenge Base (Baseline Navigation):** Maintains center-line control using the difference in line areas and an ultrasonic-assisted safety fallback.
   
		- **Lane Selection Technique (Computer Vision):** Long-range color segmentation using a new expanded frontal Region of Interest (ROI_OBSTACLES).
    
		- **Asynchronous State Machine:** Dedicated control algorithms for precise evasion and safe return to the lane.

	- **ROIS:** To anticipate the trajectory of the pillars without interfering with the reading of the road guide lines, a central scanning zone named ROI_OBSTACULOS was implemented with optimized pixel dimensions `ROI(30, 30, 610, 320)`. This configuration allows objects to be processed before they enter the critical frontal collision threshold.
Additionally, the system implements two independent PID control loops with different tunings based on the vehicle’s dynamic requirements:

		- **Standard Line PID:** Configured with conservative values (`Kp = 0.015`, `Kd = 0.035`) to maintain smooth transitions and stable linear movement on straight sections.
  
		- **Obstacle Avoidance PID:** Configured with a highly aggressive response (`Kp = 0.32`, `Kd = 0.01`). The high proportional term ensures that the vehicle responds with immediate steering torque to the movement of the pillar in the image, while the derivative term dampens the return to prevent the rear of the chassis (tail) from skidding and hitting the obstacle.

		- **Implementation of the Navigation State Machine:** Halbi the Green’s dynamic behavior is governed by a finite-state machine that switches asynchronously between 	three operating modes to ensure that the centering and evasion logics do not conflict.

	- **State 1:** LINEAR (Base Navigation and Sharp Curves)
    
		This is the robot’s default state. While in this mode, the vehicle prioritizes geometric centering by calculating the error between the lateral black areas (`error = black_areas[1] - black_areas[0]`). If the front ultrasonic sensor detects a wall at a short distance (`front_dist < 90 cm`) in the presence of a high density of black track pixels (`LNM.black_area > 8000`), the state is temporarily locked under the `turning = True` flag to force a 90° sharp turn. Simultaneously, the `process_obstacles()` method analyzes the filtered maximum contours under the `mask_red` and `mask_green` masks. The transition to the evasion state is triggered immediately when the area of a contour exceeds the calibrated noise thresholds:

		<div align="center">
		
		**Green Pillar: Area $> 350 \text{ px} \rightarrow$ Transition to DODGING | side_memory = "LEFT" (The pillar must be left on the left).**
   
		**Red Pillar: Area $> 300 \text{ px} \rightarrow$ Transition to DODGING | side_memory = "RIGHT" (The pillar must be left on the right).**

		</div>
		
	- **State 2:** AVOIDING (Obstacle Avoidance Control Loop)

		Upon entering this mode, the line PID is suspended and directional control is transferred to the obstacle PID loop. The algorithm tracks an absolute setpoint at the edges of the visual frame to force the cart to veer toward the clear lane:

		<div align="center">
		
		**For green pillars (leave on the left), the system targets `SETPOINT_GREEN = 549` (right edge of the frame).**

		**For red pillars (leave on the right), the system targets `SETPOINT_RED = 50` (left edge of the frame).**

		</div>

		- **Grace Period Mechanism:** Due to the sharpness of the turn, it is common for the pillar to exit the camera’s field of view before the vehicle has physically passed it.

		To prevent the robot from returning prematurely to the center of the track and colliding with the obstacle, an inertia timer (`TIEMPO_GRACIA = 0.2 seconds`) was implemented. If the pillar’s area drops to zero, the system retains the last recorded error (`error_obs = prev_error`), maintaining the turn angle via hardware for the grace period before switching to the OVERTAKING state.

		- **Box-In Safety:** If the ultrasonic sensors detect that the vehicle is dangerously approaching the outer wall of the circuit due to an evasive maneuver (`left_dist or right_dist < DIST_MIN_PARED` of $18.0\text{ cm}$), the machine aborts the vision PID loop and forces an immediate transition to the OVERRUN state to protect structural integrity.
  
	- **State 3:** PASSING (Safety and Return Zone)
    
		This state ensures that the rear of the chassis completely passes the pillar before restoring linear driving conditions. Since the camera no longer has visual contact with the obstacle, control is delegated to the telemetry from the side ultrasonic sensors. The vehicle maintains a controlled compensation angle based on the memorized side to avoid scraping the side wall. The state machine does not allow a return to LINEAR mode until the ultrasonic sensor on the side opposite the pillar registers a clear distance greater than $40\text{ cm}$ (`left_dist > 40` or `right_dist > 40`). This clearance mathematically ensures that the robot’s entire volume has cleared the pillar’s position, preventing snagging on the rear corners or the base of the obstacle.

		As a final layer of protection against loss of visual tracking or imminent collision scenarios, the control loop executes a physical parking brake subroutine in each iteration. If the front ultrasonic sensor detects a distance less than `DIST_MIN_CHOQUE` ($12.0\text{ cm}$), the vehicle cuts power to the motors using `LNM.stop()` and dynamically calculates a reverse escape angle:

		<div align="center">
	
	  	**Escape Angle = 160°**

		</div>
	

		The robot performs a high-power reverse maneuver (`speed = 85`) for $0.75$ seconds, resets the PID integral variables to zero, and restores the running mode to LINEAR, ensuring the software’s resilience in critical traffic congestion conditions.


		- **Flowchart:**
 
		<div align="center">

		<img width="4417" height="6692" alt="untitled@1 25x (4)" src="https://github.com/user-attachments/assets/cad05d6e-52f6-4a7a-926a-9065179510fa" />

		</div>

# 4. Challenges

- ### Hardware Issues:

	**Objective:** Complete three laps autonomously on dynamically configured circuits.

	### Spacing Issues

	During the early development of *Halbi the Green*, issues arose regarding the positioning of components within the base chassis (unmodified). Since the components took up more space than was available, the problem was temporarily resolved by securing them with electrical tape. Although this worked as a stopgap measure, it was not a viable long-term solution. 

	Therefore, it was decided to implement a series of 3D-printed bases designed to add **two additional levels** to the vehicle and **three supplementary mounts** (two on the sides and one at the front) to position the ultrasonic sensors, which originally had no designated location.

	More specifically, the spacing issues and their respective solutions were as follows:

	- **Space occupied by the batteries:**

		- * *Problem:* They took up too much space in the chassis and left no room to comfortably position the components.

    	- *Solution:* A custom base was designed to position them in the center of the robot, and the upper deck was built on top of this structure.
       
	- **Mounting of ultrasonic sensors:**
   
		- *Problem:* There were no designated mounting points to attach them to the original chassis.

    	- *Solution:* Three printed bases were designed to attach to three sides of the chassis.
      
    - *Technical note:* This solution was not entirely ideal, as these bases protrude slightly from the structure, causing mechanical jams when the vehicle passes very close to a corner.
      
	* **Camera and Controller Location:** * *Problem:* There was no physical space to mount the camera or the processing board.
  
    	* *Solution:* A dedicated mount for the Raspberry Pi and the camera was designed on top of the battery base. The camera mount features an adjustable angle to allow for convenient and precise adjustment of the lens’s field of view.

	### Connection Issues (Wiring)

	* **Problem:** Because the cables were loose and exposed, they constantly got caught on the surrounding environment and sometimes even knocked over obstacles on the circuit.
  
	* **Solution:** The connections were completely reorganized to eliminate loops and protruding sections of wiring.

