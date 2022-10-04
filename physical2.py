import serial.tools.list_ports
import time
import sys

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "FT232R USB UART" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


portName = getPort()
if portName != "None":
    ser = serial.Serial(port=portName, baudrate=9600)

# print(getPort())

relay1_ON = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

while True:
    ser.write(relay1_ON)
    time.sleep(2)
    ser.write(relay1_OFF)
    time.sleep(10)