# -*- coding: utf-8 -*-
from SimpleCV import *
from SimpleCV.Color import Color
from matplotlib import pyplot as plt
import webcolors
import time
import colorsys

for j in range(1,5):
    filename ="blue-"+str(j)
    img = Image(filename+".jpg")

    print "load file "+filename+".jpg"

    img.show()
    time.sleep(1)

    white_dice = img.hueDistance(Color.BLUE,minsaturation=90, minvalue=10)
    only_dice = img - white_dice

    only_dice_int = only_dice.binarize().erode(1).dilate()

    only_dice.show()
    time.sleep(1)

    only_dice_fil = only_dice_int.floodFill((0,0),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((img.width-1,0),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((img.width-1,img.height-1),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((0,img.height-1),color=Color.BLACK)


    only_dice_fil.show()
    time.sleep(1)

    blobs = only_dice_fil.findBlobs()
    blobs.show()
    time.sleep(1)
    if blobs is not None:
        pips = 0
        for blob in blobs:
            if(blob.isCircle(0.9)):
                pips = pips + 1
        print "pips "+ str(len(blobs))
        print "circle pips "+ str(pips)