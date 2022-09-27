import time
import db
import schedule
import threading
import datetime
from schedule import every, repeat, run_pending

import publisher
import subscriber_accept_client as sub_accept_client
import subscriber_send_db as sub_db
import subscriber_send_data as sub_send_data
import subscriber_delete as sub_del

queue = []
thread_queue = []
alive_thread = []
inserting_db = []
delete = []
is_calling = [0]
temp_global = []
db2send = []

TEMPO = 3

def t():
    while True:
        run_pending()
        time.sleep(1)

th = threading.Thread(target = t)
th.start()

@repeat(every(1).seconds)
def job():
    global TEMPO
    removes = []
    for i in queue:
        if(type(i[1]) == type(datetime.datetime.now())):
            if((datetime.datetime.now() - i[1]).total_seconds() > TEMPO):
                removes.append(i)

    for j in removes:
        queue.remove(j)

    if(len(thread_queue) != 0 and len(alive_thread) == 0):
        print('inicar nova thread')
        th = thread_queue.pop(0)
        th.start()
        alive_thread.append(th)

def client_publish(comando):
    is_calling[0] = 1

    print(comando,'1')
    publisher.run('client',comando)
    
    queue.append(comando)
    print('2')
    sub_accept_client.run('accept')
    print('3')
    data = sub_accept_client.response.pop(0)
    print('4')
    publisher.run('ackn','ackn')
    print('5')
    is_calling[0] = 0

def admin_publish(comando):
    print('entrou----------------------------')
    is_calling[0] = 1
    
    publisher.run('admin',comando)
    
    sub_send_data.run('send_data')
    
    data = sub_send_data.response.pop(0)

    parsed_data = data[1:-2].replace(" '",'')
    parsed_data = parsed_data.replace("'","").split(',')
    
    inserting_db.append((int(parsed_data[0]),int(parsed_data[1]),parsed_data[2],parsed_data[3],parsed_data[4]))
    
    publisher.run('admin_ack','admin_ack')
    is_calling[0] = 0

def on_signal(signal,c_a):
    print(signal)
    if(c_a == 'a'):
        print('admin')
        admin_publish(signal)
    else:
        print('client',signal)
        client_publish(signal)
    
    alive_thread.pop(0)

def rasp_sender(signal):
    #command = db.getCode(signal)--------------------------------------------------------------------------------------
    print(f'signal --------{signal}-{type(signal)}-{command}')
    if(command == ''):
        print('a')
        c_a = 'a'
    else:
        print('c')
        c_a = 'c'
        
    th = threading.Thread(target = on_signal,args=(signal,c_a))
    thread_queue.append(th)

def pulse_verification(pulse):
    for i in queue:
        if(i[0] == pulse):
            print(pulse)
            return

    queue.append((pulse,datetime.datetime.now()))
    temp_global.append(pulse)
    #rasp_sender(pulse)---------------------------------------------------------------------------------------------------

def del_thread():
    sub_del.run('delete')
    print('delete recebido iniciando a deleção')

    data_to_del = sub_del.response.pop(0)
    
    print('data_to_del',data_to_del)

    delete.append(data_to_del)
    th_del = threading.Thread(target = del_thread())
    th_del.start()

def send_db():
    sub_db.run('send_db')
    print('testando send_db---------------****************-------------------****************')
    print('testando send_db---------------****************-------------------****************')
    if(len(sub_db.response) > 0):
        trash = sub_db.response.pop(0)

    db2send.append(1)
    th = threading.Thread(target = send_db)
    th.start()

thread_del = threading.Thread(target = del_thread)
thread_del.start()

thread_send_db = threading.Thread(target = send_db)
thread_send_db.start()

def input_loop():
    while True:
        pulse_verification(input())

thread_del = threading.Thread(target = input_loop).start()

while True:
    if(len(temp_global) != 0):
        signal = temp_global.pop(0)
        print('signal on while true',signal)
        command = db.getCode(signal)
        if(command == ''):
            print('a')
            c_a = 'a'
        else:
            print('c')
            c_a = 'c'
            
        th = threading.Thread(target = on_signal,args=(signal,c_a))
        thread_queue.append(th)
    if(len(inserting_db) != 0):
        db.insertCode(inserting_db[0])
        inserting_db.pop(0)
    if(len(delete) != 0):
        print(f'deleting {delete[0]}')
        db.deleteCode(delete[0])
        delete.pop(0)
    if(len(db2send) != 0):
        print('sending')
        db2send.pop(0)
        publisher.run('server_send_db',db.get_all())
    time.sleep(1)

'''
import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))
while True:
    if(len(temp_global) != 0):
        signal = temp_global.pop(0)
        command = db.getCode(signal)
        if(command == ''):
            print('a')
            c_a = 'a'
        else:
            print('c')
            c_a = 'c'
            
        th = threading.Thread(target = on_signal,args=(signal,c_a))
        thread_queue.append(th)
    if(len(inserting_db) != 0):
        db.insertCode(inserting_db[0])
        inserting_db.pop(0)
    if(len(delete) != 0):
        print(f'deleting {delete[0]}')
        db.deleteCode(delete[0])
        delete.pop(0)
    if(len(db2send) != 0):
        print('sending')
        db2send.pop(0)
        publisher.run('server_send_db',db.get_all())
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        pulse_verification(str(rfdevice.rx_code))

    time.sleep(0.01)
rfdevice.cleanup()'''