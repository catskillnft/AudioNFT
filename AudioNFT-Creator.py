#!
#   'ChiaAudioNFTProtocol-'(ProtocolHex) = 43686961417564696F4E465450726F746F636F6C2D
#   'CANV002' (Chia AudioNFT Version) current v. 002

import binascii
import os
import json
import csv
import uuid
import sys

def getImageFiles():
    #scan image directory for supported image files
    #return list of valid files
    return

def getAudioFiles():
    #scan audio file directory for supported audio files
    #return list of valid files
    return

def getCollectionData():
    #reads a file called CollectionData.txt that contains user supplied information used to create AudioNFTs
    #returns dict with file info
    return

def getCsvFileData():
    #if image collection contains a CSV file with collection information this function is called
    #csv file must in the image directory
    #returns obj with csv data
    return

def createAudioNFTHexString():
    #takes file data, and creates the AudioNFT Hex String
    #appends AudioNFT Hex String to file metadata.
    return

def createMetadataFile():
    #creates a metadata file for individual AudioNFT
    #uses information from getCSVFileData and getCollectionData
    return

def createCSVFile():
    #creates a csv file for the new AudioNFT collection that includes all trait/variation info 
    return
    
def createPlayListFile():
    #creates a playlist file that contains information on all Audio file(s) in the AudioNFT
    return

def createAudioNFTFile():
    #combines and image file and audio file(s) into a single Audio NFT file
    #calls createMetadataFile(), createCSVFile()
    return


