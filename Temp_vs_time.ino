const int TempSensor = A0;

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
  int SensorVal = analogRead(TempSensor);
  float Voltage = (SensorVal/1024.0) * 5.0;
  float Temperature = (Voltage - 0.5) * 100.0;
  Serial.println(Temperature);
  delay(100);
}
