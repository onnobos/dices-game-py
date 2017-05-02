# -*- coding: utf-8 -*-
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(10)
camera.capture('foo.jpg')