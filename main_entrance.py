from gpiozero import LED, LightSensor
from time import sleep, strftime, localtime
from signal import pause
import paho.mqtt.client as mqtt
import socket
from Venue import Venue
from client_functions import get_device_topic, append_list_as_row, create_statistic_file

# -----------------------------------------------------------------------------
# these should be set to fit the specific device constellation
broker_ip = "192.168.178.56"
Hall = Venue(capacity=10) # create venue object and set venue capacity
ldr = LightSensor(4)
signal_red = LED(17)
signal_green = LED(18)
# -----------------------------------------------------------------------------

def on_msg_statistic(cleint, userdata, message):
    current_time = strftime("%H:%M:%S", localtime())
    row_contents = [current_time, Hall.get_count(), str(message.payload.decode('utf-8'))]
    append_list_as_row(statistic_file, row_contents)

def on_msg_entered(client, userdata, message):
    print("one person has entered the venue")
    Hall.person_entered()
    Hall.print_cur_visitors()
    if Hall.get_count() >= Hall.get_capacity():
        Hall.is_full()
    print("visitor count is:  ", Hall.get_count())
    print("venue capacity is: ", Hall.get_capacity())
    print("venue still has space: ", Hall.get_space())
    client.publish(topic_visitors, Hall.get_count())
    client.publish(topic_statistic, 1)
def on_msg_left(client, userdata, message):
    print("one person has left the venue")
    if Hall.get_count() == Hall.get_capacity():
        Hall.not_full()
    Hall.person_left()
    Hall.print_cur_visitors()
    print("visitor count is:  ", Hall.get_count())
    print("venue capacity is: ", Hall.get_capacity())
    print("venue still has space: ", Hall.get_space())
    client.publish(topic_visitors, Hall.get_count())
    client.publish(topic_statistic, 0)

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


statistic_file = create_statistic_file() # creates file to save statistics
entrance_topic = "entrance/+/people" # wildcard for all devices publishing in entrance
exit_topic = "exit/+/people" # wildcard for all devices publishing in exit
topic = get_device_topic("entrance") # <== set topic of this pi 
topic_visitors = "metrics/visitors" # topic for live update of visitor count
topic_statistic = "metrics/statistic" # topic to save statistics

client = mqtt.Client(client_id=socket.gethostname(), clean_session=False)
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.message_callback_add(entrance_topic, on_msg_entered)
client.message_callback_add(exit_topic, on_msg_left)
client.message_callback_add(topic_statistic, on_msg_statistic)

client.connect(host=broker_ip)
client.loop_start()
client.subscribe(topic=entrance_topic)
client.subscribe(topic=exit_topic)
client.subscribe(topic=topic_statistic)
while not client.connected_flag: #wait in loop
    print("waiting for connection ...")
    sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()

signal_red.off()
signal_green.on()

client.publish(topic_statistic, 0)
client.publish(topic_visitors, Hall.get_count())

interrupt = False
while True:
    print("Besucher: ", Hall.get_count())
    signal_red.off()
    signal_green.on()
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
            signal_green.off()
            signal_red.on()
            begin_full = False

sleep(5)
client.loop_stop()
pause()
