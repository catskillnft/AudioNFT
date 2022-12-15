
import binascii
import os
import json
import csv
import uuid
import sys


workingDir = os.getcwd()
allItems = os.listdir(workingDir)
imageDir = 'SourceImage'
audioDir = 'SourceAudio'
outputDir = 'AudioNFT'
for item in allItems:
    if os.path.isdir(item):
        if imageDir in item:
            imageDir = os.path.join(workingDir,item)
        if audioDir in item:
            audioDir = os.path.join(workingDir,item)
        if outputDir in item:
            outputDir = os.path.join(workingDir,item)

audioFiles = os.listdir(audioDir)
for file in audioFiles:
    if 'Herr Doktor' in file:
        currentSong = file
        currentSong = currentSong.replace(" ","")
        currentSong = os.path.join(audioDir,currentSong)
        os.startfile(currentSong)



