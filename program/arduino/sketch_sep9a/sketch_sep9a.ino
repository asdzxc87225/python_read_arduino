unsigned long previousMillis = 0;
const long interval = 100;    // 設定間隔時間，1000ms
char chr;

void setup() {
  Serial.begin(9600);
}

void loop() {
  unsigned long currentMillis = millis();
  int sensorValue = analogRead(A0);
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    Serial.print("sensor ");
    Serial.print(sensorValue);
    Serial.print(" \n");
  }
}