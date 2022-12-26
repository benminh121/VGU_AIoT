import time
import cv2
import argparse
import numpy as np
from imutils.video import VideoStream
import imutils
import pyglet

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


# Doc tu webcam
cap = VideoStream(src=2).start()

# Doc ten cac class
classes = None
with open('yolov3.txt', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
# net = cv2.dnn.readNet(args.weights, args.config)
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
nCount = 0

# Bat dau doc tu webcam
while (True):

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
            # Play file sound
            music = pyglet.resource.media('police.wav')
            music.play()
            # pyglet.app.run()

    cv2.imshow("object detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
cv2.destroyAllWindows()
