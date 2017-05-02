# -*- coding: utf-8 -*-
from SimpleCV import *
from SimpleCV.Color import Color
from matplotlib import pyplot as plt
import webcolors
import time
import colorsys

for j in range(5,15):
    filename ="white-"+str(j)
    img = Image(filename+".jpg")

    print "load file "+filename+".jpg"
    img.show()
    time.sleep(1)

    img_edges = img.watershed()

    img_edges.show()
    time.sleep(1)

    img_circles = img_edges.floodFill((0,0),color=Color.WHITE).invert()


    img_circles.show()
    time.sleep(1)

    blobs = img_circles.findBlobs()
    if blobs is not None:
        print "pips "+ str(len(blobs))
    print blobs

raw_input("Press Enter to Exit")
