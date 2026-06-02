//const byte HEADER = 255;
//tipo_de_comando, accion, arg1, arg2

void setup() {
  Serial.begin(115200);
  Serial.println("MegaPi lista :)");
}

void loop() {

  if (Serial.available() > 0) {
    String entrada = Serial.readStringUntil('\n');
    entrada.trim();

    if (entrada.length() > 0) {
      int tipo_de_comando,accion, arg1, arg2;
      int campos = sscanf(entrada.c_str(), "%d,%d,%d,%d", &tipo_de_comando, &accion, &arg1, &arg2);

      if (campos == 4) {
        procesarComandoTexto(tipo_de_comando, accion, arg1, arg2);
      } else {
        Serial.println("Error");
      }
    }
  }
//  if (Serial.available() >= 5) {
//    byte checkHeader = Serial.read();
//    if (checkHeader == HEADER) {
//      byte tipo_de_comando = Serial.read();
//      byte accion = Serial.read();
//      byte arg1 = Serial.read();
//      byte arg2 = Serial.read();
//
//      procesarComando(tipo_de_comando, accion, arg1, arg2);
//    }
//  }
}

void procesarComandoTexto(int tipo_de_comando, int accion, int arg1, int arg2) {
  Serial.print("Ejecutando tipo: "); Serial.print(tipo_de_comando);
  Serial.print(" Accion: "); Serial.print(accion);

  //if (tipo == 1 && accion == 1) {
    //motor1.run(arg1);
    //motor2.run(arg2);
  //}
}

//void procesarComando(byte tipo, byte accion, byte arg1, byte arg2) {
//  if (tipo == 1) {

//    if (accion == 1) {
//      moverAdelante(arg1, arg2);
//    } else if (accion == 0) {
//      detenerMotores();
//    }
//  }
//}

void moverAdelante(byte velI, byte velD) {
  // motorIz.run(velI);
}

void detenerMotores() {
  // frenar todo
}
