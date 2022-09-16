# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'
global global_client

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! publisher")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,topic,data):
    time.sleep(1)
    msg = f"messages: {data}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    client.disconnect()

def disconnect():
    global global_client
    global_client.disconnect()

def run(topic,data):
    global global_client
    print('inicia publisher')
    client = connect_mqtt()
    global_client = client
    print('conectancdo publisher mqtt')
    client.loop_start()
    print('enviando dado do publisher')
    publish(client,topic,data)

if __name__ == '__main__':
    topic = 'client'
    data = 'dado'
    run(topic,data)