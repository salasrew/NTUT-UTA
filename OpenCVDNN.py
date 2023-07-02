import cv2
import numpy as np

net = cv2.dnn.readNet("./backup/yolov4-custom_final.weights", "./cfg/yolov4-custom.cfg")
classes = []
with open("./data/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

frame_width = 640
frame_height = 480
output_video = cv2.VideoWriter("output2.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 25, (frame_width, frame_height))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                width = int(detection[2] * frame_width)
                height = int(detection[3] * frame_height)
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    for i in range(len(boxes)):
        if i in indexes:
            x, y, width, height = boxes[i]
            label = classes[class_ids[i]]
            confidence = confidences[i]
            color = colors[class_ids[i]]

            cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
            cv2.putText(frame, "{} {:.2f}".format(label, confidence), (x, y - 10), font, 0.5, color, 2)

    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    output_video.write(frame)

cap.release()
output_video.release()
cv2.destroyAllWindows()
