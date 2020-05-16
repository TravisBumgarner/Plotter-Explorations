#define joystickY A1
#define joystickSelect 2
int motorPosition = 0;

void setup() {
  Serial.begin(9600);
  digitalWrite(joystickSelect, HIGH);
}

void loop() {
    int yValue = analogRead(joystickY);
    int selectValue = digitalRead(joystickSelect);
    
    if (yValue > 1000){
      motorPosition--;
      delay(50);
    } else if (yValue < 10){
      motorPosition++;
      delay(50);
    } else if (selectValue == 0){
      motorPosition = 0;
      delay(50);
    }
    Serial.println(motorPosition);
}
