import publisher
import time
import db
import subscriber as sub
import schedule
import threading
import datetime
from schedule import every, repeat, run_pending

thread_end = [0]
queue = []

def t():
    while not thread_end[0]:
        run_pending()
        time.sleep(1)

th = threading.Thread(target = t)
th.start()

@repeat(every(1).seconds)
def job():
    removes = []
    for i in queue:
        if((datetime.datetime.now() - i[1]).total_seconds() > 3):
            removes.append(i)
    for j in removes:
        queue.remove(j)

def client_publish(comando):
    publisher.run('client',comando)
    
    queue.append(comando)
    
    sub.run('accept')
    
    publisher.run('ack','ack')

def admin_publish(comando):
    publisher.run('admin',comando)

    data = sub.run('send_data')
    
    parsed_data = data[1:-2].replace("'",'').split(',')
    
    db.insertCode((str(parsed_data[0]),int(parsed_data[1]),str(parsed_data[2])))
    
    publisher.run('admin_ack','admin_ack')

def on_signal(signal,c_a):
    if(c_a == 'a'):
        print('admin')
        admin_publish(signal)
    else:
        print('client')
        client_publish(signal)

def rasp_sender(signal):
    command = db.getCode(signal)
    if(command == ''):
        print('a')
        c_a = 'a'
    else:
        print('c')
        c_a = 'c'
        
    th = threading.Thread(target = on_signal,args=(signal,c_a))

    th.start()

def pulse_verification(pulse):
    for i in queue:
        if(i[0] == pulse):
            print(pulse)
            return
    queue.append((pulse,datetime.datetime.now()))
    rasp_sender(pulse)

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
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        pulse_verification(str(rfdevice.rx_code))

    time.sleep(3)
rfdevice.cleanup()