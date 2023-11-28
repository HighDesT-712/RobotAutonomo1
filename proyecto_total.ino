const int motorPin1 = 2;    // 28BYJ48 In1
const int motorPin2 = 3;    // 28BYJ48 In2
const int motorPin3 = 4;   // 28BYJ48 In3
const int motorPin4 = 5;   // 28BYJ48 In4

//definicion variables
int motorSpeed = 900;   //variable para fijar la velocidad
int stepCounter = 0;     // contador para los pasos
int stepsPerRev = 4076;  // pasos para una vuelta completa
 
//secuencia media fase
const int numSteps = 8;
const int stepsLookup[8] = { B1000, B1100, B0100, B0110, B0010, B0011, B0001, B1001 };
 
 
void setup()
{
  //declarar pines como salida
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
}
 
void loop()
{
  for (int i = 0; i < stepsPerRev * 2; i++)
  {
    clockwise();
    delayMicroseconds(motorSpeed);
  }
  for (int i = 0; i < stepsPerRev * 2; i++)
  {
    anticlockwise();
    delayMicroseconds(motorSpeed);
  }
  delay(1000);
}

int ultraSonido(int trig,int eco){
  digitalWrite(trig,1);delay(1);digitalWrite(trig,0);//se genera un pulso en el ultrasonido emisor
  int tiempo = pulseIn(eco,1);//se lee cuanto tarda el receptor en detectar la onda
  return tiempo; 
}
 
void clockwise()
{
  stepCounter++;
  if (stepCounter >= numSteps) stepCounter = 0;
  setOutput(stepCounter);
}
 
void anticlockwise()
{
  stepCounter--;
  if (stepCounter < 0) stepCounter = numSteps - 1;
  setOutput(stepCounter);
}
 
void setOutput(int step)
{
  digitalWrite(motorPin1, bitRead(stepsLookup[step], 0));
  digitalWrite(motorPin2, bitRead(stepsLookup[step], 1));
  digitalWrite(motorPin3, bitRead(stepsLookup[step], 2));
  digitalWrite(motorPin4, bitRead(stepsLookup[step], 3));
}
