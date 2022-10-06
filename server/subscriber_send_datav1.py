# python3.6
import datetime

from paho.mqtt import client as mqtt_client
import time

broker = None
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
            response = []
            print(f"Connected to MQTT Broker! subscriber - topic {topico[0]}{client_id}")
            rerun[0] += 1
            if(rerun[0] == 1):
                client.disconnect()
                rerun[0] = -1
                rerun[1] = 1
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
    connected_once[0] = 0
    topico.append(topic)
    print(f'iniciando subscriber - topic {topic}')
    
    client = connect_mqtt()
    
    print('enviando dado do subscriber')
    subscribe(client,topic)
    client.loop_forever()
    if(rerun[1]):
        rerun[1] = 0
        run(topic)
    else:
        pass
        print('reponse',response)

if __name__ == '__main__':
    run('admin')