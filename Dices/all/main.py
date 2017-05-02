import os
import glob
import time
from SimpleCV import *
from SimpleCV.Color import Color
import time

print __doc__

#Constants
INFO = "I"
WARNING = "W"
ERROR = "E"

#Settings
my_images_path = os.getcwd() #get the current directory
extension = "*.jpg"
input_image_file = "File_004_small.jpeg"
showimages = False

def logEntry(typeEntry,text):
    print typeEntry + ":" + text

def showImage(img):
    if showimages:
        img.show()
        time.sleep(1)

def findDicesB(img, dices):
    """Find the Blue dice in a picture"""
    logEntry(INFO, "Finding the Blue Dice in the picture..")
    hue = img.hueDistance(Color.BLUE)
    mask = hue.binarize(70)
    mask_erode = mask.erode(1).dilate(1)
    blobs = mask_erode.findBlobs(minsize=3000, maxsize=8000)
    if blobs is not None:
        logEntry(INFO, "Found blue Dice")
        blobs[0].myColor = "blue"
        dices.append(blobs[0])
    return dices

def findDicesG(img, dices):
    """Find the Green dice in a picture"""
    logEntry(INFO, "Finding the Green Dice in the picture..")
    img_green = img.hueDistance(Color.GREEN)
    img_green_bin = img_green.binarize(30)
    img_green_bin_erode = img_green_bin.erode(2).dilate(1)
    blobs = img_green_bin_erode.findBlobs(minsize=3000, maxsize=8000)
    if blobs is not None:
        logEntry(INFO, "Found green Dice")
        blobs[0].myColor = "green"
        dices.append(blobs[0])
    return dices

def findDicesR(img, dices):
    """Find the Red dice in a picture"""
    logEntry(INFO, "Finding the Red Dice in the picture..")
    img_red = img.hueDistance(Color.RED)
    img_red_bin = img_red.binarize(15)
    img_red_bin_erode = img_red_bin.erode(2).dilate(1)
    blobs = img_red_bin_erode.findBlobs(minsize=3000, maxsize=8000)
    if blobs is not None:
        blobs[0].myColor = "red"
        logEntry(INFO, "Found red Dice")
        dices.append(blobs[0])
    return dices

def findDicesWY(img, dices):
    """Find the White & Yellow dices in a picture"""
    logEntry(INFO, "Finding the Yellow and White Dices in the picture..")
    img_bin = img.binarize().invert()
    img_erode = img_bin.erode(2)
    img_dilate = img_erode.dilate(1)
    blobs = img_dilate.findBlobs(minsize=3000, maxsize=8000)
    found_yellow = False
    for blob in blobs:
        img_crop = img.crop(blob)
        showImage(img_crop)
        white_dice = img_crop.hueDistance(Color.YELLOW,minsaturation=100, minvalue=10)
        only_dice = img_crop - white_dice
        showImage(only_dice)
        only_dice_bin = only_dice.binarize().invert()
        showImage(only_dice_bin)
        blobs_crop = only_dice_bin.findBlobs(minsize=3000, maxsize=6000)
        if blobs_crop is not None:
            blob.myColor = "yellow"
            logEntry(INFO, "Found Yellow Dice")
        else:
            blob.myColor = "white"
            logEntry(INFO, "Found White Dice")
        dices.append(blob)
    return dices


def indentifyDices(img):
    """Identify Dices in a pictures"""
    logEntry(INFO, "Identify Dices in a pictures")
    dices = []
    dices = findDicesWY(img,dices)
    dices = findDicesB(img,dices)
    dices = findDicesR(img,dices)
    dices = findDicesG(img,dices)
    return dices

def findPipsW(img,version=1):
    """Find the pips on a white Dice"""
    logEntry(INFO, "Find the pips on a white Dice")
    pips = 0

    showImage(img)

    img_edges = img.watershed()
    showImage(img_edges)


    img_circles = img_edges.floodFill((0,0),color=Color.WHITE).invert()
    showImage(img_circles)

    blobs = img_circles.findBlobs()
    if blobs is not None:
        logEntry(INFO, "White Dice - pips "+ str(len(blobs)))
        pips = len(blobs)
    return pips

