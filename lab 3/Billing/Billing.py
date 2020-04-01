import docx
from docxtpl import DocxTemplate
import sys
import os
import csv
import math


data_traff = {'out': [], 'in': []}  # Array for storing incoming, outgoing traffic

data = {'outCalls': [], 'inCalls': [], 'sms': []}  # Array for storing incoming, outgoing calls and the number of SMS

number = ["ноль","один","два","три","четыре","пять","шесть","семь","восемь","девять"]
teen = ["десять","одиннадцать","двенадцать","тринадцать","четырнадцать","пятнадцать","шестнадцать","семнадцать","восемнадцать","девятнадцать"]
decades =["двадцать","дридцать","сорок","пятьдесят","шестьдесят","семьдесят","восемьдесят","девяносто"]

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
        price+=round(math.ceil(call_duration_out_num*2*100)/100, 2)

    for call_duration_in in data['inCalls']:
        price += (float(call_duration_in))*0

    for sms_number in data['sms']:
        price+=round(float(sms_number)*2, 2)

    return price

def csv_dict_reader_traff(file_obj,ip): #Function for parsing a csv - file and filling the array with data
    reader = csv.DictReader(file_obj, delimiter=',')

    for line in reader:
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
    price+=round(math.ceil(traf_Mb*100)/100, 2)*1 #  - 1 rub / Mb
    return price

def num_to_str(Sum):
    if Sum <= 9:
       return number[Sum]
    elif Sum >= 10 and Sum <= 19:
        tens = Sum % 10
        return(teen[tens])
    elif Sum > 19 and Sum <= 99:
        ones = math.floor(Sum / 10)
        twos = ones - 2
        tens = Sum % 10
        if tens == 0:
            return decades[twos]
        elif tens != 0:
            return decades[twos] + " " + number[tens]


with open("file.csv") as f_obj:
    with open("data.csv") as f_obj_phone:
        ph_number = input("Enter phone number: ")
        ip = input("Enter ip: ")
        csv_dict_reader(f_obj_phone, ph_number)
        csv_dict_reader_traff(f_obj, ip)
        Price_tr = traffic(data_traff)
        Price_ph = billing(data)
        print('Price_tr = ', Price_tr )
        print('Price_ph = ', Price_ph)
        Sum = Price_tr+Price_ph;
        Sum = round(math.ceil(Sum * 100) / 100, 2)

        arr = math.modf(Sum)
        f_part =  str(num_to_str(int(arr[1]))) + " руб. "
        sec_part = str(num_to_str(int(round(arr[0],2)*100) )) + " коп."


doc = DocxTemplate("template.docx") #Get the template

context = {
'product' : 'Услуги Сотовой связи',
'qty' : '1',
'price' : Price_ph,
'sum' : Price_ph,
'product1' : 'Оплата Интернет',
'qty1' : '1',
'price1' : Price_tr,
'sum1' : Price_tr,
'fin_sum' : Sum,
'fin_nds' : round(Sum*20/120,2),
'fin_sum_n' : Sum,
'rows' : '2',
'ed' : 'шт',
'string_sum' : f_part + sec_part,
'bank' : 'ПАО Сбербанк (ИНН 7707083893, ОГРН 1027700132195)',
'inn' : '1234567890',
'kpp': '0987654321',
'supp': 'ООО Моя Фирма - Supplier',
'buyer': 'ООО Фирма-Buyer',
'director': 'Анастасия Алексеевна',
'bik': '12345',
'account': '12345432123563511',
'account2': '02345432123563511',
'doc_num': '5',
'data': '31 марта 2020',
'base': 'Коммерческое предложение № 5',
'accountant': 'Главный бухгалтер Анастасия Алексеевна'
}
doc.render(context) # Rendering doc - file
doc.save("final.docx") # Save doc - file


myCmd = 'libreoffice --convert-to pdf final.docx'
os.system (myCmd)
