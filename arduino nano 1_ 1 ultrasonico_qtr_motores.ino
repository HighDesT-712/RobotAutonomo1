int TRIG1 = 7;

int ECO1 = 6; 

int tiempo1 = 0;

int ultraSonido(int trig, int eco){
  digitalWrite(trig,1);delay(1);digitalWrite(trig,0);//se genera un pulso en el ultrasonido emisor
  int tiempo = pulseIn(eco,1);//se lee cuanto tarda el receptor en detectar la onda
  return tiempo;
}

void setup(){

  Serial.begin(9600);
  pinMode(TRIG1,OUTPUT);

  pinMode(ECO1,INPUT);

}

void loop(){
tiempo1 = ultraSonido(TRIG1, ECO1);
Serial.println(tiempo1-1400);
// se usa como se quiere.

}

