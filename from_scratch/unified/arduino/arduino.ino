String readString;

void read_gcode_from_serial(int instruction[3])
{
  while(Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
    int ind1 = readString.indexOf(',');
      String x_pos = readString.substring(0, ind1);
      int ind2 = readString.indexOf(',', ind1 + 1);
      String y_pos = readString.substring(ind1 + 1, ind2);
      String z_pos = readString.substring(ind2 + 1);
      instruction[0] = x_pos.toInt();
      instruction[1] = y_pos.toInt();
      instruction[2] = z_pos.toInt();
      readString = "";
      return;
    } else {
      readString += c;
    }
    
  }
}


void setup()
{
  Serial.begin(9600);
  Serial.println("Ready");
}

void loop()
{
  int instruction[3] = {-1 ,-1, -1};
  read_gcode_from_serial(instruction);
  if(instruction[0] != -1 && instruction[1] != -1 && instruction[2] != -1){
    Serial.println("x_pos=" + String(instruction[0]) + " y_pos=" + String(instruction[1]) + " z_pos=" + String(instruction[2]));
  }

}
