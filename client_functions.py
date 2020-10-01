def get_device_topic(this_device, id):
    if this_device is "entrance":
        return "entrance/"+id+"/people"
    elif this_device is "exit":
        return "exit/"+id+"/people"
