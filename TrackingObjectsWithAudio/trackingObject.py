import cv2
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

pan1 = 90
tilt1 = 90
pan2 = 90
tilt2 = 90

kit.servo[0].angle = pan1
kit.servo[1].angle = tilt1
kit.servo[2].angle = pan2
kit.servo[3].angle = tilt2

# supported resolution: 640x480, 1280x720, 1920x1080, 3840x2160, 4096x2160, 4192x3120
width = 1280
height = 720

cam1 = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam2 = cv2.VideoCapture(1, cv2.CAP_V4L2)

cam1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cam2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10.0, (1280, 720))

# tracker_types = ['MOSSE', 'KCF', 'CSRT', 'BOOSTING', 'MIL', 'TLD', 'MEDIANFLOW', 'GOTURN']

# tracker1 = cv2.TrackerMOSSE_create()  # Faster than CSRT but less accurate
# tracker1 = cv2.TrackerKCF_create()  # In the middle of CSRT and MOSSE
tracker1 = cv2.TrackerCSRT_create()  # Slower than MOSSE but more accurate

# tracker2 = cv2.TrackerMOSSE_create()  # Faster than CSRT but less accurate
# tracker2 = cv2.TrackerKCF_create()  # In the middle of CSRT and MOSSE
tracker2 = cv2.TrackerCSRT_create()  # Slower than MOSSE but more accurate

success1, img1 = cam1.read()
bbox1 = cv2.selectROI("Tracking Object", img1, False)
tracker1.init(img1, bbox1)

success2, img2 = cam2.read()
bbox2 = cv2.selectROI("Tracking Object", img2, False)
tracker2.init(img2, bbox2)

flag1 = True
flag2 = False
count1 = 0
count2 = 0


def drawBox(img, bbox, camNum, pan, tilt):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    objX = x + (w / 2)
    objY = y + (h / 2)
    errorPan = objX - (width / 2)
    errorTilt = objY - (height / 2)

    if camNum == 1:
        if abs(errorPan) > 15:
            pan = pan + (errorPan / 250)
        if abs(errorTilt) > 15:
            tilt = tilt - (errorTilt / 250)
        if pan > 180:
            pan = 180
            print('Pan 1 Out of Range')
        if pan < 0:
            pan = 0
            print('Pan 1 Out of Range')
        if tilt > 180:
            tilt = 180
            print('Tilt 1 Out of Range')
        if tilt < 0:
            tilt = 0
            print('Tilt 1 Out of Range')

        kit.servo[0].angle = pan
        kit.servo[1].angle = tilt

        cv2.putText(img, "Tracking Object 1", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    elif camNum == 2:
        if abs(errorPan) > 15:
            pan = pan + (errorPan / 250)
        if abs(errorTilt) > 15:
            tilt = tilt - (errorTilt / 250)
        if pan > 180:
            pan = 180
            print('Pan 2 Out of Range')
        if pan < 0:
            pan = 0
            print('Pan 2 Out of Range')
        if tilt > 180:
            tilt = 180
            print('Tilt 2 Out of Range')
        if tilt < 0:
            tilt = 0
            print('Tilt 2 Out of Range')

        kit.servo[2].angle = pan
        kit.servo[3].angle = tilt
        cv2.putText(img, "Tracking Object 2", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

    return pan, tilt

while True:
    timer = cv2.getTickCount()

    success1, img1 = cam1.read()
    success1, bbox1 = tracker1.update(img1)

    success2, img2 = cam2.read()
    success2, bbox2 = tracker2.update(img2)

    if success1:
        pan1, tilt1 = drawBox(img1, bbox1, 1, pan1, tilt1)
    else:
        cv2.putText(img1, "Lost Target 1", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        success1, bbox1 = tracker1.update(img1)

    if success2:
        pan2, tilt2 = drawBox(img2, bbox2, 2, pan2, tilt2)
    else:
        cv2.putText(img2, "Lost Target 2", (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
        success2, bbox2 = tracker2.update(img2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img1, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(img2, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Tracking Object", img1)
    cv2.imshow("Tracking Object 2", img2)

    # out.write(img1)

    # if flag1:
    #     cv2.putText(img1, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    #     cv2.imshow("Tracking Object", img1)

    #     count1 = count1 + 1
    #     # print(count1)
    #     if count1 == 120:
    #         count1 = 0
    #         flag1 = False
    #         flag2 = True

    # if flag2:
    #     cv2.putText(img2, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    #     cv2.imshow("Tracking Object", img2)

    #     count2 = count2 + 1
    #     # print(count2)
    #     if count2 == 120:
    #         count2 = 0
    #         flag1 = True
    #         flag2 = False

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()