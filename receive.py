import RPi.GPIO as GPIO
import time
ERROR = 0xFE
PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
print(PIN)

while not GPIO.input(PIN):
    print(PIN)
    pass
print('saiu')
GPIO.cleanup()