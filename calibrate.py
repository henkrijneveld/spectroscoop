# fswebcam en  uvcdynctl
# met fswebcam vooral de brightness lijkt effect te hebben
# instelling in fswebcam:
# (output voor sudo fswebcam -d /dev/video3 --list-controls)
# sudo fswebcam -d /dev/video1 -s "Brightness"=-150
#
#Available Controls        Current Value   Range
#------------------        -------------   -----
#Brightness                -150 (20%)      -255 - 255
#Contrast                  10 (33%)        0 - 30
#Saturation                20 (15%)        0 - 127
#Hue                       0 (50%)         -180 - 180
#White Balance Temperature, Auto False           True | False
#Gamma                     100 (34%)       20 - 250
#Gain                      4               0 - 10
#Power Line Frequency      50 Hz           Disabled | 50 Hz | 60 Hz
#White Balance Temperature 4000 (32%)      2800 - 6500
#Sharpness                 60 (55%)        0 - 108
#Backlight Compensation    0               0 - 2
#Error reading value of menu item 0 for control 'Exposure, Auto'
#VIDIOC_QUERYMENU: Invalid argument
#Exposure (Absolute)       333 (5%)        39 - 5000
#Exposure, Auto Priority   False           True | False
#Focus (absolute)          0 (0%)          0 - 831
#Adjusting resolution from 384x288 to 320x240.


import numpy as np
import cv2
import time
from configfile import ConfigData

cap = cv2.VideoCapture(1)

print("Current resolution:")
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#webcam on asus only does 1280x720 as heigher resolution
print(cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592))
print(cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944))

print("New resolution:")
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("FPS:")
print(cap.get(cv2.CAP_PROP_FPS))

print("Brightness:")
print(cap.get(cv2.CAP_PROP_BRIGHTNESS))
print(cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5))
time.sleep(1)
print(cap.get(cv2.CAP_PROP_BRIGHTNESS))

print("Contrast:")
print(cap.get(cv2.CAP_PROP_CONTRAST))
print(cap.set(cv2.CAP_PROP_CONTRAST, 0.3))
print(cap.get(cv2.CAP_PROP_CONTRAST))

print("Convert RGB:")
print(cap.get(cv2.CAP_PROP_CONVERT_RGB))
#print(cap.set(cv2.CAP_PROP_CONVERT_RGB, 0.5))
#time.sleep(1)
#print(cap.get(cv2.CAP_PROP_CONVERT_RGB))

print("Gain:")
print(cap.get(cv2.CAP_PROP_GAIN))

print("Exposure:")
print(cap.get(cv2.CAP_PROP_EXPOSURE))
#print(cap.set(cv2.CAP_PROP_EXPOSURE, 1.0))
#time.sleep(1)
#print(cap.get(cv2.CAP_PROP_EXPOSURE))


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
 #   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
 #   cv2.imshow('frame',gray)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
while cv2.waitKey(1) & 0xFF != ord('s'):
    pass

cap.release()
cv2.destroyAllWindows()

# make the configuration file
c = ConfigData()
c.analyze(frame)
c.write()

crop_frame = frame[c.bottomh:c.toph, c.bottomw:c.topw, ]

cv2.imshow("cropped", crop_frame)
cv2.waitKey(0)

cv2.imwrite("test.png", crop_frame)



# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)