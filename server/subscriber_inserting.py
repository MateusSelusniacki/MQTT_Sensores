# python3.6
import datetime

from paho.mqtt import client as mqtt_client
import time
#import publisher
import threading

broker = 'test.mosquitto.org'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-inserting{datetime.datetime.now()}'
username = 'emqx'
password = 'public'
response = []
global_client = []
connected_once = [0]
fim_thread = [0]
topico = []
clients = dict()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            response = []
            print(f"Connected to MQTT Broker! subscriber - topic {topico[0]}{client_id}")
        else:
            pass
            print(f"Failed to connect, return code{topico[0]}{rc}\n", )

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client

def subscribe(client: mqtt_client,topic):
    print('subscribe subscriber')
    def on_message(client, userdata, msg):
        print(f'publicação recebida - topico: {topic} {str(msg.payload)}')
        response.append(str(msg.payload.decode()[10:]))
        client.disconnect()

    client.subscribe(topic)
    client.on_message = on_message

def run(topic):
    connected_once[0] = 0
    topico.append(topic)
    print(f'iniciando subscriber - topic {topic}')
    
    client = connect_mqtt()
    print('enviando dado do subscriber')
    subscribe(client,topic)
    
    client.loop_forever()
    fim_thread[0] = 1
    print('morreu', topic)
if __name__ == '__main__':
    run('admin')