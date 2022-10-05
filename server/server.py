import argparse
import signal
import sys
import time
import db
import schedule
import threading

import publisher
import subscriber_send_data as sub_send_data
import subscriber_inserting as sub_insert
import subscriber_send_db as sub_db
import subscriber_accept_client as sub_accept_client
import subscriber_delete as sub_del

TESTE = 1

if(not TESTE):
    from rpi_rf import RFDevice
    import logging

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


client_queue = []
admin_queue = []
inserting_db = []
deleting_db = []
pulsefnow = ['11112222','1','11112222','11112222','11112225','11112222','11112222','11112222','11112227','11112222','11112222']

#-------------------------listar fromdb-----------------------------------------#
def listar():
    sub_db.run('send_db')

threading.Thread(target = listar).start()

#-------------------------Delete fromdb-----------------------------------------#
def delete_db():
    sub_del.run('delete')
    
    if(len(sub_del.response) > 0):
        deleting_db.append(sub_del.response.pop(0))
    threading.Thread(target = delete_db).start()

threading.Thread(target = delete_db).start()

#-------------------------Admin Handler-----------------------------------------#
def most_frequent(List):
    return max(set(List), key = List.count)

def admin_handler():
    print('iniciando admin')
    sub_send_data.run('server_cad_newbutton')
    fill_cmd = []

    if(not TESTE):
        admin_timestamp = rfdevice.rx_code_timestamp
        t1 = time.time()
        while(admin_timestamp == rfdevice.rx_code_timestamp and time.time()-t1 < 60*5):
            time.sleep(0.01) 
        t1 = time.time()
        while(time.time() - t1 < 2):
            if rfdevice.rx_code_timestamp != admin_timestamp:
                admin_timestamp = rfdevice.rx_code_timestamp
                fill_cmd.append(rfdevice.rx_code)
                time.sleep(0.01)  
    else:
        fill_cmd = pulsefnow
             

    publisher.run('sub_press_btnsec',most_frequent(fill_cmd))
    fill_cmd = []
    threading.Thread(target = admin_handler).start()

threading.Thread(target = admin_handler).start()

def insertion_handler():
    print('insertion handler')
    sub_insert.run('send_data')
    
    data = sub_insert.response.pop(0)
    print('data',data)
    parsed_data = data[1:-2].replace(" '",'')
    parsed_data = parsed_data.replace("'","").split(',')
    print(type(parsed_data),parsed_data)
    
    inserting_db.append((parsed_data[0],parsed_data[1],parsed_data[2],parsed_data[3],parsed_data[4]))
    
    publisher.run('admin_ack','admin_ack')
    threading.Thread(target = insertion_handler).start()

threading.Thread(target = insertion_handler).start()

#-------------------------Client Handler-----------------------------------------#

def row_to_string(row):
    string_row = ''
    for i in row:
        string_row = string_row + str(i) + ","
    
    return string_row

def client_handler():
    while True:
        time.sleep(0.5)
        if(len(client_queue) != 0):
            print('enviando publicação para cliente')
            comando = row_to_string(client_queue[0])
            
            print('queue cliente',client_queue)
            print('comando',comando)
            
            sub_accept_client.run('accept','client',comando)
            data = sub_accept_client.response.pop(0)
        
            publisher.run('ackn',data)
            publisher.run('ackn2','data')
            client_queue.pop(0)

threading.Thread(target = client_handler).start() 
#-----------------------------Queue Handlers-------------------------------------#
#insere o pulso na fila caso ainda não esteja
def client_pulse_VerifyQueue(host,user,password,table,pulse):
    if(pulse not in client_queue):
        client_queue.append(db.get_row_byCode(host,user,password,table,pulse))

#---------------------------------------------------------------------------------#

def adminorclient(pulse):
    cmd = pulse
    if(cmd != ''):
        client_pulse_VerifyQueue(cmd)

def parse_cfg(cfg):
    return cfg.split(',')

if(TESTE):
    adminorclient('11112222')
    while True:
        if(len(inserting_db) != 0):
            db.insertCode(inserting_db.pop(0))
        if(len(deleting_db) > 0):
            db.deleteCode(deleting_db.pop(0))
        if(len(sub_db.response) > 0):
            sub_db.response.pop(0)
            publisher.run('server_send_db',db.get_all(host,user,password,table,))
        time.sleep(0.01)

if(not TESTE):
    while True:
        if(len(inserting_db) != 0):
            not_parsed = inserting_db.pop(0)
            insert_content = not_parsed.split(',')
            db.insertCode(host,user,password,table,inserting_db.pop(0))
        if(len(deleting_db) > 0):
            db.deleteCode(host,user,password,table,deleting_db.pop(0))
        if(len(sub_db.response) > 0):
            sub_db.response.pop(0)
            publisher.run('server_send_db',db.get_all())
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            logging.info(str(rfdevice.rx_code) +
                        " [pulselength " + str(rfdevice.rx_pulselength) +
                        ", protocol " + str(rfdevice.rx_proto) + "]")
            adminorclient(str(rfdevice.rx_code))

        schedule.run_pending()
        time.sleep(0.01)
        #time.sleep(3)
    rfdevice.cleanup()