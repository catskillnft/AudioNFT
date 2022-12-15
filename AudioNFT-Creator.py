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
import mutagen

def getImageFiles(folderInfo):
    #scan image directory for supported image files and valid CSV files
    #return list of valid files
    imageFilesDir = folderInfo[1]
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
    
    #returndata[0] image files list
    #returndata[1] metadata.csv file
    returnData = [imageFilesList, csvFileList]
    return returnData

def getAudioFiles(folderInfo):
    #scan audio file directory for supported audio files
    #return list of valid files
    audioFilesDir = folderInfo[2]
    validFileTypes = ['mp3','ogg','wav']
    audioFilesList = []
    fileList = os.listdir(audioFilesDir)
    for file in fileList:
        fileName = file.split(".")
        if fileName[1] in validFileTypes:
            audioFilesList.append(file)
    return audioFilesList

def getCollectionData(folderInfo):
    #reads a file called CollectionData.txt that contains user supplied information used to create AudioNFTs
    #returns dict with file info
    workingDir = folderInfo[0]
    collectionDataFile = os.path.join(workingDir, 'CollectionData.txt')
    if os.path.exists(collectionDataFile):  

        with open(collectionDataFile, 'r') as c:
            collectionData = json.load(c)
            
        return collectionData
    else:
        return print("ERROR: CollectionData.txt does not exist. Please place file in AudioNFT-Creator main folder")

def getCsvMetaDataFileInfo(folderInfo):
    #current functionality is using delim = ','
    #future functionality should use delim = ';' with the following structure:
   

    #Headers = File, Name, Description, trait_value, trait_value, trait_value, etc.. 
    #NFTInfo = filename, name of nft, description of nft, value, value, value, etc..

    #acceptable csv metadata file format is planned to follow requirements for use in mintgarden studio.

    #if image collection contains a CSV file with collection information this function is called
    #csv file must be in the image directory
    #returns obj with csv data
    metadataInfo = []
    workingDir = folderInfo[0]
    csvMetadataFile = os.path.join(workingDir + 'metadata.csv')
    
    if os.path.exists(csvMetadataFile):
        with open(csvMetadataFile, 'r') as c:
            csvFile = csv.reader(c)
            for row in csvFile:
                metadataInfo.append(row)
        
            headers = metadataInfo[0]
            metadataInfo.pop(0)
    

        if len(metadataInfo < 1):
            print('ERROR: metadata.csv file has no information in it')
            returnData = []
            return returnData

        #returnData  headers[0]
        #returnData  files metadata[1]
        returnData = [headers, metadataInfo]
        return returnData

def createAudioNFTHexString(hexIDString, version):
    #takes file data, and creates the AudioNFT Hex String
    #appends AudioNFT Hex String to file metadata.

    hexIDString = 'ChiaAudioNFTProtocol-'
    version = 'CANV002'

    return

def createMetadataFile(folderInfo,audioFile):

    #creates a metadata file for individual AudioNFT
    #uses information from getCSVFileData and getCollectionData
    return

def createCSVFile(folderInfo):
    #creates a csv file for the new AudioNFT collection that includes all trait/variation info 
    return
    
def createPlaylistFile(audioFiles):
    #creates a playlist file that contains information on all Audio file(s) in the AudioNFT
    audioFileInfo = {}
    #for each audio file, getID3Info()
    #construct playlist with ID3 data
    #create playlist for all files, and return ID3 data for each audio file
    #will need ID3 tag length in bytes, and for each audio will need total song length in seconds. 
    returnData = "placeholder for playlist file info"
    return returnData

def getId3Info(audioFile):

    returnData = "placeholder for id3 Data"
    return returnData

def getFolders():
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

    #returnData[0] = workingDir
    #returnData[1] = imageDir
    #returnData[2] = audioDir
    #returnData[3] = outputDir
    returnData = [workingDir,imageDir, audioDir, outputDir]
    return returnData    
    
def createAudioNFTFiles():
    #combines and image file and audio file(s) into a single Audio NFT file
    #calls createMetadataFile(), createCSVFile()
    folderInfo = getFolders()
    workingDir = folderInfo[0]
    imageDir = folderInfo[1]
    audioDir = folderInfo[2]
    outputDir = folderInfo[3]
    imageFiles = getImageFiles(folderInfo)
    audioFiles = getAudioFiles(folderInfo)
    collectionData = getCollectionData(folderInfo)
    audioFilesInfo = {}
    
    for file in audioFiles:
        type = str(file).split(".")
        type = type[1]
        if type == 'mp3':
            fileName = os.path.join(audioDir,file)
            print(mutagen.Tags())
    
    print(audioFiles)


    return

def menu():
    options = ['1','2']
    print("Welcome to CatskillNFTs AudioNFTs Creation Tool")
    print("Read the ReadME.txt file found in your AudioNFT install directory.")
    print("Note: The AudioNFTFiles folder must be empty prior to creating a new collection.\n\n")
    
    print("Please select from one of the following options. ")
    print("1- create AudioNFTs")
    print("2- Exit CatskillNFTs AudioNFT Creation Tool")
    choice = input("Select a valid option ")
    choice = str(choice)
    if choice in options:
        if choice == '1':
            print('creating AudioNFT Files\n')
            createAudioNFTFiles()
            return menu()

        if choice == '2':
            print("Thank you for using CatskillNFTs AudioNFT creation tool")
            sys.exit
    else:
        print("Invalid option selected. Please Try again\n\n")
        return(menu())





menu()
