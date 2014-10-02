/*
Arduino sketch for tempo.
When gets 'A' from python code, it reads the value from LM35
and returns the temperature after sending 'ok\n'
*/

float temp;
int reading;
int temp_pin = 0;

void setup()
{
  //analogReference(INTERNAL);
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0){
    char incoming = Serial.read();
    if (incoming == 'A'){
      // Reading
      reading = analogRead(temp_pin);
      temp = (500 * reading ) / 1024;
      // Sending
      Serial.println("ok");
      Serial.println(temp);
    }
  }
}
