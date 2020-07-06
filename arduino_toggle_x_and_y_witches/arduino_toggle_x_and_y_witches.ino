int x_switch_pin = 3;
int y_switch_pin = 4;

void setup() {
  pinMode(x_switch_pin, INPUT);
  pinMode(y_switch_pin, INPUT);
  Serial.begin(9600);
}

void loop() {
  bool is_x_switch_on = digitalRead(x_switch_pin);
  bool is_y_switch_on = digitalRead(y_switch_pin);
  Serial.print("X: ");
  Serial.println(is_x_switch_on);
  Serial.print("Y: ");
  Serial.println(is_y_switch_on);
  delay(50);

}
