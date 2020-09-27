# corona_ppl_count
Counting people entering a venue and controlling a traffic light to limit the entrance. Controlled with a Raspberry Pi

Things to install on the Raspberry Pi (Any version will work):

  - Raspbian Lite
  - gpiozero:
    - `sudo apt update`
    - `sudo apt install python3-gpiozero`
  - Mosquitto client:
    - `sudo apt-get install mosquitto-clients`
  - Mosquitto MQTT server (only on the Raspberry pi to handle the Server):
    - `sudo apt-get install mosquitto`
  - pip for python 3:
    - `sudo apt-get install python3-pip`
  - paho mqtt:
    - `sudo pip3 install paho-mqtt`
