#!/bin/sh
# Installs needed dependencies on Fedora. Tested on version 36

sudo dnf install python3-pip
pip install tensorflow
pip install mediapipe
pip install numpy
sudo dnf install python3-tkinter
sudo dnf install python3-pillow-tk python3-pillow
