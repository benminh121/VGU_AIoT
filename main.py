# Import Library
import time
import sys
from Adafruit_IO import MQTTClient
from datetime import datetime
from Adafruit_IO import Client
from sendData import *
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Adafruit_IO Config
AIO_FEED_ID = ["actuator1", "actuator2", "actuator3", "actuator4"]
AIO_USERNAME = os.environ.get('AIO_USERNAME')
AIO_KEY = os.environ.get('AIO_KEY')


def connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong...")


def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)


def message(client, feed_id, payload):
    if feed_id == "actuator3":
        autoPumpButton = payload
        print("Mode: ", autoPumpButton)


# Adafruit_IO connected
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


def autoPump():
    nw = datetime.now()
    if nw.hour == 15 and nw.minute == 0:
        client.publish("actuator3", 1)
    if nw.hour == 15 and nw.minute == 15:
        client.publish("actuator3", 0)


while True:
    # sendData(client)
    time.sleep(1)
    pass

# API
'''
actuator1: light
actuator2: pump
actuator3: auto mode of pump, api: https://io.adafruit.com/api/v2/tranlydongdong/groups/default/feeds/actuator3/data, send 0 1

'''
