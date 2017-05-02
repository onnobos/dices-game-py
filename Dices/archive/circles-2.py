# -*- coding: utf-8 -*-
from SimpleCV import *
from SimpleCV.Color import Color
from matplotlib import pyplot as plt
import webcolors
import time
import colorsys

for j in range(10,15):
    filename ="white-"+str(j)
    img = Image(filename+".jpg")

    print "load file "+filename+".jpg"

    img.show()
    time.sleep(1)

    white_dice = img.hueDistance(Color.YELLOW,minsaturation=80, minvalue=15)
    only_dice = img - white_dice

    only_dice_int = only_dice.binarize()

    only_dice_int.show()
    time.sleep(1)

    only_dice_fil = only_dice_int.floodFill((0,0),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((img.width-1,0),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((img.width-1,img.height-1),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((0,img.height-1),color=Color.BLACK)


    only_dice_fil.show()
    time.sleep(1)

    blobs = only_dice_fil.findBlobs()
    if blobs is not None:
        print "pips "+ str(len(blobs))
    print blobs