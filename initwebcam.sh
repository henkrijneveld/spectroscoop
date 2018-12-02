 #!/bin/bash
 echo "Run as sudo!"

 fswebcam -d /dev/video1 -s "Brightness"=0
 fswebcam -d /dev/video1 -s "Saturation"=0
 fswebcam -d /dev/video1 -s "Gain"=2
 fswebcam -d /dev/video1 --list-controls
