#define RXD2 16
#define TXD2 17

#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include "time.h"

#define isDebug false

//WIFI info - secretize
const char* ssid = "";
const char* password = "";

//NTP INFO
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -21600;
const int   daylightOffset_sec = 3600;




//TODO Clean this up heavily
const char* ProdServerHostName = "http://sddec21-09.ece.iastate.edu:20002/debug/post/echo";
const char* ProdServerGETHostName = "http://sddec21-09.ece.iastate.edu:20002/debug/get/version/server";
const char* DebugServerHostName = "https://postman-echo.com/post";
String apiKey = "0CG0I76JOZLIZ7JB";

WiFiClient client;
HTTPClient http;

char server[512] = "";
String strBuilder = "";
String strStorer = "";
WiFiMulti wifiMulti;

void setup() {
  if(isDebug){
    strcpy(server,DebugServerHostName);
  }else{
    strcpy(server,ProdServerHostName);
  }
  Serial.begin(115200);
  Serial.println("**SETUP**");
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
  Serial.printf("Serial2 Txd is on pin: %s, Rxd is on pin %s \n", String(TXD2), String(RXD2));
  Serial.printf("Connecting to %s", String(ssid));
  wifiMulti.addAP(ssid, password);
  while ((wifiMulti.run() != WL_CONNECTED)) {
    delay(50);
    Serial.print(".");
  }
  Serial.print("WiFi connected : ");
  Serial.print(WiFi.localIP());
  Serial.println();
  Serial.println(WiFi.macAddress());
  
  delay(100);
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.print("Got time as : ");
  printLocalTime();
  Serial.printf("\nServer: %s \n", server);
  getTest();
  //printLocalTime();
  Serial.println("**END SETUP**");
}

void loop() { //Choose Serial1 or Serial2 as required'
  while (Serial2.available()) {
    char val = char(Serial2.read());   
    strBuilder += val;
    if(val == ']'){
      strStorer = String(strBuilder);
      //xTaskCreate(
      //  uploadToServer,
      //  "Post Data",
      //  10000,
      //  (void*)&strStorer,
      //  1,
      //  NULL       
      //);
      uploadToServer((void*)&strStorer);
      strBuilder="";
    }
  }
}

void uploadToServer(void * postData){
    http.begin(client, server);
    http.addHeader("Content-Type", "application/json");
    String httpRequestData = "{\"payload\":\"" + *((String*)postData) + "\"}"; 
    int httpCode = http.POST(httpRequestData);
    Serial.print(httpCode);
    if(httpCode<0){
      Serial.print(':');
      Serial.print(http.errorToString(httpCode));
    }
    Serial.println();
    http.end();
    //vTaskDelete(NULL);
}

void getTest(){
  if((wifiMulti.run() == WL_CONNECTED)) {
        HTTPClient http;
        http.begin(ProdServerGETHostName);
        printLocalTime();
        int httpCode = http.GET();
        if(httpCode > 0) {
            Serial.printf("[HTTP] GET... code: %d ... Content(if Exists):", httpCode);
            if(httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                Serial.println(payload);
            }
        } else {
            Serial.printf("[HTTP] GET... failed, error: %s \n", http.errorToString(httpCode).c_str());
        }
        http.end();
    }
}

void printLocalTime()
{
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.print(&timeinfo, "%Y-%b-%d-%H:%M:%S");
}
