#include <Stepper.h>
const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

int switchPin = 12;

String readString;
String x_position_instruction;
String y_position_instruction;
String z_position_instruction;

int x_pos = 0;

int ind1;
int ind2;
 
void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
  pinMode(switchPin, INPUT);

  myStepper.setSpeed(60);
}

void loop() {
  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == '\n') {     
      ind1 = readString.indexOf(',');  //finds location of first ,
      x_position_instruction = readString.substring(0, ind1);   //captures first data String
      ind2 = readString.indexOf(',', ind1 + 1);   //finds location of second ,
      y_position_instruction = readString.substring(ind1 + 1, ind2);   //captures second data String
      z_position_instruction = readString.substring(ind2 + 1);

      int x_current = 0;
      while(x_current < x_position_instruction.toInt()){
          int val = digitalRead(switchPin);
          if(val == HIGH){
            break;  
          }
          myStepper.step(1);
          x_current++;
      }
      
     Serial.print("x_pos = ");
     Serial.print(x_position_instruction);
     Serial.print("y_pos = ");
     Serial.print(y_position_instruction);
     Serial.print("z_pos = ");
     Serial.print(z_position_instruction);
     Serial.println();
     
      readString=""; //clears variable for new input
      x_position_instruction="";
      y_position_instruction="";
      z_position_instruction="";
    } 
    else {     
      readString += c; //makes the string readString
    }
  }
}
