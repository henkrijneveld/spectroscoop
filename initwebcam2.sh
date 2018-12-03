 #!/bin/bash
 echo "Run as sudo!"

 fswebcam -d /dev/video2 -s "Brightness"=0
 fswebcam -d /dev/video2 -s "Saturation"=0
 fswebcam -d /dev/video2 -s "Gain"=2
 fswebcam -d /dev/video2 --list-controls
