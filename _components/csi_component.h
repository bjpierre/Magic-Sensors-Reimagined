#ifndef ESP32_CSI_CSI_COMPONENT_H
#define ESP32_CSI_CSI_COMPONENT_H

#include "time_component.h"
#include "math.h"
#include "../_components/uart_component.h"

char *project_type;

#define VERBOSITY 1 //0 = only to uart, 1 = drops mac to serial, 2 = drops mac and csi to serial, 3 = console, no uart
#define CSI_RAW 0
#define RSSI 0
#define CSI_AMPLITUDE 1
#define CSI_PHASE 0

#define CSI_TYPE CSI_RAW

void _wifi_csi_cb(void *ctx, wifi_csi_info_t *data) {
    wifi_csi_info_t d = data[0];
    //https://github.com/espressif/esp-idf/blob/9d0ca60398481a44861542638cfdc1949bb6f312/components/esp_wifi/include/esp_wifi_types.h#L314

    int8_t *my_ptr;

        my_ptr = data->buf;
        char buffer[2048];
        int index = 0;
        

        index += sprintf(&buffer[index], "[");
#if RSSI
index += sprintf(&buffer[index], "[%d]\n", d.rx_ctrl.rssi);
#endif

#if CSI_RAW
    if(strcmp("AP", project_type) == 0 && VERBOSITY >= 1){
        outprintf("AP Handling CSICB\n  ..  Not Analyzing\n");
    }else{
        //outprintf("Handling CSICB: %02X:%02X:%02X:%02X:%02X:%02X\n", data[0].mac);
        int i =0;

        for(i =0; i<105; i++){
            index += sprintf(&buffer[index], "%d,", my_ptr[i+12]);
        }
        index += sprintf(&buffer[index], "%d", my_ptr[105+12]);
        
    }
    
#endif
#if CSI_AMPLITUDE
     my_ptr = data->buf;

     for (int j = 6; j < 64; j++) {
         index += sprintf(&buffer[index],"%.4f ", sqrt(pow(my_ptr[j * 2], 2) + pow(my_ptr[(j * 2) + 1], 2)));
     }
#endif
#if CSI_PHASE
     for (int k = 6; k < 64; k++) {
        index += sprintf(&buffer[index],"%.4f, ", atan2(my_ptr[k*2], my_ptr[(k*2)+1]));
    }
#endif

    sprintf(&buffer[index],"]");
    if(VERBOSITY < 3) {
        uart_write_bytes(UART_NUM_2, (const char*)buffer, strlen(buffer));
    }
    if(VERBOSITY > 1){
        outprintf(buffer);
        outprintf(" \n ");
    }
    // outprintf("\n");
    sd_flush();
    vTaskDelay(0);
}

void _print_csi_csv_header() {
    char *header_str = "type,role,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,real_time_set,real_timestamp,len,CSI_DATA\n";
    outprintf(header_str);
}

void csi_init(char *type) {
    project_type = type;

#ifdef CONFIG_SHOULD_COLLECT_CSI
    outprintf("Start Status: %s\n", esp_err_to_name(esp_wifi_set_csi(1)));

    // @See: https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi_types.h#L401
    wifi_csi_config_t configuration_csi;
    configuration_csi.lltf_en = 1;
    configuration_csi.htltf_en = 1;
    configuration_csi.stbc_htltf2_en = 1;
    configuration_csi.ltf_merge_en = 1;
    configuration_csi.channel_filter_en = 0;
    configuration_csi.manu_scale = 0;

    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&configuration_csi));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(&_wifi_csi_cb, NULL));

    _print_csi_csv_header();
#endif
}

#endif //ESP32_CSI_CSI_COMPONENT_H
