#include "MeMegaPi.h"

class Carro {
  private:
    MeMegaPiDCMotor motorIzquierdo;
    MeMegaPiDCMotor motorDerecho;

  public:
    Carro() : motorIzquierdo(PORT1), motorDerecho(PORT2) {}

    void avanzar(byte v1, byte v2) {
      motorDerecho.run(v2);
      motorIzquierdo.run(-v1);
    }

    void retroceder(byte v1, byte v2) {
      motorDerecho.run(-v2);
      motorIzquierdo.run(v1);
    }

    void girarIzquierda(byte v1, byte v2) {
      motorIzquierdo.run(-v1);
      motorDerecho.run(-v2);
    }

    void girarDerecha(byte v1, byte v2) {
      motorIzquierdo.run(v1);
      motorDerecho.run(v2);
    }

    void detenerse() {
      motorIzquierdo.stop();
      motorDerecho.stop();
    }
};

Carro miCarro;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() >= 5) {
    byte header = Serial.read();
    if (header == 0xFF) {
      byte tipo = Serial.read();
      byte accion = Serial.read();
      byte v1 = Serial.read();
      byte v2 = Serial.read();

      if (accion == 1) miCarro.avanzar(v1, v2);
      else if (accion == 2) miCarro.retroceder(v1, v2);
      else if (accion == 3) miCarro.girarIzquierda(v1, v2);
      else if (accion == 4) miCarro.girarDerecha(v1, v2);
      else if (accion == 5) miCarro.detenerse();
    }
  }
}
