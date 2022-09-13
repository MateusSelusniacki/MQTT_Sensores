import publisher
import time
import db
import subscriber as sub
import schedule

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

admin_publish('comando')