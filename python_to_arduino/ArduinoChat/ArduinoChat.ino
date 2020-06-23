
void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  Serial.println("<Arduino is ready>");
}

void loop() {
  if (Serial.available() > 0) {
    Serial.print("<" + Serial.readString() +"to you too>");
  }
}
