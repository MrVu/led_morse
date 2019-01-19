#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPUpdateServer.h>

//khai bao bien
const char* host = "esp8266-webupdate";
const char* update_path = "/firmware";
const char* update_username = "admin";
const char* update_password = "Vu1781991";
const char* ssid = "ahihi";
const char* password = "phongbui97";
#define buttonPin 5
#define LED 4
int tick = 0;
String clientName = "";

//Server http update
ESP8266WebServer httpServer(80);
ESP8266HTTPUpdateServer httpUpdater;


//Ham xuat tin hieu ra cong LED
void playLed(int first, int second) {
  for (int i = 0; i < first; i++) {
    analogWrite(LED, 1023);
    delay(200);
    analogWrite(LED, 0);
    delay(200);
  }
  delay(1000);
  for (int y = 0; y < second; y++) {
    analogWrite(LED, 1023);
    delay(200);
    analogWrite(LED, 0);
    delay(200);
  }
  delay(1000);
}

//Mac address to String
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

void charToSig(char character) {
  if (character == 'a') {
    playLed(1, 1);
  }
  else if (character == 'b') {
    playLed(1, 2);
  }
  else if (character == 'c') {
    playLed(1, 3);
  }
  else if (character == 'c') {
    playLed(1, 3);
  }
  else if (character == 'd') {
    playLed(1, 4);
  }
  else if (character == 'e') {
    playLed(1, 5);
  }
  else if (character == 'f') {
    playLed(2, 1);
  }
  else if (character == 'g') {
    playLed(2, 2);
  }
  else if (character == 'h') {
    playLed(2, 3);
  }
  else if (character == 'i') {
    playLed(2, 4);
  }
  else if (character == 'j') {
    playLed(2, 5);
  }
  else if (character == 'l') {
    playLed(3, 1);
  }
  else if (character == 'm') {
    playLed(3, 2);
  }
  else if (character == 'n') {
    playLed(3, 3);
  }
  else if (character == 'o') {
    playLed(3, 4);
  }
  else if (character == 'p') {
    playLed(3, 5);
  }
  else if (character == 'q') {
    playLed(4, 1);
  }
  else if (character == 'r') {
    playLed(4, 2);
  }
  else if (character == 's') {
    playLed(4, 3);
  }
  else if (character == 't') {
    playLed(4, 4);
  }
  else if (character == 'u') {
    playLed(4, 5);
  }
  else if (character == 'v') {
    playLed(5, 1);
  }
  else if (character == 'w') {
    playLed(5, 2);
  }
  else if (character == 'x') {
    playLed(5, 3);
  }
  else if (character == 'y') {
    playLed(5, 4);
  }
  else if (character == 'z') {
    playLed(5, 5);
  }
}


void setup () {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);

  //Get client Name
  clientName += "ESP8266-";
  uint8_t mac[6];
  WiFi.macAddress(mac);
  clientName += macToStr(mac);
  clientName += "-";
  clientName += String(micros() & 0xff, 16);
  Serial.println(clientName);

  //connect to wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.print("Connecting..");
  }

  // In địa chỉ IP
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  MDNS.begin(host);
  // Tạo server
  httpUpdater.setup(&httpServer, update_path, update_username, update_password);
  httpServer.begin();

  MDNS.addService("http", "tcp", 80);
  Serial.printf("HTTPUpdateServer ready! Open http://%s.local%s in your browser and login with username '%s' and password '%s'\n", host, update_path, update_username, update_password);
}


//Handling JSON type server response
void json_handle(String payload) {
  const size_t capacity = JSON_ARRAY_SIZE(0) + JSON_OBJECT_SIZE(1) + JSON_OBJECT_SIZE(2) + 40;
  DynamicJsonBuffer jsonBuffer(capacity);
  JsonObject& root = jsonBuffer.parseObject(payload);
  const char* none_data = root["data"];
  const char* data_word = root["data"]["word"];
  if (none_data == "none") {
    Serial.println("No more value");
  }
  else
  { Serial.println(data_word);
    Serial.println(strlen(data_word));
    for (int n = 0; n < strlen(data_word); n++) {
      Serial.println(data_word[n]);
      charToSig(data_word[n]);
    }
  }

}

void post_request() {
  String link = "http://35.236.172.46:5000/api_1_0/getdata/";
  link += clientName;
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
    HTTPClient http;    //Declare object of class HTTPClient

    http.begin(link);      //Specify request destination
    http.addHeader("Content-Type", "text/plain");  //Specify content-type header

    int httpCode = http.POST("Message from ESP8266");   //Send the request
    String payload = http.getString();                  //Get the response payload

    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

  } else {

    Serial.println("Error in WiFi connection");

  }
}


void send_request() {
  String link = "http://35.236.172.46:5000/api_1_0/getdata/"; //api link
  link += clientName;
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
    //String link = "http://35.236.172.46:5000/api_1_0/getdata/" + macToStr;

    HTTPClient http;  //Declare an object of class HTTPClient

    http.begin(link);  //Specify request destination
    int httpCode = http.GET();                                                                  //Send the request

    if (httpCode > 0) { //Check the returning code

      String payload = http.getString();   //Get the request response payload
      Serial.println(payload);                     //Print the response payload
      json_handle(payload);

    }

    http.end();   //Close connection

  }
}


void loop() {
  httpServer.handleClient();

  if ((digitalRead(buttonPin) == 0)) {
    //chong rung bang delay 20ms
    delay(20);
    while ((digitalRead(buttonPin) == 0)) {
      tick = tick + 1;
      Serial.println(tick);

    }


  }
  if ((digitalRead(buttonPin) == 1)) {
    if (tick < 10) {
      tick = 0;
    }
    else if ((10 < tick) and (tick < 500)) {
      send_request();
      tick = 0;
    }

    else {
      post_request();
      send_request();
      tick = 0;
    }
  }

}
