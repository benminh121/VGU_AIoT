import serial.tools.list_ports


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


portName = getPort()
ser = None
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)


def writeData(data):
    ser1.write((str(data)).encode())


def sendData(client):
    # client.publish("actuator1", readTemperature())
    # client.publish("actuator2", readMoisture())
    client.publish("sensor1", 50)


'''
Get last_value
Sensor 1: https://io.adafruit.com/api/v2/tranlydongdong/feeds/sensor1
Sensor 2: https://io.adafruit.com/api/v2/tranlydongdong/feeds/sensor2

Time
updated_at
'''
