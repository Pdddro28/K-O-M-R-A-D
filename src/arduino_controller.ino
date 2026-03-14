#include "MeMegaPi.h"

// --- System Constants ---
#define SERVO_CENTER   90    // Default neutral position for steering
#define MAX_LEFT       180   // Maximum hardware limit for left turn
#define MIN_RIGHT      0     // Minimum hardware limit for right turn
#define SERIAL_BAUD    115200 // Communication speed for RPi4 link
#define SENSOR_TIMEOUT 25000 // Pulse timeout in microseconds (~4 meters)

/**
 * Carro
 * Handles low-level hardware control for traction, steering, and sensing.
 */
class Carro {
  private:
    MeMegaPiDCMotor motorTraccion; // Main DC motor connected to PORT1
    Servo servoDireccion;          // Front axle steering servo
    
    // Pin Definitions
    const int pinServo = A6;       
    const int centro   = SERVO_CENTER;
    
    // HC-SR04 Ultrasonic Sensor Pins
    const int trig1 = A15;
    const int echo1 = A14;
    const int trig2 = A13;
    const int echo2 = A12;

  public:
    /**
     * Constructor initializes the DC motor on MegaPi PORT1.
     */
    Carro() : motorTraccion(PORT1) {} 

    /**
     * Configures hardware pins and attaches the steering servo.
     */
    void inicializar() {
      servoDireccion.attach(pinServo);
      servoDireccion.write(centro);
      
      // Ultrasonic pins setup
      pinMode(trig1, OUTPUT);
      pinMode(echo1, INPUT);
      pinMode(trig2, OUTPUT);
      pinMode(echo2, INPUT);
      
      Serial.println("System: Hardware Initialized");
    }

    /**
     * Measures distance using HC-SR04 ultrasonic sensors.
     * Trigger pin
     * Echo pin
     * Distance in centimeters (returns 400 if no echo).
     */
    long obtenerDistancia(int trig, int echo) {
      digitalWrite(trig, LOW);
      delayMicroseconds(2);
      digitalWrite(trig, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig, LOW);
      
      long duracion = pulseIn(echo, HIGH, SENSOR_TIMEOUT); 
      long distancia = duracion * 0.034 / 2;
      
      return (distancia == 0) ? 400 : distancia;
    }

    // Helper methods for telemetry
    long getDistancia1() { return obtenerDistancia(trig1, echo1); }
    long getDistancia2() { return obtenerDistancia(trig2, echo2); }

    /**
     * Moves the car forward at a set speed while centering steering.
     * PWM speed (0-255).
     */
    void avanzar(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(velocidad); 
    }

    /**
     * Moves the car backward.
     */
    void retroceder(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(-velocidad);
    }

    /**
     * Executes a left turn by adding an offset to the center.
     * Degrees to add (0-90).
     * Movement speed during turn.
     */
    void girarIzquierda(byte angulo, byte velocidad) {
      int pos = centro + angulo;
      if (pos > MAX_LEFT) pos = MAX_LEFT;
      servoDireccion.write(pos);
      motorTraccion.run(velocidad); 
    }

    /**
     * Executes a right turn by subtracting an offset from center.
     */
    void girarDerecha(byte angulo, byte velocidad) {
      int pos = centro - angulo;
      if (pos < MIN_RIGHT) pos = MIN_RIGHT;
      servoDireccion.write(pos);
      motorTraccion.run(velocidad);
    }

    /**
     * Safety function to stop motors and reset steering.
     */
    void detenerse() {
      motorTraccion.stop();
      servoDireccion.write(centro);
    }
};

// Global Instance
Carro miCarro;
unsigned long timerSensores = 0; // Telemetry timing tracker

// ---------------------------------------------------------
// Setup
// ---------------------------------------------------------
void setup() {
  Serial.begin(SERIAL_BAUD);
  miCarro.inicializar();
}

// ---------------------------------------------------------
// Main Control Loop
// ---------------------------------------------------------
void loop() {
  /* * Part 1: Serial Command Processing (RPi4 -> MegaPi)
   * Protocol format: [0xFF, Type, Action, Param1, Param2]
   */
  if (Serial.available() >= 5) {
    byte header = Serial.read();
    if (header == 0xFF) {
      byte tipo   = Serial.read();   
      byte accion = Serial.read(); 
      byte v1     = Serial.read();     
      byte v2     = Serial.read();     

      switch (accion) {
        case 1: miCarro.avanzar(v1); break;
        case 2: miCarro.retroceder(v1); break;
        case 3: miCarro.girarIzquierda(v1, v2); break;
        case 4: miCarro.girarDerecha(v1, v2); break;
        case 5: miCarro.detenerse(); break;
        default: miCarro.detenerse(); break;
      }
    }
  }

  /* * Part 2: Periodic Telemetry Update (MegaPi -> RPi4)
   * Broadcasts sensor data every 100ms.
   */
  if (millis() - timerSensores > 100) {
    int d1 = (int)miCarro.getDistancia1();
    int d2 = (int)miCarro.getDistancia2();
    
    // Telemetry Packet: [Header, Sensor1, Sensor2, Padding, Padding]
    Serial.write(0xAA); 
    Serial.write(constrain(d1, 0, 255));
    Serial.write(constrain(d2, 0, 255));
    Serial.write(0x00);
    Serial.write(0x00);
    
    timerSensores = millis();
  }
}
