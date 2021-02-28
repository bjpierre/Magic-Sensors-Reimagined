/*
 *  This sketch demonstrates how to scan WiFi networks.
 *  This sketch also uses android OTA
 */
#include "WiFi.h"
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include "soc/rtc_cntl_reg.h"

#include "esp_wifi.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_event_loop.h"
#include "esp_log.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"
#include "freertos/event_groups.h"

#include "os.h"

const char* ssid = "The515";
const char* password ="Bluemoon696!";
int counter;



 
void setup()
{
    Serial.begin(115200);
 
    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    delay(100);

    bensOTABuilder();
    csiSetup();
  
    Serial.println("Setup done");
}

void csiSetup(){

  //https://github.com/jonathanmuller/ESP32-gather-channel-state-information-CSI-/blob/master/create_STA_and_AP/STA/main/scan.c

  Serial.println("Setting up CSI Handler");
  wifi_csi_config_t configuration_csi;
  configuration_csi.lltf_en = 1;
  configuration_csi.htltf_en = 1;
  configuration_csi.stbc_htltf2_en = 1;
  configuration_csi.ltf_merge_en = 1;
  configuration_csi.channel_filter_en = 1;
  configuration_csi.manu_scale = 0;

  esp_wifi_set_csi_config(&configuration_csi);
  esp_wifi_set_csi_rx_cb(&handleCSI, NULL);
}

void handleCSI(void *ctx, wifi_csi_info_t *data){
  Serial.println("Got CSI Packets");
  wifi_csi_info_t received = data[0];
  int8_t* my_ptr = received.buf;
  for(int i = 0; i < received.len; i++)
  {
      printf("%d ", my_ptr[i]);
  }
  
}

void bensOTABuilder(){
  ArduinoOTA.setHostname("CSIScanner1");
  ArduinoOTA
    .onStart([]() {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";

      // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
      Serial.println("Start updating " + type);
    })
    .onEnd([]() {
      Serial.println("\nEnd");
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });

  ArduinoOTA.begin();
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void scanWifi(){
  if(counter++>5000){
    counter = 0;
    Serial.println("Scanning Starting");
 
    // WiFi.scanNetworks will return the number of networks found
    int n = WiFi.scanNetworks();
    Serial.println("scan done");
    if (n == 0) {
        Serial.println("no networks found");
    } else {
        Serial.print(n);
        Serial.println(" networks found");
        for (int i = 0; i < n; ++i) {
            // Print SSID and RSSI for each network found
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(WiFi.SSID(i));
            Serial.print(" (");
            Serial.print(WiFi.RSSI(i));
            Serial.print(")");
            Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
            delay(10);
        }
    }
    Serial.println("");
  }
  
}
 
void loop()
{
    wifi_csi_info_t inty;
    ArduinoOTA.handle();
    scanWifi();
    delay(1);
}
