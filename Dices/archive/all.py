# -*- coding: utf-8 -*-
from SimpleCV import *
from SimpleCV.Color import Color
from matplotlib import pyplot as plt
import webcolors
import time
import colorsys

for j in range(1,13):
    filename =""+str(j)
    img = Image(filename+".jpg")

    dl = DrawingLayer((img.width, img.height))

    print "load file "+filename+".jpg"

    img.show()
    time.sleep(1)

    white_dice = img.smooth('median',(5,5))

    white_dice.show()
    time.sleep(1)

    histo = white_dice.toGray()
    histo_eq = histo.equalize()
    histo_eq.show()
    time.sleep(1)

    max = histo_eq.maxValue()
    min = histo_eq.minValue()

    print [max, min]

    stretch = white_dice.stretch(min,max-120)
    stretch.show()
    time.sleep(1)



    only_dice_int = stretch.binarize().invert().erode(1).dilate(2)

    blobs = only_dice_int.findBlobs(minsize=40)
    blobs.show()
    time.sleep(1)

    if blobs is not None:

        print "blobs:" + str(len(blobs))

        for blob in blobs:
            print [blob.perimeter(), blob.area(), blob.angle(),blob.coordinates()]

        circles = blobs.filter([b.perimeter() < 55 and  b.perimeter() > 30 for b in blobs])

        if circles is not None:
            if len(circles) > 0:
                print "cirlces: "+ str(len(circles))
                circles.show()
                time.sleep(1)

