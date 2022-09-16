# python3.6

import random

from paho.mqtt import client as mqtt_client

import publisher

broker = 'broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'
response = []
global global_client

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        global connected_once
        if rc == 0:
            connected_once = 0
            print("Connected to MQTT Broker! subscriber")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    print('1')
    client.username_pw_set(username, password)
    print('2')
    client.on_connect = on_connect
    print('3')
    client.connect(broker, port)
    print('4')
    return client

def subscribe(client: mqtt_client,topic):
    print('subscribe subscriber')
    def on_message(client, userdata, msg):
        print(f'publicação recebido - topico: {topic} {str(msg.payload)}')
        response.append(str(msg.payload.decode()[10:]))
        client.disconnect()

    client.subscribe(topic)
    client.on_message = on_message

def disconnect():
    global global_client
    global_client.disconnect()

def run(topic):
    global global_client
    print('iniciando subscriber')
    client = connect_mqtt()
    global_client = client    
    print('enviando dado do subscriber')
    subscribe(client,topic)
    client.loop_forever()
    print('reponse',response)
    return response[0]

if __name__ == '__main__':
    run()