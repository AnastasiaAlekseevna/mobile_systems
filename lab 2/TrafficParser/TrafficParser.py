import csv
import math

data_traff = {'out': [], 'in': []}  # Array for storing incoming, outgoing traffic

def csv_dict_reader_traff(file_obj,ip): #Function for parsing a csv - file and filling the array with data
    reader = csv.DictReader(file_obj, delimiter=',')

    for line in reader:
        #print(line)
        if line['da'] == ip:
           data_traff['in'].append(line['ibyt'])
        if line['sa'] == ip:
            data_traff['out'].append(line['obyt'])

def traffic(data): # Payment calculation
    price = 0
    traf_Mb = 0
    sum_traf = 0

    for traf_out in data['out']:
        sum_traf+= float(traf_out)
    for traf_in in data['in']:
        sum_traf += float(traf_in)
    traf_Mb = sum_traf / (2**20) # From bytes to Mb

    print('sum_traf = ' , sum_traf )
    print('traf_Mb = ' , traf_Mb )


    price+=round(math.ceil(traf_Mb*100)/100, 2)*1 #  - 1 rub / Mb
    return price


with open("file.csv") as f_obj:
        ip = input("Enter ip: ")
        csv_dict_reader_traff(f_obj, ip)
        print('Price = ', traffic(data_traff))


