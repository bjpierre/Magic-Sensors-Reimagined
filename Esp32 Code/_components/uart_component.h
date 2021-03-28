#ifndef ESP32_CSI_UART_COMPONENT_H
#define ESP32_CSI_UART_COMPONENT_H

#define UART_NUM_2             (2) /*!< UART port 2 */



#include "../driver/uart.h"

void UART_config(){
    //const int uart_num = UART_NUM_2;
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS, //byte by byte
        .parity = UART_PARITY_DISABLE, //not important enough for parity with the rolling average
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_CTS_RTS,
        .rx_flow_ctrl_thresh = 122,
    };
    ESP_ERROR_CHECK(uart_param_config(2, &uart_config));
}

#endif