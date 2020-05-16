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


void setup() {
  Serial.begin(9600);
  digitalWrite(joystickSelect, HIGH);

  tft.init(240, 240); 
  tft.fillScreen(ST77XX_BLACK);
}

void loop() {
    int yValue = analogRead(joystickY);
    int selectValue = digitalRead(joystickSelect);
    
    if (yValue > 1000){
      motorPosition--;
      drawText(String(motorPosition), ST77XX_WHITE);
      delay(50);
    } else if (yValue < 10){
      motorPosition++;
      drawText(String(motorPosition), ST77XX_WHITE);
      delay(50);
    } else if (selectValue == 0){
      motorPosition = 0;
      drawText(String(motorPosition), ST77XX_WHITE);
      delay(50);
    }
    Serial.println(motorPosition);

    
}

void drawText(String text, uint16_t color) {
  tft.fillScreen(ST77XX_BLACK);
  tft.setCursor(0, 0);
  tft.setTextColor(color);
  tft.setTextSize(10);
  tft.setTextWrap(true);
  tft.print(text);
}
