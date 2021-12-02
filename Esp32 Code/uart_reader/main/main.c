#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "freertos/event_groups.h"
#include "esp_wifi.h"
#include "nvs_flash.h"

#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include "lwip/netdb.h"
#include "lwip/dns.h"

#include "../../_components/nvs_component.h"
#include "../../_components/uart_component.h"
#include "../../_components/sd_component.h"

static const int BUFF_SIZE = 2048;

#define SSID CONFIG_ESP_WIFI_SSID//replace this with your own info
#define PASSWORD CONFIG_ESP_WIFI_PASSWORD
#define SERVER "http://http://sddec21-09.ece.iastate.edu/"
#define PORT "80"
#define PATH "/RyanIMY"

static EventGroupHandle_t s_wifi_event_group;
const int WIFI_CONNECTED_BIT = BIT0;

static esp_err_t event_handler(void *ctx, system_event_t *event) {
    switch (event->event_id) {
        case SYSTEM_EVENT_STA_START:
            esp_wifi_connect();
            break;
        case SYSTEM_EVENT_STA_GOT_IP:
            outprintf("Got ip:%s\n", ip4addr_ntoa((const ip4_addr_t *) &event->event_info.got_ip.ip_info.ip));
            xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
            break;
        case SYSTEM_EVENT_STA_DISCONNECTED: {
            outprintf("connect to the AP fail\n");
            break;
        }
        default:
            break;
    }
    return ESP_OK;
}

void wifi_init(void){
    s_wifi_event_group = xEventGroupCreate();
    tcpip_adapter_init();
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_event_loop_init(event_handler, NULL));
    wifi_config_t wifi_config = {
            .sta = {
                    .ssid = SSID,
                    .password = PASSWORD,
            },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    esp_wifi_set_ps(WIFI_PS_NONE);

    outprintf("Wifi has not died thus far");

}

void http_post(void){
    const struct addrinfo hints = {
        .ai_family = AF_INET,
        .ai_socktype = SOCK_STREAM,
    };
    struct addrinfo *res;
    struct in_addr *addr;
    int s, r;
    int err = getaddrinfo(SERVER, PORT, &hints, &res);
    if(err != 0 || res == NULL) {
        ESP_LOGE("WIFI LOGGING", "DNS lookup failed err=%d res=%p", err, res);
    }else{
        outprintf("Time to go postal\n");
    }
}

bool is_wifi_connected() {
    return (xEventGroupGetBits(s_wifi_event_group) & WIFI_CONNECTED_BIT);
}

void app_main() {
    nvs_init();
    ESP_ERROR_CHECK(esp_netif_init());
    wifi_init();
    sd_init();
    UART_init();


    //Realistically this should all be in a job but that's mildy over my head right now
    char JavaDoesStringsBetter[BUFF_SIZE];
    char LowLevelLanguages = 'a';
    char buffer[1];
    int index = 0;
    outprintf("Waiting for task!\n");
    while(true){
        if(uart_read_bytes(UART_NUM_2, (unsigned char*)buffer, sizeof(LowLevelLanguages), 1000) > 0){
            index += sprintf(&JavaDoesStringsBetter[index], "%c", buffer[0]);
            if(buffer[0] == ']'){
                JavaDoesStringsBetter[index+1] = '\n';
                if(is_wifi_connected()){
                    http_post();
                }
                //outprintf(JavaDoesStringsBetter);
                //outprintf("\n");
                index = 0;
            }
        }else{
            outprintf("No Data Read In 1000 Ticks\n");
        }
    }
}