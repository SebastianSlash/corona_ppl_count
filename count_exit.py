from gpiozero import LED, LightSensor
from time import sleep
from signal import pause
import paho.mqtt.client as mqtt
import socket
from client_functions import get_device_topic

# -----------------------------------------------------------------------------
# these should be set to fit the specific device constellation
broker_ip = "192.168.178.56"
ldr = LightSensor(4)
# -----------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag = True
        print("connected OK Returned code = ",rc)
    else:
        print("Bad connection Returned code = ",rc)
        client.bad_connection_flag = True

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
def on_publish(client, userdata, topic):
    print("value published succesfully to: "+topic)
def on_log(client, userdata, level, buf):
    print("log: ",buf)

topic = get_device_topic("exit") # topic for device at exit

client = mqtt.Client(client_id=socket.gethostname(), clean_session=False)
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.connect(host=broker_ip)
client.loop_start()
while not client.connected_flag: #wait in loop
    print("waiting for connection ...")
    sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()

interrupt = False
while True:
    while interrupt is False:
        if ldr.value < 0.1:
            client.publish(topic, 1)
            interrupt = True
    while interrupt is True:
        if ldr.value > 0.1:
            interrupt = False

sleep(5)
client.loop_stop()
pause()
