/* Joystick Setup */
#define joystickY A1
#define joystickSelect 2
int motorPosition = 0;
/* End Joystick Setup */

/* Screen Setup */
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <SPI.h>

#define TFT_CS        10
#define TFT_RST        9
#define TFT_DC         8

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);
/* End Screen Setup */

/* Motor Setup */
#include <Stepper.h>
const int stepsPerRevolution = 200; 
Stepper myStepper(stepsPerRevolution, 3,4,5,6);
/* End Motor Setup */

void setup() {
  Serial.begin(9600);
  digitalWrite(joystickSelect, HIGH);

  tft.init(240, 240); 
  tft.fillScreen(ST77XX_BLACK);

  myStepper.setSpeed(60);
}
/*
 * 60 rpm
 * 1 rotation per second
 * 1 rotation = 200 steps
 * 1/200th of second 
 */ 
void loop() {
    int yValue = analogRead(joystickY);
    int selectValue = digitalRead(joystickSelect);

    if (yValue > 900){
      motorPosition--;
      drawText(String(motorPosition));
      myStepper.step(-1);
    } else if (yValue < 100){
      motorPosition++;
      drawText(String(motorPosition));
      myStepper.step(1);
    } else if (selectValue == 0){
      myStepper.step(-motorPosition);
      motorPosition = 0;
      drawText(String(motorPosition));
    }
    
    Serial.println(motorPosition);

    
}

void drawText(String text) {
  tft.setCursor(0, 0);
  tft.setTextColor(ST77XX_WHITE, ST77XX_BLACK);
  tft.setTextSize(2);
  tft.setTextWrap(true);
  tft.print(text);
}
