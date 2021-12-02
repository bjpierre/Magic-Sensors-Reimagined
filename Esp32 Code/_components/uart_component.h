#ifndef ESP32_CSI_UART_COMPONENT_H
#define ESP32_CSI_UART_COMPONENT_H

#define UART_NUM_2             (2) /*!< UART port 2 */



#include "../driver/uart.h"

void UART_init(){
    //const int uart_num = UART_NUM_2;
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS, //byte by byte
        .parity = UART_PARITY_DISABLE, //not important enough for parity with the rolling average
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    };
    const int uart_buffer_size = (2048);
    QueueHandle_t uart_queue;
    ESP_ERROR_CHECK(uart_param_config(UART_NUM_2, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART_NUM_2, 16, 17, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));
    ESP_ERROR_CHECK(uart_driver_install(UART_NUM_2, uart_buffer_size, 0, 10, &uart_queue,0));
}

#endif