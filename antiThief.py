import time
import cv2
import numpy as np
from imutils.video import VideoStream
import imutils
import pyglet
import os
from dotenv import load_dotenv
from Adafruit_IO import Client
from Adafruit_IO import MQTTClient

load_dotenv(".env")

AIO_FEED_ID = ["actuator4"]
AIO_USERNAME = os.environ.get('AIO_USERNAME')
AIO_KEY = os.environ.get('AIO_KEY')

# Adafruit_IO connected
aio = Client(AIO_USERNAME, AIO_KEY)
actuator4 = aio.receive('actuator4')
feed4 = aio.feeds('actuator4')
feed5 = aio.feeds('actuator5')


# Adafruit MQTT
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
    global temp
    if feed_id == "actuator4":
        temp = int(payload)
        print(type(temp), temp)


# Ham tra ve output layer
def get_output_layers(net1):
    layer_names = net1.getLayerNames()
    output_layers = [layer_names[a - 1] for a in net1.getUnconnectedOutLayers()]
    return output_layers


# Ham ve cac hinh chu nhat va ten class
def draw_prediction(img, class_id, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

temp = 0
aio.send_data(feed5.key, 0)
actuator4 = aio.receive('actuator4')
while True:
    actuator4 = aio.receive('actuator4')
    valueTravel = int(actuator4.value)
    print("Travel", valueTravel)
    actuator5 = aio.receive('actuator5')
    valueAlarm = int(actuator5.value)
    print(type(temp), temp)
    if temp == 0:
        aio.send_data(feed5.key, 0)
    actuator5 = aio.receive('actuator5')
    valueAlarm = int(actuator5.value)
    print("Alarm: ", valueAlarm)
    if valueTravel == 1 and valueAlarm == 0:
        # Doc tu webcam
        cap = VideoStream(src=1).start()
        # Doc ten cac class
        classes = None
        with open('model/yolov3.txt', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
        net = cv2.dnn.readNet('model/yolov3.weights', 'model/yolov3.cfg')
        nCount = 0
        # Bat dau doc tu webcam
        while True:
            # Doc frame
            frame = cap.read()
            image = imutils.resize(frame, width=600)

            # Bien theo doi do vat co ton tai trong khung hinh hay khong
            isExist = False

            # Resize va dua khung hinh vao mang predict
            Width = image.shape[1]
            Height = image.shape[0]
            scale = 0.00392
            blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(get_output_layers(net))

            # Loc cac object trong khung hinh
            class_ids = []
            confidences = []
            boxes = []
            conf_threshold = 0.5
            nms_threshold = 0.4

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if (confidence > 0.5) and (classes[class_id] == 'car'):
                        center_x = int(detection[0] * Width)
                        center_y = int(detection[1] * Height)
                        w = int(detection[2] * Width)
                        h = int(detection[3] * Height)
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])

            indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

            # Ve cac khung chu nhat quanh doi tuong
            for i in indices:
                box = boxes[i]
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                if classes[class_ids[i]] == 'car':
                    isExist = True
                    draw_prediction(image, class_ids[i], round(x), round(y), round(x + w), round(y + h))

            # Neu ton tai do vat thi set so frame =0
            if isExist:
                nCount = 0
            else:
                # Neu khong ton tai thi tang so frame khong co len
                nCount += 1
                # Neu qua 5 frame ko co thi bao dong!
                if nCount > 10:
                    # hien thi chu Alarm
                    cv2.putText(image, "Alarm alarm alarm!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    aio.send_data(feed5.key, 1)
                    break
            cv2.imshow("object_detection", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.stop()
        # traval = 1, alarm = 1 ->
    time.sleep(1)
