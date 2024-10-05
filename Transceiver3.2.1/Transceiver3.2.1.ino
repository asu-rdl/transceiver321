#include <Wire.h>



void setup(){
  Serial.begin(115200);
  Wire.begin();    
}

void loop(){
  byte data[2];
	while(Serial.available() < 2);

    String str = Serial.readStringUntil('\n');
    if (str.equals("get_id")){
        //ensure empty input
        while(Serial.available()>0){
            Serial.read();
        }
        Serial.println("transceiver_3.2.1");
    }
    else if (str.equals("set_atten"))
    {
        Serial.readBytes(data, 2);
        if (data[0] > 7){
            Serial.println("FAIL, BAD ADDRESS NOT BETWEEN 0 THROUGH 7");
            return;
        }
        if (data[1] > 127){
            Serial.println("FAIL, ATTENUATION VALUE IS TOO LARGE");
            return;
        }
        //ensure empty input
        while(Serial.available()>0){
            Serial.read();
        }

      Wire.beginTransmission(0b0100000+data[0]);
      Wire.write(data[1]);
      int status = Wire.endTransmission();
      if (status == 0){
          Serial.println("OK");
      } else {
          Serial.println("FAIL, NO-ACKNOWLEDGE FROM I2C DEVICE");
      }
    } else {
        Serial.println("BAD COMMAND");
    }

}