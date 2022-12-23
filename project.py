# Import Library
import serial.tools.list_ports
import time
import sys
from Adafruit_IO import MQTTClient
from datetime import datetime
from Adafruit_IO import Client

# Adafruit_IO Config
AIO_FEED_ID = ["actuator1", "actuator2", "actuator3", "actuator4"]
AIO_USERNAME = "tranlydongdong"
AIO_KEY = "aio_mVLt08wD3Nd2mVBdedDiZHFu4tJq"


# Adafruit_IO Function
def connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID)


def subscribe(client, userdata, mid, granted_qos):
    print("Subcribe thanh cong...")


def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Nhan du lieu: " + payload)
    setDevice1(payload)
    ser.write((str(payload) + "#").encode())


# Physical Function

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "COM3" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


portName = getPort()
ser = None
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)


def serial_read_data(ser1):
    bytesToRead = ser1.inWaiting()
    if bytesToRead > 0:
        out = ser1.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0


soil_temperature = [1, 3, 0, 6, 0, 1, 100, 11]
soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]


def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)


def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)


# Adafruit_IO connected
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


# Send data from sensor to Adafruit_IO
def sendData():
    time.sleep(60)
    client.publish("sensor1", readMoisture() / 100)
    time.sleep(1)
    client.publish("sensor2", readTemperature() / 100)
    time.sleep(1)


def autoPump():
    nw = datetime.now()
    if nw.hour == 15 and nw.minute == 0:
        client.publish("actuator3", 1)
    if nw.hour == 15 and nw.minute == 15:
        client.publish("actuator3", 0)


def getAutoMode():
    aio = Client(AIO_USERNAME, AIO_KEY)
    dataAutoMode = aio.data('actuator4')
    for d in dataAutoMode:
        return d.value


while True:
    # sendData()
    # openPump()
    time.sleep(5)
    pass

# API
'''
Get last_value
Sensor 1: https://io.adafruit.com/api/v2/tranlydongdong/feeds/sensor1
Sensor 2: https://io.adafruit.com/api/v2/tranlydongdong/feeds/sensor2

actuator3: pump
actuator4: auto mode of pump
Time
updated_at
'''
