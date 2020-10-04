from csv import writer
import os
from datetime import datetime
import socket

def get_device_topic(this_device):
    id = socket.gethostname() # get hostname as ID for publishing
    if this_device is "entrance":
        return "entrance/"+id+"/people"
    elif this_device is "exit":
        return "exit/"+id+"/people"

def append_list_as_row(file_name, list_of_elem): # appends list as row to csv
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def create_statistic_file(): # creates csv file for saving statistics
    if not os.path.exists('statistics/'):
        os.mkdir('statistics')
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    new_csv = 'statistics/'+dt_string+'.csv'
    header = ['time', 'visitors', 'in/out'] # 1 = in, 0 = out
    with open(new_csv, 'w', newline='') as csvfile:
        csv_writer = writer(csvfile)
        csv_writer.writerow(header)
    # return name of created file
    return new_csv
