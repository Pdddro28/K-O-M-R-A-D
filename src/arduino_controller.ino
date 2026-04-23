#include "MeMegaPi.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// --- System Constants ---
#define SERVO_CENTER    90
#define MAX_LEFT        180
#define MIN_RIGHT       0
#define SERIAL_BAUD     115200
#define SENSOR_TIMEOUT  25000

class Carro {
  private:
    MeMegaPiDCMotor motorTraccion;
    Servo servoDireccion;
    Adafruit_MPU6050 mpu;
    
    const int pinServo = A6;
    const int centro   = SERVO_CENTER;
    
    const int trig_front = A15;
    const int echo_front = A14;
    const int trig_left  = A13;
    const int echo_left  = A12;
    const int trig_right = A11;
    const int echo_right = A10;

    const int botonPin = A7;

  public:
    Carro() : motorTraccion(PORT1) {}

    void inicializar() {
      boton.

      servoDireccion.attach(pinServo);
      servoDireccion.write(centro);
      
      // Ultrasonic pins setup
      pinMode(trig_front, OUTPUT); pinMode(echo_front, INPUT);
      pinMode(trig_left, OUTPUT);  pinMode(echo_left, INPUT);
      pinMode(trig_right, OUTPUT); pinMode(echo_right, INPUT);
      
      // MPU6050 IMU
      if (!mpu.begin()) {
        Serial.println("System: MPU6050 NOT Found");
      } else {
        Serial.println("System: MPU6050 Initialized");
        mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
        mpu.setGyroRange(MPU6050_RANGE_500_DEG);
        mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
      }
      
      Serial.println("System: Hardware Initialized");
    }

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

    void getMPUData(int8_t &accelX, int8_t &accelY, int8_t &gyroZ) {
      sensors_event_t a, g, temp;
      mpu.getEvent(&a, &g, &temp);
      accelX = (int8_t)constrain(a.acceleration.x * 10, -128, 127);
      accelY = (int8_t)constrain(a.acceleration.y * 10, -128, 127);
      gyroZ  = (int8_t)constrain(g.gyro.z * 10, -128, 127);
    }

    long getDistanciaFront() { return obtenerDistancia(trig_front, echo_front); }
    long getDistanciaLeft()  { return obtenerDistancia(trig_left, echo_left); }
    long getDistanciaRight() { return obtenerDistancia(trig_right, echo_right); }

    void avanzar(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(velocidad);
    }

    void retroceder(byte velocidad) {
      servoDireccion.write(centro);
      motorTraccion.run(-velocidad);
    }

    void girarIzquierda(byte angulo, byte velocidad) {
      int pos = centro + angulo;
      if (pos > MAX_LEFT) pos = MAX_LEFT;
      servoDireccion.write(pos);
      motorTraccion.run(velocidad);
    }

    void girarDerecha(byte angulo, byte velocidad) {
      int pos = centro - angulo;
      if (pos < MIN_RIGHT) pos = MIN_RIGHT;
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

void setup() {
  Serial.begin(SERIAL_BAUD);
  miCarro.inicializar();
}

void loop() {
  // Part 1: Serial Command Processing
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
        case 6: miCarro.girarCentro(); break;
        case 7: miCarro.iniciar(); break;
        default: miCarro.detenerse(); break;
      }
    }
  }

  // Part 2: Telemetry Update (3 distances + 2 padding)
  if (millis() - timerSensores > 100) {
    int d_front = (int)miCarro.getDistanciaFront();
    int d_left  = (int)miCarro.getDistanciaLeft();
    int d_right = (int)miCarro.getDistanciaRight();
    
    Serial.write(0xAA);              // Header
    Serial.write(constrain(d_front, 0, 255));  // Byte 1: Front
    Serial.write(constrain(d_left, 0, 255));   // Byte 2: Left
    Serial.write(constrain(d_right, 0, 255));  // Byte 3: Right
    Serial.write(0x00);              // Byte 4: Padding
    Serial.write(0x00);              // Byte 5: Padding
    
    timerSensores = millis();
  }
}
