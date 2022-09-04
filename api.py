import requests
import conf

def getQueue():
    r = requests.get(f'http://{conf.IP}:{conf.HTTP_port}/')
    return r.text.split(',')

print(getQueue())