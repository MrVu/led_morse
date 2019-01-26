#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>


//khai bao bien
const char* ssid = "ahihi";
const char* password = "phongbui97";
#define buttonPin 5
#define LED 4
int tick = 0;
String time_signal = "";



void setup () {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.print("Connecting..");
  }

}


void post_request(String data) {
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;    //Declare object of class HTTPClient

    http.begin("http://35.236.172.46:5000/api_1_0/senddata");      //Specify request destination
    http.addHeader("Content-Type", "text/plain");  //Specify content-type header

    int httpCode = http.POST(data);   //Send the request
    String payload = http.getString();                  //Get the response payload

    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

  } else {

    Serial.println("Error in WiFi connection");

  }
}


//ham bien timestamp thanh String
void timeStore() {
  long time_now = millis();
  Serial.println(time_now);
  time_signal = time_signal + time_now;
  time_signal = time_signal + "-";
  Serial.println(time_signal);
}


void loop() {
  if ((digitalRead(buttonPin) == 0)) { //khi nut duoc nhan
    delay(20); // nghi 20 mili giay de chong nhieu
    while ((digitalRead(buttonPin) == 0)) {
      tick = tick + 1; // dem thoi gian tuong doi
      Serial.println(tick);
    }
  }
  if ((digitalRead(buttonPin) == 1)) {
    if (tick < 70) {
      tick = 0;
    }
    else if ((70 < tick) and (tick < 1000)) { //danh dau timestamp
      timeStore();
      tick = 0;
    }

    else {
      Serial.println("Long press");
      post_request(time_signal);//gui timestamp len server
      time_signal = "";
      tick = 0;
    }
  }

}
