import os
import glob
import time
from SimpleCV import *
from SimpleCV.Color import Color
import time

img = Image("output.jpg")
img_light = img * 2.5
lines = img_light.findLines()

lines.filter(lines.length()>50)
lines.show(width=3)
time.sleep(2)

vertical = lines.filter((np.abs(lines.angle()) > 80))
vertical.draw(width=3)
img_light.show()
img_light.applyLayers().save("lines.png")
