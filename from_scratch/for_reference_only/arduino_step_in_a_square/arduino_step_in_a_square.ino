#include <Stepper.h>

const int stepsPerRevolution = 200; 

Stepper x_stepper(stepsPerRevolution, 10,11,12,13);
Stepper y_stepper(stepsPerRevolution, 5,6,7,8);

void setup() {
  Serial.begin(9600);
}
int x = 0;
int y = 0;

boolean is_x_stepping = false;

boolean is_x_positive = true;
boolean is_y_positive = true;

void loop() {
  if(is_x_stepping) {
    if(is_x_positive){
      x += 5;
      x_stepper.step(5);
    } else {
      x -= 5;
      x_stepper.step(-5);
    }
    if(x > 400 || x < 0){
      is_x_positive = !is_x_positive;
      is_x_stepping = !is_x_stepping;
    }
  } else {
      if(is_y_positive){
      y += 5;
      y_stepper.step(5);
    } else {
      y -= 5;
      y_stepper.step(-5);
    }
    if(y > 400 || y < 0){
      is_y_positive = !is_y_positive;
      is_x_stepping = !is_x_stepping;
    }
  }
  delay(10);
  
  Serial.println(x);
}
