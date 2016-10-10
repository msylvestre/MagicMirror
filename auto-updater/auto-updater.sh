#!/bin/bash
cd /home/pi/MagicMirror
git pull origin master
DISPLAY=:0 npm start

# To set the file as executable : $ chmod +x mm.sh