from Venue import Venue
import client_functions as cf
own_name = "test"
Hall = Venue(capacity=30)

print(Hall.get_capacity())
print(cf.get_device_topic("entrance", own_name))
cf.on_msg_entered(1,1,1, Hall)
cf.on_msg_left(1,1,1, Hall)
