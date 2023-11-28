int TRIG1 = 1;

int ECO1 = 8; 

int tiempo1 = 0;

int ultraSonido(int trig, int eco){
  digitalWrite(trig,1);delay(1);digitalWrite(trig,0);//se genera un pulso en el ultrasonido emisor
  int tiempo = pulseIn(eco,1);//se lee cuanto tarda el receptor en detectar la onda
  return tiempo;
}

void setup(){
  pinMode(TRIG1,OUTPUT);

  pinMode(ECO1,INPUT);

}

void loop(){
tiempo1 = ultrasonido(TRIG1, ECO1);

// se usa como se quiere.

}

