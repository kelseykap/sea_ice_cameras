import cv2 as cv2
import numpy as np
import os
import TIS
import time
from collections import namedtuple

# needed packages:
# pyhton-opencv
# pyhton-gst-1.0
# tiscamera

class CustomData:
        ''' Example class for user data passed to the on new image callback function
            It is used for an image counter only. Also for a busy flag, so the callback
            is not called, while a previons callback call is still active.
        '''
        def __init__(self, ):
                self.imagecounter = 0; ## TODO: add timestamp here
                self.busy = False;

def on_new_image(tis, userdata):
        '''
        Callback function, which will be called by the TIS class
        :param tis: the camera TIS class, that calls this callback
        :param userdata: This is a class with user data, filled by this call.
        :return:
        '''
        # Avoid being called, while the callback is busy
        if userdata.busy is True:
                return

        userdata.busy = True
        image = tis.Get_image() 

        # Create a file name with a running number:
        userdata.imagecounter += 1;
        filename = "./image{:04}.jpg".format(userdata.imagecounter) ## TODO: add timestamp
        
        # Save the image as jpeg
        cv2.imwrite(filename, image)
        userdata.busy = False


# Open camera, set video format, framerate and determine, whether the sink is color or bw
# Parameters: camera serialnumber, width, height, framerate (numerator only), color
# If color is False, then monochrome / bw format is in memory. If color is True, then RGB32
# colorformat is in memory. The last True lets the TIS class open a window for displaying the 
# live video.

Tis = TIS.TIS("44814140", 640, 480, 15, False, True)

# Create an instance of the CustomData class
CD = CustomData()
CD.busy = True # Avoid, that we handle image, while we are in the pipeline start phase

# Set the callback function
Tis.Set_Image_Callback(on_new_image, CD)

Tis.Set_Property("Trigger Mode", "Off") # turn off trigger in order to start pipeline

# Start the pipeline
Tis.Start_pipeline()
Tis.Set_Property("Trigger Mode", "On")  # enable trigger

# Wait a moment, for the camera accepting trigger mode
time.sleep(0.1) 

CD.busy = False  # Now the callback function does something on a trigger

# loop until keyboard input quit
while True:
        key = raw_input("q : quit\nPlease enter:")
        if key == "q":
                break

Tis.Stop_pipeline()
print('Program end')
