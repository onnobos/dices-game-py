from SimpleCV import *
from SimpleCV.Color import Color
from matplotlib import pyplot as plt
import webcolors
import time
import colorsys

dices =[]

filename ="File_000_small"
img = Image(filename+".jpeg")
dl = DrawingLayer((img.width, img.height))
counter = 0
##Get Yellow and White Dices
img_bin = img.binarize().invert()
img_erode = img_bin.erode(2)
img_dilate = img_erode.dilate(1)
blobs = img_dilate.findBlobs(minsize=3000, maxsize=8000)
found_yellow = False
for blob in blobs:
    img_crop = img.crop(blob)
    img_crop.show()
    time.sleep(1)
    white_dice = img_crop.hueDistance(Color.YELLOW,minsaturation=100, minvalue=10)
    only_dice = img_crop - white_dice
    only_dice.show()
    # (b, g, r)
    time.sleep(1)
    only_dice_bin = only_dice.binarize().invert()
    only_dice_bin.show()
    time.sleep(1)
    blobs_crop = only_dice_bin.findBlobs(minsize=3000, maxsize=6000)
    blob.drawRect(layer=dl, color=Color.RED,width=4)

    if blobs_crop is not None:
        blob.myColor = "yellow"
        print ("Yellow")
    else:
        blob.myColor = "white"
        print("White")
    dices.append(blob)

#Get Blue Dice
hue = img.hueDistance(Color.BLUE)
mask = hue.binarize(70)
mask_erode = mask.erode(1).dilate(1)
blobs = mask_erode.findBlobs(minsize=3000, maxsize=8000)
blobs[0].drawRect(layer=dl, color=Color.RED,width=4)
blobs[0].myColor = "blue"
dices.append(blobs[0])

#Get Red Dice
img_red = img.hueDistance(Color.RED)
img_red_bin = img_red.binarize(15)
img_red_bin_erode = img_red_bin.erode(2).dilate(1)
blobs = img_red_bin_erode.findBlobs(minsize=3000, maxsize=8000)
blobs[0].drawRect(layer=dl, color=Color.RED,width=4)
blobs[0].myColor = "red"
dices.append(blobs[0])

#Get Green Dice
img_green = img.hueDistance(Color.GREEN)
img_green_bin = img_green.binarize(30)
img_green_bin_erode = img_green_bin.erode(2).dilate(1)
blobs = img_green_bin_erode.findBlobs(minsize=3000, maxsize=8000)
blobs[0].drawRect(layer=dl, color=Color.RED,width=4)
blobs[0].myColor = "green"
dices.append(blobs[0])

#Display Dices on Pictures
print dices
img.addDrawingLayer(dl)
#img.show()

print len(dices)
counter = 0
for dice in dices:
    counter = counter + 1
    img_crop = img.crop(dice)
    if hasattr(dice, 'myColor'):
        print "Color is %s" % dice.myColor
        img_crop.save(filename+"-"+dice.myColor+"-"+str(counter)+".jpg")
    else:
        print "No Color Found."
    img_crop.show()
    time.sleep(1)

#Green
#(0.31183987020623266, 0.5404349348421589, 49.9510582010582, 16.934444335368863)
#(0.3218349200886486, 0.3919263823369702, 147.71745104774993)
#(0.32216346240472804, 0.5135293518926904, 83.77803617571058)
#(0.33600406969350116, 0.38860103626943004, 72.55493402180149)

#Blue
#(0.017451761581126452, 0.2438425052860163, 51.46764705882352)
#(0.019954549739247002, 0.24672033308630936, 77.89556404230316)
#(0.02393372396395708, 0.2423781746701019, 98.4128891941392)
#(0.024080745140038384, 0.15493223317519828, 52.86562998405104)

#Red
#(0.6685814336328658, 0.4998588905307619, 133.96686491079015)
#(0.668311937299908, 0.7237137425200725, 104.7848277608916)
#(0.649303657385511, 0.5756570165745857, 69.90792238289458)
#(0.6560527154529893, 0.6042703688607272, 98.85347985347985)

#Yellow
#(0.5194635580090355, 0.4530200426879394, 181.28241112002138)
#(0.5484700075444676, 0.6676895072606314, 170.23953488372092)
#(0.5447387840356209, 0.7073156826414111, 202.17309220985692)
#(0.5523713826630267, 0.7198983741565423, 138.2150411280846)

#White
#(0.5490838244292018, 0.04656843999550107, 169.3910989178479)
#(0.5507803599908864, 0.11809233390883207, 150.4689608636977)
#(0.5672380578391283, 0.14931816965071015, 119.58932926829269)
#(0.5680591521068347, 0.048013170502704226, 178.96304347826086)
#(0.5745513300601925, 0.12374448313998156, 136.01036414565826)
#(0.5745513300601925, 0.12374448313998156, 136.01036414565826)
#(0.5716388135389595, 0.1634260665769715, 113.4226441631505)
#(0.5840567937587787, 0.1543575423372404, 163.17945439045184)

#raw_input("Press Enter to Exit")
