#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
const char* ssid = "ahihi";
const char* password = "phongbui97";
#define buttonPin 14
#define LED 12
int tick=0;
String time_signal="";


String macToStr(const uint8_t* mac)
{
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    if (i < 5)
      result += ':';
  }
  return result;
}


void setup () {
 pinMode(buttonPin, INPUT_PULLUP);
 pinMode(LED,OUTPUT);
 Serial.begin(115200);
 WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.print("Connecting..");
  }
}


void post_request(String data){
   if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
 
   HTTPClient http;    //Declare object of class HTTPClient
 
   http.begin("http://35.236.172.46:5000/api_1_0/getdata/nodemcu");      //Specify request destination
   http.addHeader("Content-Type", "text/plain");  //Specify content-type header
 
   int httpCode = http.POST(data);   //Send the request
   String payload = http.getString();                  //Get the response payload
 
   Serial.println(httpCode);   //Print HTTP return code
   Serial.println(payload);    //Print request response payload
 
   http.end();  //Close connection
 
 }else{
 
    Serial.println("Error in WiFi connection");   
 
 }
  }



void timeStore(){
long time_now= millis();
Serial.println(time_now);
time_signal= time_signal + time_now;
time_signal= time_signal + "-";
Serial.println(time_signal);
}

  
void loop() {
 
 if((digitalRead(buttonPin) == 0)){
  tick= tick + 1;
  Serial.println(tick);
  
  
  }
 if((digitalRead(buttonPin) == 1)){
  if (tick <10){
    tick=0;
    }
  else if ((10<tick) and (tick < 500)){
  timeStore();
  tick = 0;
  }

  else{
    Serial.println("Long press");
    post_request(time_signal);
    time_signal="";
    tick=0;
    }
  }
 
}
