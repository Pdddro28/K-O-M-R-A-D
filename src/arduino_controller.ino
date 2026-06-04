#include "MeMegaPi.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include "Ultrasonic.h"

// --- Constantes del Sistema ---
#define SERVO_CENTER    90
#define LEFT            0
#define RIGHT           180
#define SERIAL_BAUD     115200
#define SENSOR_TIMEOUT  25000

// Pines de Hardware
#define BUTTON          A9
#define pinServo        A7
#define trig_front      A15
#define echo_front      A14
#define trig_left       29
#define echo_left       39
#define trig_right      A11
#define echo_right      A10
#define centro          90

Ultrasonic sensorF(A15,A14);
Ultrasonic sensorL(29,39);
Ultrasonic sensorD(A11,A10);


class Carro {
  private:
    MeMegaPiDCMotor motorTraccion;
    Servo servoDireccion;
    Adafruit_MPU6050 mpu;
    
  public:
    // Motor conectado al Puerto 1 de la MegaPi
    Carro() : motorTraccion(PORT4B) {}

    void inicializar() {
      // Configuración del botón (Pull-up interna)
      pinMode(BUTTON, INPUT_PULLUP);

      // Configuración del Servo
      servoDireccion.attach(pinServo);
      servoDireccion.write(centro);
      
      /*
      // Inicialización del MPU6050 (I2C)
      if (!mpu.begin()) {
        Serial.println("System: MPU6050 NOT Found");
      } else {
        Serial.println("System: MPU6050 Initialized");
        mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
        mpu.setGyroRange(MPU6050_RANGE_500_DEG);
        mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
      }
      */
      Serial.println("System: Hardware Initialized");
    }

    // --- Lógica de Sensores ---
    bool botonPresionado() {
      return digitalRead(BUTTON) == LOW; // LOW porque usa INPUT_PULLUP
    }

    long obtenerDistancia(int trig, int echo) {
      digitalWrite(trig, LOW);
      delayMicroseconds(2);
      digitalWrite(trig, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig, LOW);
      
      long duracion = pulseIn(echo, HIGH, SENSOR_TIMEOUT);
      long distancia = duracion * 0.034 / 2;
      
      // Si el sensor da 0 (fuera de rango), devolvemos 400cm como valor seguro
      return (distancia <= 0) ? 400 : distancia;
    }

    long getDistanciaFront() { return sensorF.read(); }
    long getDistanciaLeft()  { return sensorL.read(); }
    long getDistanciaRight() { return sensorD.read(); }

    // --- Lógica de Movimiento ---
    void avanzar(byte velocidad) {
      motorTraccion.run(velocidad);
    }

    void retroceder(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(-velocidad);
    }

    void girarIzquierda(byte angulo, byte velocidad) {
      servoDireccion.write(angulo);
      motorTraccion.run(velocidad);
    }

    void girarDerecha(byte angulo, byte velocidad) {
      servoDireccion.write(angulo);
      motorTraccion.run(velocidad);
    }

    void detenerse() {
      motorTraccion.stop();
      servoDireccion.write(centro);
    }

    void girarCentro() {
      servoDireccion.write(centro);
    }
};

Carro miCarro;
unsigned long timerSensores = 0;

void setup() {
  Serial.begin(SERIAL_BAUD);
  miCarro.inicializar();
}

void loop() {
  // --- PARTE 1: Procesamiento de Comandos (Raspberry -> Arduino) ---
  if (Serial.available() >= 5) {
    byte header = Serial.read();
    if (header == 0xFF) {
      byte tipo   = Serial.read();
      byte accion = Serial.read();
      byte v1     = Serial.read(); // Velocidad o Ángulo
      byte v2     = Serial.read(); // Velocidad secundaria

      switch (accion) {
        case 1: miCarro.avanzar(v1); break;
        case 2: miCarro.retroceder(v1); break;
        case 3: miCarro.girarIzquierda(v1, v2); break;
        case 4: miCarro.girarDerecha(v1, v2); break;
        case 5: miCarro.detenerse(); break;
        case 6: miCarro.girarCentro(); break;
        case 7: miCarro.inicializar(); break; // Reiniciar configuración
        default: miCarro.detenerse(); break;
      }
    }
  }

  // --- PARTE 2: Telemetría (Arduino -> Raspberry) cada 100ms ---
  if (millis() - timerSensores > 100) {
    int d_front = (int)miCarro.getDistanciaFront();
    int d_left  = (int)miCarro.getDistanciaLeft();
    int d_right = (int)miCarro.getDistanciaRight();
    byte estadoBoton = miCarro.botonPresionado() ? 1 : 0;
    
    // Paquete de Telemetría (6 bytes en total)
    Serial.write(0xAA);                        // Byte 0: Header
    Serial.write(constrain(d_front, 0, 255));  // Byte 1: Frontal
    Serial.write(constrain(d_left, 0, 255));   // Byte 2: Izquierda
    Serial.write(constrain(d_right, 0, 255));  // Byte 3: Derecha
    Serial.write(estadoBoton);                 // Byte 4: Botón (0 o 1)
    Serial.write(0x00);                        // Byte 5: Relleno (Padding)
    
    timerSensores = millis();
  }
}