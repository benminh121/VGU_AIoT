import sys
from Adafruit_IO import MQTTClient
from test import *

AIO_FEED_ID = "FaceDetector"
AIO_USERNAME = "tranlydongdong"
AIO_KEY = "aio_mVLt08wD3Nd2mVBdedDiZHFu4tJq"

def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter_ai = 5

while True:
    counter_ai = counter_ai -1
    if counter_ai <= 0:
        counter_ai = 5
        ai_result = image_detector()
        print(ai_result)
        client.publish(ai_result)
    pass
