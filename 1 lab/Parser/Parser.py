import csv
import math

data = {'outCalls': [], 'inCalls': [], 'sms': []}  # Array for storing incoming, outgoing calls and the number of SMS

def csv_dict_reader(file_obj,ph_number): #Function for parsing a csv - file and filling the array with data
    reader = csv.DictReader(file_obj, delimiter=',')

    for line in reader:
        if line['msisdn_origin'] == ph_number:
            data['outCalls'].append(line['call_duration'])
            data['sms'].append(line['sms_number'])
        if line['msisdn_dest'] == ph_number:
            data['inCalls'].append(line['call_duration'])

def billing(data): # Payment calculation
    price = 0
    call_duration_out_num = 0
    for call_duration_out in data['outCalls']:
        call_duration_out_num+= float(call_duration_out)
    if call_duration_out_num > 20:
        call_duration_out_num-= 20
    price+=int(math.ceil(call_duration_out_num*2)) #Rounding up

    for call_duration_in in data['inCalls']:
        price += int(float(call_duration_in))*0

    for sms_number in data['sms']:
        price+=int(float(sms_number))*2

    return price


with open("data.csv") as f_obj:
        ph_number = input("Enter phone number: ")
        csv_dict_reader(f_obj, ph_number)

        print('Price = ', billing(data))


