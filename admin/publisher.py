# python 3.6

import random
import time
import datetime

from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{datetime.datetime.now()}'
username = 'emqx'
password = 'public'
global global_client

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker! publisher {client_id}")
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
        #print(f"Send `{msg}` to topic `{topic}`")
        pass
    else:
        print(f"Failed to send message to topic {topic}")
    client.disconnect()

def run(topic,data):
    global global_client
    print(f'inicia publisher {topic}' )
    client = connect_mqtt()
    global_client = client
    print('conectancdo publisher mqtt')
    client.loop_start()
    print('enviando dado do publisher')
    publish(client,topic,data)

if __name__ == '__main__':
    topic = 'sub_press_btnsec'
    data = 'dado'
    run(topic,data)