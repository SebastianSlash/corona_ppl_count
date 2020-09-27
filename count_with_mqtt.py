from gpiozero import LED, LightSensor
from time import sleep
from signal import pause
import paho.mqtt.client as mqtt

broker_ip = "192.168.178.56"
id_pi = "pi_01"
ldr = LightSensor(4)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
def on_message(client, userdata, topic):
    print(msg.topic+" "+str(msg.payload))
def on_publish(client, userdata, msg):
    print("value published succesfully to: "+topic)
client = mqtt.Client(client_id=id_pi, clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.connect(host=broker_ip)
client.loop_start()

interrupt = False
count = 0

while True:
    print("Besucher: ", count)
    while interrupt is False:
        if ldr.value < 0.1:
            count += 1
            client.publish("entrance/"+id_pi+"/people", count)
            interrupt = True
    while interrupt is True:
        if ldr.value > 0.1:
            interrupt = False

client.loop_stop()
pause()
