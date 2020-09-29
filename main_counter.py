from gpiozero import LED, LightSensor
from time import sleep
from signal import pause
import paho.mqtt.client as mqtt
import socket

broker_ip = "192.168.178.56"
ldr = LightSensor(4)

own_name = socket.gethostname() # get hostname as ID for publishing

def get_entrance_topic(this_device):
    if this_device is "entrance":
        return "entrance/"+own_name+"/people"
    else:
        return "entrance/+/people"
def get_exit_topic(this_device):
    if this_device is "exit":
        return "exit/"+own_name+"/people"
    else:
        return "exit/+/people"

entrance_topic = "entrance/+/people"
exit_topic = "entrance/+/people"

def on_msg_entered(client, userdata, message):
    # do what needs to be done if a person enters the venue
    #venue.person_entered()
    return 0 #just a space holder
def on_msg_left(client, userdata, message):
    # do what needs to be done if a person leaves the venue
    #venue.person_left()
    return 0 # just a space holder


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

client = mqtt.Client(client_id=own_name, clean_session=False)
client.conected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.message_callback_add(entrance_topic, on_msg_entered())
client.message_callback_add(exit_topic, on_msg_left())

client.connect(host=broker_ip)
while not client.connected_flag: #wait in loop
    print("waiting for connection ...")
    sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()

client.subscribe(topic=exit_topic)

client.loop_start()

interrupt = False
count = 0

space = True

class Venue:
    def __init__(self, capacity, entrance_topic, exit_topic, space=True):
        self.capacity = capacity
        self.entrance_topic = entrance_topic
        self.exit_topic = exit_topic
        self.space = space
        self.count = 0
    def person_entered(self):
        self.count += 1

    def person_left(self):
        self.count -= 1

    def get_count(self):
        return self.count

HalleBilfingen = Venue(capacity=60)



while space:
    print("Noch ", 60-count, "Plätze frei")
    if count =< 60:
        while interrupt is False:
            if ldr.value < 0.1:
                HalleBilfingen.person_entered()
                client.publish(entrance_topic, HalleBilfinge.count)
                interrupt = True
        while interrupt is True:
            if ldr.value > 0.1:
                interrupt = False
    else:
        space = False
        print("Die Halle ist derzeit ausgelastet")
while not space:

sleep(5)
client.loop_stop()
pause()
