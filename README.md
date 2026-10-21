
# Magic Sensors Reimagined

A senior design capstone project exploring contactless door-state detection using Wi-Fi Channel State Information (CSI) and ESP32 microcontrollers.

## Overview

The project used multiple ESP32 devices to analyze Channel State Information (CSI) from Wi-Fi signals traveling between devices. By monitoring changes in the wireless channel, the system aimed to detect changes in a door's state without requiring a physical contact sensor.

## How It Works

- **Signal Collection:** ESP32 devices transmit and receive Wi-Fi signals while collecting CSI measurements.
- **Channel Analysis:** CSI data is analyzed to identify changes in signal propagation caused by movement in the environment.
- **Door-State Detection:** Changes in the wireless channel are used to determine whether a door's state has changed.

## Project Context

Developed as a senior design capstone project, this work explored the use of wireless sensing as an alternative to traditional physical sensors for monitoring environmental changes.



## References

- [ESP32 CSI Tool](https://stevenmhernandez.github.io/ESP32-CSI-Tool/) — Toolkit for collecting Channel State Information (CSI) from ESP32 devices for Wi-Fi sensing and localization.
- [ESP32 CSI Data Collection Example](https://github.com/jonathanmuller/ESP32-gather-channel-state-information-CSI-) — Example implementation for gathering Wi-Fi Channel State Information using ESP32 hardware.
- [Espressif ESP-IDF Wi-Fi Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html) — Official documentation for ESP32 Wi-Fi functionality, including CSI configuration and collection.
