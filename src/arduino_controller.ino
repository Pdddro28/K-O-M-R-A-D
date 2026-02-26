// --------------------libraries------------------------
#include "MeMegaPi.h"
#include <Servo.h>
// --------------------libraries------------------------

// --------------------Constants------------------------
// Default servo position for straight movement
#define SERVO_CENTER 90
// Maximum and minimum safety limits for steering
#define MAX_LEFT 180
#define MIN_RIGHT 0
// --------------------Constants------------------------

class Carro {
  private:
    MeMegaPiDCMotor motorTraccion; // DC motor instance
    Servo servoDireccion;          // Steering servo instance
    const int pinServo = A6;       // Signal pin for the servo
    const int centro = SERVO_CENTER;

  public:
    // Constructor: Initializes the motor on MegaPi PORT1
    Carro() : motorTraccion(PORT1) {} 

    // Hardware configuration
    void inicializar() {
      servoDireccion.attach(pinServo);
      servoDireccion.write(centro); // Set initial position to 90 degrees
      Serial.println("Carro Inicializado");
    }

    // Moves the car forward at a specific PWM speed
    void avanzar(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(velocidad); 
    }

    // Moves the car backward at a specific PWM speed
    void retroceder(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(-velocidad); // Negative value for reverse rotation
    }

    // Turns the front wheels left by a given angle and moves
    void girarIzquierda(byte angulo, byte velocidad) {
      int pos = centro + angulo;
      if (pos > MAX_LEFT) pos = MAX_LEFT; // Safety bound
      servoDireccion.write(pos);
      motorTraccion.run(velocidad); 
    }

    // Turns the front wheels right by a given angle and moves
    void girarDerecha(byte angulo, byte velocidad) {
      int pos = centro - angulo;
      if (pos < MIN_RIGHT) pos = MIN_RIGHT; // Safety bound
      servoDireccion.write(pos);
      motorTraccion.run(velocidad);
    }

    // Stops the traction motor and centers the steering
    void detenerse() {
      motorTraccion.stop();
      servoDireccion.write(centro);
    }
};

// Global instance of the car
Carro miCarro;

// --------------------Setup------------------------
void setup() {
  // Serial communication at 115200 baud for Raspberry Pi 4 link
  Serial.begin(115200);
  miCarro.inicializar();
}
// --------------------Setup------------------------

// --------------------Main Loop--------------------
void loop() {
  // Protocol: [Header(0xFF), Type(0x01), Action, Val1, Val2]
  // Requires exactly 5 bytes to process a command
  if (Serial.available() >= 5) {
    byte header = Serial.read();
    
    // Check for start of packet
    if (header == 0xFF) {
      byte tipo = Serial.read();   // Reserved for future sensor data types
      byte accion = Serial.read(); // Command ID (1 to 5)
      byte v1 = Serial.read();     // Primary parameter: Velocity or Angle
      byte v2 = Serial.read();     // Secondary parameter: Velocity during turns

      // Execution logic based on Action ID
      switch (accion) {
        case 1: // Forward
          miCarro.avanzar(v1);
          break;
        case 2: // Backward
          miCarro.retroceder(v1);
          break;
        case 3: // Turn Left
          miCarro.girarIzquierda(v1, v2);
          break;
        case 4: // Turn Right
          miCarro.girarDerecha(v1, v2);
          break;
        case 5: // Stop All
          miCarro.detenerse();
          break;
        default:
          // Invalid command received
          miCarro.detenerse();
          break;
      }
    }
  }
}
// --------------------Main Loop--------------------