def findPipsY(img,version=1):
    """Finding pips on Yellow Dices"""

    logEntry(INFO, "Finding pips on Yellow Dice")

    pips = 0

    showImage(img)

    white_dice = img.hueDistance(Color.YELLOW,minsaturation=80, minvalue=15)
    only_dice = img - white_dice

    only_dice_int = only_dice.binarize()
    showImage(only_dice_int)


    only_dice_fil = only_dice_int.floodFill((0,0),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((img.width-1,0),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((img.width-1,img.height-1),color=Color.BLACK)

    only_dice_fil = only_dice_fil.floodFill((0,img.height-1),color=Color.BLACK)

    showImage(only_dice_fil)

    total_img_pix = img.height * img.width

    blobs = only_dice_fil.findBlobs()
    if blobs is not None:
        counter = 0
        for blob in blobs:
            #print [counter, blob.perimeter(), blob.area(), blob.angle(), blob.circleDistance()]
            #print [blob.radius(), blob.isCircle(), blob.isRectangle()]
            #print [(blob.minRectWidth() / blob.minRectHeight()),blob.isSquare()]
            blob.isMySquare = blob.minRectWidth() / blob.minRectHeight()
            #print [blob.isMySquare]

        logEntry(INFO, "Yellow Dice - pips "+ str(len(blobs)))
        pips = len(blobs)
    else:
        darker_img = img / 1.5
        darker_img.filename = img.filename
        pips = findPipsYW(darker_img)
    return pips

def findPipsRGB(img,version=1):
    """Finding pips on Red, Green and Blue Dices"""

    logEntry(INFO, "Finding pips on Red, Green and Blue Dices")

    pips = 0

    #dl = DrawingLayer((img.width, img.height))

    white_dice = img.smooth('median',(5,5))

    if version == 1:
        # Version 1 Approach Normal
        histo = white_dice.toGray()
        histo_eq = histo.equalize()
        showImage(histo_eq)

        max = histo_eq.maxValue()
        min = histo_eq.minValue()

        stretch = white_dice.stretch(min,max-100)

        only_dice_int = stretch.binarize().invert().erode(2).dilate(2)

    blobs = only_dice_int.findBlobs(minsize=40)

    if blobs is not None:

        layer1 = DrawingLayer((img.width, img.height))
        counter = 0
        for blob in blobs:
            #print [counter, blob.perimeter(), blob.area(), blob.angle(), blob.circleDistance()]
            #print [blob.radius(), blob.isCircle(), blob.isRectangle()]
            #print [(blob.minRectWidth() / blob.minRectHeight()),blob.isSquare()]
            blob.isMySquare = blob.minRectWidth() / blob.minRectHeight()
            #print [blob.isMySquare]
            #blob.draw(layer=layer1, color=Color.RED)
            #layer1.text(str(counter), blob.coordinates())
            counter = counter + 1

        #img.addDrawingLayer(layer1)
        #img.applyLayers()

        showImage(img)

        total_img_pix = img.height * img.width

        large_blobs = blobs.filter([b.area() > (0.25 * total_img_pix) for b in blobs])
        if large_blobs is not None and len(large_blobs) > 0:
            #img.clearLayers()
            showImage(img)
            darker_img = img / 1.5
            darker_img.filename = img.filename
            pips = findPipsRGB(darker_img)
        else:
            circles = blobs.filter([b.perimeter() < 55 and  b.perimeter() > 30 and b.circleDistance() > 0.11 and (b.isMySquare >= 0.8 and b.isMySquare <= 1.1) for b in blobs])
            if circles is not None:
                if len(circles) > 0:
                    logEntry(INFO, "RGB dice. Found pip(s): "+ str(len(circles)))
                    pips = len(circles)
    else:
        logEntry(ERROR, "No blobs found")
    #img.clearLayers()
    return pips;

def ProcessingPicture():
    """Identifying dices in Picture"""
    logEntry(INFO, "Identifying dices in Picture")
    img = Image(input_image_file)
    showImage(img)

    diceFileNameStart = img.filename.split(".")[0]

    logEntry(INFO, "Dice filename start" + diceFileNameStart)

    dices = indentifyDices(img)
    if dices is not None and len(dices) > 0:
        cnt = 0
        for dice in dices:
            dice.pips = 0
            diceFileName = ""
            cnt = cnt + 1
            img_crop = img.crop(dice)
            if dice.myColor == "yellow":
                dice.pips = findPipsY(img_crop)
            elif dice.myColor == "white":
                dice.pips = findPipsW(img_crop)
            else:
                dice.pips = findPipsRGB(img_crop)
            logEntry(INFO, "Found Pips:" + str(dice.pips))
            diceFileName = diceFileNameStart + "-"+dice.myColor+"-"+str(dice.pips)+"-"+str(cnt)+".jpg"

            logEntry(INFO, "Dice File Name:" + my_images_path + "/" + diceFileName)

            img_crop.clearLayers()
            img_crop.save(my_images_path + "/" + diceFileName)

def main():
    """Start Main Program"""
    logEntry(INFO, "Start Main Program")

    logEntry(INFO, "Output path for images:" + my_images_path)

    ProcessingPicture()

main()