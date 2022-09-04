import publisher
import time
import db
import subscriber as sub

queue = []

def client_publish(comando):
    publisher.run('client',comando)
    queue.append(comando)
    sub.run('accept')
    publisher.run('ack','ack')

client_publish('comando')