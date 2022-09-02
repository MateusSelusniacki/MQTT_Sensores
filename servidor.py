import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

mqttBroker ="192.168.18.51:1883" 

client = mqtt.Client("client")
client.connect(mqttBroker) 

while True:
    randNumber = uniform(20.0, 21.0)
    client.publish("Client", randNumber)
    print("Just published " + str(randNumber) + " to topic TEMPERATURE")
    time.sleep(1)