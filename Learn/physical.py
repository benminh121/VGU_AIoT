import serial.tools.list_ports
import time
import sys

from Adafruit_IO import MQTTClient

AIO_FEED_ID = "Actuator1"
AIO_USERNAME = "tranlydongdong"
AIO_KEY = "aio_mVLt08wD3Nd2mVBdedDiZHFu4tJq"


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

relay1_ON = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

relay2_ON = [15, 6, 0, 0, 0, 255, 200, 164]
relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]


def setDevice1(state):
    if state == True:
        while True:
            ser.write(relay1_ON)
            time.sleep(2)
            ser.write(relay1_OFF)
            time.sleep(5)
    else:
        ser.write(relay1_OFF)


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


def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)


soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]


def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


while True:
    client.publish("sensor1", readTemperature()/100)
    client.publish("sensor2", readMoisture()/100)
    pass
# DOng
