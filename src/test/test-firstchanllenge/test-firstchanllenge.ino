#include "MeMegaPi.h"

#define SERVO_RECTO -5;
#define ANGULO_GIRO 40

MeMegaPiDCMotor motor1(PORT2A);
uint8_t motorSpeed = 60;

Servo servo1;            
const int pinServo = A6;   


void setup()
{
  servo1.attach(pinServo);
  moverServo(SERVO_RECTO); // Centro
}

void loop()
{
  recto();
  avanzar();
  delay(2400);
  girarDerecha();
  delay(1750);
  detener();
}
void recto()
{
  moverServo(SERVO_RECTO);
}
void avanzar()
{
  motor1.run(motorSpeed);
}

void girarDerecha()
{
  moverServo(ANGULO_GIRO);  
  motor1.run(95);       
}

void girarIzquierda()
{
  moverServo(-ANGULO_GIRO);
  motor1.run(95);
}

void detener()
{
  motor1.run(0);
}


void moverServo(int anguloSafe)
{
  anguloSafe = constrain(anguloSafe, -70, 70);

  int anguloServo = anguloSafe + 90;
  servo1.write(anguloServo);
}
