# python 3.6
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
global global_client

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            pass
            print(f"Connected to MQTT Broker! publisher {client_id}")
        else:
            pass
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,topic,data):
    time.sleep(1)
    msg = f"messages: {data}"
    #print(f'publicando - {topic} - ')
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        pass
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        pass
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
    topic = 'client'
    data = 'dado'
    run(topic,data)