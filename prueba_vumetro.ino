//En estas variables se van a guardar los valores crudos de los potenciometros. Que va de 0 a 1024
int pot1 = 0;
int pot2 = 0;
int pot3 = 0;
int pot4 = 0;
int pot5 = 0;
int pot6 = 0;


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(300);
  pinMode(3, OUTPUT);//Pin VUmetro 1
  pinMode(5, OUTPUT);//Pin VUmetro 2
  pinMode(6, OUTPUT);//Pin Luces
}


int linearizar(int raw) { //Esta funcion sirve para mapear los valores de los potenciometros de 0 a 100 de forma lineal
  const int raw_th = 830;
  if (raw <= raw_th) {
    return map(raw,0,raw_th,0,40);
  } else {
    return map(raw,raw_th,1023,40,100);
  }
}
void loop() {
  if (Serial.available()) { //Si hay algo para leer en serial
    //Los paquetes de handshake tienen el formato [0.hs]
    //Los paquetes de sonido tienen el formato [1.0,0] donde cada 0 representa la intensidad de db de cada canal
    //Los paquetes de iluminacion tienen el formato [2.0] donde el 0 representa la intensidad de la luz que debe ponerse
    int tipo = Serial.readStringUntil('.').toInt();
    if (tipo == 5){ //Paquete de tipo HandShake, el arduino debe contestar con un paquete rs, el tipo de paquete es 5 porque no podia ser cero ya que al leerse de nuevo daba vacio y el vacio en toInt es 0 
      byte header = 0xAA;
      byte comando = 0x01;
      byte checksum = header ^ comando;
      byte paquete[3] = {header, comando, checksum};
      Serial.write(paquete, 3);
    }
    if (tipo == 1){ //Paquete de sonido
      String input_der = Serial.readStringUntil(',');
      String input_izq = Serial.readStringUntil('\n');
      int valor_der = input_der.toInt();
      int valor_izq = input_izq.toInt();
      valor_izq = constrain(valor_izq, 0, 255);
      valor_der = constrain(valor_der, 0, 255);
      analogWrite(3, valor_der);
      analogWrite(5, valor_izq);
    } 
    if (tipo == 2){//Paquete de iluminacion
      int intensidad = Serial.readStringUntil('\n').toInt();
      intensidad = intensidad*2.55;
      analogWrite(6, intensidad);
    }
  }
  
  //if (analogRead(A0) < pot1-3 || analogRead(A0) > pot1+3){
  //  pot1 = analogRead(A0);
  //  int pot1_norm = linearizar(analogRead(A0));
  //  Serial.print("Pot1: ");
  //  Serial.println(pot1_norm);
  //}
  Serial.print("pot1: ");
  Serial.println(analogRead(A0));
  delay(10);
  }
