# python3.6
import datetime

from paho.mqtt import client as mqtt_client
import time
import threading

broker = None
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-eccept{datetime.datetime.now()}'
username = 'emqx'
password = 'public'
response = []
global_client = []
connected_once = [0]
rerun = [-1,0]
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

def thread_publisher(client,topic,comando):
    msg = f"messages: {comando}"
    #print(f'publicando {comando} para o topico {topic}')
    client.publish(topic,msg)
    t1 = time.time()
    while(not fim_thread[0]):
        if(time.time() - t1 > 4):
            t1 = time.time()
            #print(f'publicando para o topico {topic}')
            result = client.publish(topic,msg)
            status = result[0]
            if status == 0:
               # print(f"Send {comando} to topic `{topic}`")
               pass
            else:
                print(f"Failed to send message to topic {topic}")
    print('final da thread publishe morreu')
    fim_thread[0] = 0

def run(topic,pub,comando):
    topico.append(topic)
    print(f'iniciando subscriber - topic {topic}')
    
    client = connect_mqtt()
    threading.Thread(target = thread_publisher,args = (client,pub,comando)).start()
    print('enviando dado do subscriber')
    subscribe(client,topic)
    
    client.loop_forever()
    fim_thread[0] = 1
    print('morreu', topic)

if __name__ == '__main__':
    run('admin')