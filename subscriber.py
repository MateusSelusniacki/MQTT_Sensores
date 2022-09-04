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

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! subscriber")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client,topic):
    print('subscribe subscriber')
    def on_message(client, userdata, msg):
        print(f'publicação recebido - topico: {topic}')
        client.disconnect()

    client.subscribe(topic)
    client.on_message = on_message

def run(topic):
    print('iniciando subscriber')
    client = connect_mqtt()
    print('enviando dado do subscriber')
    subscribe(client,topic)
    client.loop_forever()


if __name__ == '__main__':
    run()