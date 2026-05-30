```

#include "MeMegaPi.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// --- SYSTEM CONSTANTS ---
#define SERVO_CENTER    90
#define LEFT            0
#define RIGHT           180
#define SERIAL_BAUD     115200
#define SENSOR_TIMEOUT  25000

// --- HARDWARE PIN CONFIGURATION ---
#define BUTTON          A9
#define pinServo        A8
#define trig_front      A15
#define echo_front      A14
#define trig_left       29
#define echo_left       39
#define trig_right      A11
#define echo_right      A10
#define centro          90

// --- VEHICLE ACTUATOR AND SENSOR CONTROL CLASS ---
class Carro {
  private:
    MeMegaPiDCMotor motorTraccion;
    Servo servoDireccion;
    Adafruit_MPU6050 mpu;
    
  public:
    Carro() : motorTraccion(PORT1) {}

    void inicializar() {
      pinMode(BUTTON, INPUT_PULLUP);

      servoDireccion.attach(pinServo);
      servoDireccion.write(centro);
      
      pinMode(trig_front, OUTPUT); pinMode(echo_front, INPUT);
      pinMode(trig_left, OUTPUT);  pinMode(echo_left, INPUT);
      pinMode(trig_right, OUTPUT); pinMode(echo_right, INPUT);

      Serial.println("System: Hardware Initialized");
    }

    // --- SENSOR LOGIC ---
    bool botonPresionado() {
      return digitalRead(BUTTON) == LOW; 
    }

    long obtenerDistancia(int trig, int echo) {
      digitalWrite(trig, LOW);
      delayMicroseconds(2);
      digitalWrite(trig, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig, LOW);
      
      long duracion = pulseIn(echo, HIGH, SENSOR_TIMEOUT);
      long distancia = duracion * 0.034 / 2;
      
      return (distancia <= 0) ? 400 : distancia;
    }

    long getDistanciaFront() { return obtenerDistancia(trig_front, echo_front); }
    long getDistanciaLeft()  { return obtenerDistancia(trig_left, echo_left); }
    long getDistanciaRight() { return obtenerDistancia(trig_right, echo_right); }

    // --- MOTION AND STEERING LOGIC ---
    void avanzar(byte velocidad) {
      motorTraccion.run(velocidad);
    }

    void retroceder(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(-velocidad);
    }

    void girarIzquierda(byte angulo, byte velocidad) {
      int pos = centro + angulo;
      if (pos > LEFT) pos = LEFT;
      servoDireccion.write(pos);
      motorTraccion.run(velocidad);
    }

    void girarDerecha(byte angulo, byte velocidad) {
      int pos = centro - angulo;
      if (pos < RIGHT) pos = RIGHT;
      servoDireccion.write(pos);
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

// --- MAIN SETUP ---
void setup() {
  Serial.begin(SERIAL_BAUD);
  miCarro.inicializar();
}

// --- MAIN EXECUTION LOOP ---
void loop() {
  // --- SERIAL COMMAND PROCESSING (RASPBERRY PI -> ARDUINO) ---
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
        case 3: miCarro.girar
```
