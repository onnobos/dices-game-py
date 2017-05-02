import os
import glob
import time
from SimpleCV import *
from SimpleCV.Color import Color
import time

vidcam = VirtualCamera("Service.mp4","video")

#maxframe = 280

#camImages = ImageSet()

#prv_img = Image()

#for counter in range(maxframe):
    #img = vidcam.getImage()
    ##print str(counter)
    ##if counter > 1:
        ##diff_img = img - prv_img
        ##diff_img.show()
        ##time.sleep(1)
    ##prv_img =  img
    ###img_crop = img.adaptiveScale((220,180))
    #camImages.append(img)

#camImages.show()
#result = camImages.average(mode="average")
#result.show()
#time.sleep(1)


#result.save("output.jpg")

#Next_img = vidcam.getImage()

#diff = Next_img - result
#diff.show()
#diff.save("output_diff.jpg")
#time.sleep(1)

img1 = vidcam.getImage()

img1.show()
time.sleep(1)

img2 = vidcam.getImage()

img2.show()
time.sleep(1)

motion = img2.findMotion(img1)
motion.draw()
img2.show()
time.sleep(1)
img2.save("motion.png")