#define HEADER 0xAA
void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() >= 4){
    if(Serial.read() == HEADER){
      uint8_t tipo = Serial.read()
      uint8_t accion = Serial.read()
      uint8_t valor1 = Serial.read()
      uint8_t valor2 = Serial.read()
      excuteComand()
    }
  }
}
