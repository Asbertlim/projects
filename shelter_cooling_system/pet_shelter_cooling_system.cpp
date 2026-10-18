const int temperaturePin = A0;
const int fanPin = 7;

const float ON_TEMP = 23.0;
const float OFF_TEMP = 22.0;

void setup() {
  Serial.begin(9600);

  pinMode(fanPin, OUTPUT);
  digitalWrite(fanPin, LOW);
}

void loop() {

  int reading = analogRead(temperaturePin);

  float voltage = reading * (5.0 / 1023.0);

  float temperature = (voltage - 0.5) * 100;

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");

  if (temperature >= ON_TEMP) {
    digitalWrite(fanPin, HIGH);
  }
  else if (temperature <= OFF_TEMP) {
    digitalWrite(fanPin, LOW);
  }

  delay(1000);
}

