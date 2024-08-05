# esp 32

## Notes

- to access esp32 from terminal use ```bash sudo picocom /dev/ttyUSB0 -b 115000``` and ctrl - c twice.
- to change access rights for esp32 ```bash udo chmod a+rw /dev/ttyUSB0 ```

#### simple mosquitto 
- 'mosquitto_pub -h 192.168.8.2 -t heat_storage -m relay_6_on' - publish messages
- 'mosquitto_sub -h 192.168.8.2 -t heat_storage' - subscribe to topic  