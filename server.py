import publisher
import time
import db
import subscriber as sub
import schedule
import threading

queue = []

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

def read_rasp():
    signal = "comando"
    command = db.getCode(signal)
    if(command == ''):
        print('a')
        c_a = 'a'
    else:
        print('c')
        c_a = 'c'
        
    th = threading.Thread(target = on_signal,args=(signal,c_a))

    th.start()

read_rasp()