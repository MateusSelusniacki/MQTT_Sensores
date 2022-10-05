# python3.6
import datetime

from paho.mqtt import client as mqtt_client
import time

broker = 'broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{datetime.datetime.now()}'
username = 'emqx'
password = 'public'
response = []
global_client = []
connected_once = [0]
rerun = [-1,0]
topico = []
clients = dict()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            pass
            print(f"Connected to MQTT Broker! subscriber - topic {topico[0]}{client_id}")
        else:
            pass
            print("Failed to connect, return code %d\n", rc)

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

def disconnect():
    print('disconect2')
    global_client[0].disconnect()

def run(topic):
    t1 = time.time()
    topico.append(topic)
    print(f'iniciando subscriber - topic {topic}')
    
    client = connect_mqtt()
    global_client.append(client)
    print('enviando dado do subscriber')
    subscribe(client,topic)
    
    while(time.time() - t1 < 10 and len(response) == 0):
        client.loop()

if __name__ == '__main__':
    run('admin')