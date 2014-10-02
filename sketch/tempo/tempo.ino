float temp;
int reading;

void setup()
{
  analogReference(INTERNAL);
  int temp_pin = 0;
}

void loop()
{
  reading = analogRead(temp_pin);
  temp = reading / 9.31;
}
