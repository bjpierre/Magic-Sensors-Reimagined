#ifndef ESP32_CSI_CSI_COMPONENT_H
#define ESP32_CSI_CSI_COMPONENT_H

#include "time_component.h"
#include "math.h"
#include "../_components/uart_component.h"

char *project_type;

#define CSI_RAW 1
#define RSSI 0
#define CSI_AMPLITUDE 0
#define CSI_PHASE 0

#define CSI_TYPE CSI_RAW

void _wifi_csi_cb(void *ctx, wifi_csi_info_t *data) {
    wifi_csi_info_t d = data[0];
    //https://github.com/espressif/esp-idf/blob/9d0ca60398481a44861542638cfdc1949bb6f312/components/esp_wifi/include/esp_wifi_types.h#L314

    int8_t *my_ptr;
#if RSSI
	outprintf("[%d]\n", d.rx_ctrl.rssi);
#endif
#if CSI_RAW
    if(strcmp("AP", project_type) == 0){
        outprintf("AP Handling CSICB\n  ..  Not Analyzing\n");
    }else{

        char buffer[2048];

        //<---------This tells us we need to do some filtering--->
        //outprintf("Handling CSICB: %02X:%02X:%02X:%02X:%02X:%02X\n", data[0].mac);


        my_ptr = data->buf;
        

        int i =0;
        int index = 0;
        index += sprintf(&buffer[index], "[");
        for(i =0; i<105; i++){
            index += sprintf(&buffer[index], "%d,", my_ptr[i+12]);
        }
        index += sprintf(&buffer[index], "%d", my_ptr[105+12]);
        sprintf(&buffer[index],"]");

        //<------This prints our values to urat---->
        //uart_write_bytes(UART_NUM_2, (const char*)buffer, strlen(buffer));
        //<---------This allows our data to be seen on the conosole but it kills performance-------->
        outprintf(buffer);

        //<-----This is good for debugging---->
        // char* test_str = "This is a test string.\n";
        // uart_write_bytes(UART_NUM_2, (const char*)test_str, strlen(test_str));
        // outprintf(test_str);

        //<-----This is here incase we need it later---->
        //start at 12(6*2) as the first 5 subcarries are useless <i>tm</i>
        //outprintf("%d,[%d", data->len, my_ptr[0+12]);
        // snprintf(buffer, sizeof(buffer), "[%d", my_ptr[0+12]);
        // uart_write_bytes(UART_NUM_2, (const char*)buffer, strlen(buffer));
        // //start at 11 as we printed 10, end at 118(128-(5*2)) as the last 5 subarriers are also useless in our setup
        // for (int i = 0+13; i < 128-10; i++) {
        //     //outprintf(",%d", my_ptr[i]);
        //     snprintf(buffer, sizeof(buffer),",%d", my_ptr[i]);
        //     uart_write_bytes(UART_NUM_2, (const char*)buffer, strlen(buffer));
        // }
        // snprintf(buffer, sizeof(buffer),"]\n");

        //fflush(stdout);
    }
    
#endif
#if CSI_AMPLITUDE
     outprintf("%d,[", data->len);
     my_ptr = data->buf;

     for (int i = 0; i < 64; i++) {
         outprintf("%.4f ", sqrt(pow(my_ptr[i * 2], 2) + pow(my_ptr[(i * 2) + 1], 2)));
     }
     outprintf("]\n\n");
#endif
#if CSI_PHASE
     //outprintf("%d,[", data->len);
     my_ptr = data->buf;

     for (int i = 0; i < 64; i++) {
                 outprintf("%.4f, ", atan2(my_ptr[i*2], my_ptr[(i*2)+1]));
             }
     //outprintf("]\n\n");
#endif
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
