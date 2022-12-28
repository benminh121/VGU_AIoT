# Import Library
import time
import sys
from Adafruit_IO import MQTTClient
from Adafruit_IO import Client
from datetime import datetime
import os
from dotenv import load_dotenv
from sendData import *
# from faceDetect import *
load_dotenv(".env")

# Adafruit_IO Config
AIO_FEED_ID = ["actuator2", "actuator3"]
AIO_USERNAME = os.environ.get('AIO_USERNAME')
AIO_KEY = os.environ.get('AIO_KEY')


def connected(client):
    client
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong...")


def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)


def message(client, feed_id, payload):
    global autoPumpButton, hour, minute
    if feed_id == "actuator3":
        autoPumpButton = payload
        print("Mode: ", autoPumpButton)
    elif feed_id == "pumptime":
        hour = int(autoPumpButton.split(":")[0])
        minute = int(autoPumpButton.split(":")[1])


# Adafruit_IO connected
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
aio = Client(AIO_USERNAME, AIO_KEY)

autoPumpButton = aio.receive('actuator3').value
pumpButton = aio.receive('actuator2').value
hour = int(aio.receive('pumptime').value.split(":")[0])
minute = int(aio.receive('pumptime').value.split(":")[1])


def autoPump():
    if int(autoPumpButton) == 1 and int(pumpButton) == 0:
        nw = datetime.now()
        print(nw.hour, hour, nw.minute, minute)
        if nw.hour == hour and nw.minute == minute:
            client.publish("actuator2", 1)
        if nw.hour == hour and nw.minute == (minute + 15):
            client.publish("actuator2", 0)


pumpCounter = 0

while True:
    # sendData(client)
    # FaceDetector(client)
    pumpCounter -= 1
    if pumpCounter <= 0:
        autoPump()
        pumpCounter = 900
    time.sleep(1)

# API
'''
actuator1: light
actuator2: pump
actuator3: auto mode of pump, api: https://io.adafruit.com/api/v2/tranlydongdong/groups/default/feeds/actuator3/data, send 0 1
actuator4: travel mode
actuator5: alarm
'''
