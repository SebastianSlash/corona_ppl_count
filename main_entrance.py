from gpiozero import LED, LightSensor
from time import sleep
from signal import pause
import paho.mqtt.client as mqtt
import socket
from Venue import Venue
from client_functions import get_device_topic

def on_msg_entered(client, userdata, message, venue):
    print("one person has entered the venue")
    venue.person_entered()
    venue.print_cur_visitors()
    if venue.get_count() >= venue.get_capacity():
        venue.is_full()
    print("visitor count is:  ", venue.get_count())
    print("venue capacity is: ", venue.get_capacity())
    print("venue still has space: ", venue.get_space())
def on_msg_left(client, userdata, message, venue):
    print("one person has left the venue")
    if venue.get_count() == venue.get_capacity():
        venue.not_full()
    venue.person_left()
    venue.print_cur_visitors()
    print("visitor count is:  ", venue.get_count())
    print("venue capacity is: ", venue.get_capacity())
    print("venue still has space: ", venue.get_space())

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag = True
        print("connected OK Returned code = ",rc)
    else:
        print("Bad connection Returned code = ",rc)
        client.bad_connection_flag = True

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload)+"person entered")
def on_publish(client, userdata, topic):
    print("value published succesfully to: "+topic)
def on_log(client, userdata, level, buf):
    print("log: ",buf)

ldr = LightSensor(4)
led = LED(2)
Hall = Venue(capacity=10) # create venue object and set venue capacity
broker_ip = "192.168.178.56"
own_name = socket.gethostname() # get hostname as ID for publishing
entrance_topic = "entrance/+/people" # wildcard for all devices publishing in entrance
exit_topic = "exit/+/people" # wildcard for all devices publishing in exit
topic = get_device_topic("entrance") # set topic of this pi



client = mqtt.Client(client_id=own_name, clean_session=False)
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.message_callback_add(entrance_topic, on_msg_entered)
client.message_callback_add(exit_topic, on_msg_left)

client.connect(host=broker_ip)
client.loop_start()
client.subscribe(topic=entrance_topic)
client.subscribe(topic=exit_topic)
while not client.connected_flag: #wait in loop
    print("waiting for connection ...")
    sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()

led.off()
interrupt = False

while True:
    print("Besucher: ", Hall.get_count())
    led.off()
    while interrupt is False:
        if ldr.value < 0.1:
            client.publish(topic, 1)
            interrupt = True

    while interrupt is True:
        if ldr.value > 0.1:
            interrupt = False

    begin_full = True
    while not Hall.get_space(): # if capacity is full people entering will not be count
        if begin_full:
            print("Die Halle ist derzeit voll.")
            print("Bitte haben sie Geduld.")
            led.on()
            begin_full = False

sleep(5)
client.loop_stop()
pause()
