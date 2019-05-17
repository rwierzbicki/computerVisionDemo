#!/usr/bin/python
#encoding: utf-8

from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import btconn
import bluetooth
import imutils
import time
import cv2
import lane_detect as ld

if __name__ == "__main__":
    vstream = PiVideoStream().start()
    time.sleep(2.0)
    fps = FPS().start()
    sock = btconn.clientconnect(0x100F, btconn.bdBaseAddr, bluetooth.L2CAP)


    while True:

        frame = vstream.read()
        location = ld.Houghdat(frame)
        sock.send(str(location))
        time.sleep(0.05)

