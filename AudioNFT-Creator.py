#!
#   'ChiaAudioNFTProtocol-'(ProtocolHex) = 43686961417564696F4E465450726F746F636F6C2D
#   'CANV002' (Chia AudioNFT Version) current v. 002
#   Currently being developed in a Win11 environment. Possible file/folder/os issues on other systems.

import binascii
import os
import json
import csv
import uuid
import sys

def getImageFiles():
    #scan image directory for supported image files and valid CSV files
    #return list of valid files

    validFileTypes = ['csv', 'png', 'jpg', 'jpeg', 'gif']
    csvFileList = []
    imageFilesList = []
    
    fileList = os.listdir(imageFilesDir)
    for file in fileList:
        fileName = str(file).split(".")
        if fileName[1] in validFileTypes:
            
            if fileName[1] == 'csv':
                if fileName[0] == 'metadata':
                    csvFileList.append(file)
                else:
                    print('Error: A CSV file was found, but it was not named metadata.csv.  If you wish to use that file, please rename it to metadata.csv')
            else:
                imageFilesList.append(file)

    if len(csvFileList) > 1:
        return print('Error: more than one CSV file located in SouceImageFiles folder.  Only one CSV file is allowed')
    returnData = [imageFilesList, csvFileList]
    return returnData

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

def createAudioNFTHexString(hexIDString, version):
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

workingDir = os.getcwd()
imageFilesDir = (workingDir + "/SourceImageFiles/")
audioFilesDir = (workingDir + "/SourceAudioFiles/")
destinationDir = (workingDir +"/AudioNFTFiles/")

hexIDString = 'ChiaAudioNFTProtocol-'
version = 'CANV002'

imageFilesList = getImageFiles()
print(imageFilesList)