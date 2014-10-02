/*
Arduino sketch for tempo.
When gets 'A' from python code, it reads the value from LM35
and returns the temperature after sending 'ok\n'
*/

float temp;
int reading;

void setup()
{
  analogReference(INTERNAL);
  int temp_pin = 0;
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0){
    incoming = Serial.read();
    if (incoming == 'A'){
      // Reading
      reading = analogRead(temp_pin);
      temp = reading / 9.31;
      // Sending
      Serial.println("ok");
      Serial.println(temp);
    }
  }
}
