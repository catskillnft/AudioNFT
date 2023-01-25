import binascii
import os
import json
import sys


def getFolders():
    workingDir = os.getcwd()
    sourceDir = os.path.join(workingDir,'AudioNFT-Files')
    audioOutputDir = os.path.join(workingDir,'Extracted-Audio')
    imageOutputDir = os.path.join(workingDir,'Extracted-Image')

    #returnData[0] = workingDir
    #returnData[1] = sourceDir
    #returnData[2] = imageOutputDir
    #returnData[3] = audioOutputDir
    
    returnData = [workingDir,sourceDir,imageOutputDir,audioOutputDir]
    for item in returnData:
        if not os.path.exists(item):
            os.mkdir(item)
    return returnData

def getAudioNFTFiles(sourceDir):
    validFileTypes = ['png', 'jpg', 'jpeg', 'gif']
    allFiles = os.listdir(sourceDir)
    audioNFTFiles =[]
    jsonFiles = []
    audioNFTPairs = {}

    for item in allFiles:
        thisFile = str(item).split(".")
        if thisFile[1] in validFileTypes:
            audioNFTFiles.append(item)
        if thisFile[1] == 'json':
            jsonFiles.append(item)

    for item in audioNFTFiles:
        thisItem = str(item).split("-")
        for file in jsonFiles:
            thisFile = str(file).split('#')
            thisFile = thisFile[1]
            thisFile = thisFile.split(".")
            if thisFile[0] == thisItem[0]:
                audioNFTPairs.update({str(item):str(file)})

    return(audioNFTPairs)

def convertAudioNFTHexString(audioNFTHexString):
    
    #takes an AudioNFTHexString and returns the AudioNFTIDString , the version Number, a dict with the fileInfoJson, size of AudioNFTHexString in bytes
    returnData = []
    size = sys.getsizeof(audioNFTHexString)
    decodeString = binascii.unhexlify(audioNFTHexString)
    decodeString = decodeString.decode()
    decodeString = str(decodeString).split("@*-*@")
    returnData.append(decodeString[0])
    returnData.append(decodeString[1])

    decodeString = json.loads(decodeString[2])
    returnData.append(decodeString)
    returnData.append(size)

    return returnData

def extractImage(folderInfo, sourceFiles):
    sourceDir = folderInfo[1]
    imageOutputDir = folderInfo[2]

    for item in sourceFiles:
        metadataFile = os.path.join(sourceDir, sourceFiles[item])
        metadataFile = open(metadataFile)
        metadataFile = json.load(metadataFile)
        audioNFTHexString = metadataFile['data']['AudioNFT']
        audioNFTInfo = convertAudioNFTHexString(audioNFTHexString)
        
        fileInfo = audioNFTInfo[2]
        version = audioNFTInfo[1]
        if (fileInfo['AudioNFT']['info']['extract_image'] == 'True') and (version == '0.0.2'):
            fileName = fileInfo['AudioNFT']['image_info']['file_name']
            fileSize = fileInfo['AudioNFT']['image_info']['file_size']
            fileName = os.path.join(imageOutputDir, fileName)
            if not os.path.exists(fileName):
                sourceFile = os.path.join(sourceDir, item)
                with open(sourceFile, 'rb') as sF, open (fileName, 'wb') as iF:
                    newFile = sF.read(fileSize)
                    iF.write(newFile)
            else:
                print('image file ' + str(fileName) + ' already exists, no need to extract')
             
        else:
            print('Unable to extract Image file from this AudioNFT.  Wrong Version, or disallowed by creator')
        
    return print('AudioNFT image extraction complete')

def extractAudio(folderInfo, sourceFiles):
    sourceDir = folderInfo[1]
    audioOutputDir = folderInfo[3]

    for item in sourceFiles:
        metadataFile = os.path.join(sourceDir, sourceFiles[item])
        metadataFile = open(metadataFile)
        metadataFile = json.load(metadataFile)
        audioNFTHexString = metadataFile['data']['AudioNFT']
        audioNFTInfo = convertAudioNFTHexString(audioNFTHexString)
        
        fileInfo = audioNFTInfo[2]
        version = audioNFTInfo[1]
        audioNFTHexStringSize = audioNFTInfo[3]
        imageSize = fileInfo['AudioNFT']['image_info']['file_size']
        offset = int(audioNFTHexStringSize) + int(imageSize) 
        if (fileInfo['AudioNFT']['info']['extract_audio'] == 'True') and (version == '0.0.2'):
            for track in fileInfo['AudioNFT']['audio_info']:
                if 'track_number' in str(track):
                    audioFileName = fileInfo['AudioNFT']['audio_info'][track]['original_filename']
                    audioFileSize = fileInfo['AudioNFT']['audio_info'][track]['file_size']
                    audioFileName = os.path.join(audioOutputDir, audioFileName)
                    if not os.path.exists(audioFileName):
                        sourceFile = os.path.join(sourceDir, item)
                        with open (sourceFile, 'rb') as sF, open (audioFileName, 'wb') as aF:
                            sF.seek(offset)
                            aF.write(sF.read(audioFileSize))
                    offset = offset + audioFileSize
            
        else:
            print('Unable to extract Audio file(s) from this AudioNFT.  Wrong Version, or disallowed by creator')
    return print('AudioNFT audio extraction complete')


def extract(choice):
    folderInfo = getFolders()
    sourceDir = folderInfo[1]
    imageOutputDir = folderInfo[2]
    audioOutPutDir = folderInfo[3]

    sourceFiles = getAudioNFTFiles(sourceDir)

    if choice == '1':
        extractImage(folderInfo,sourceFiles)

    if choice == '2':
        extractAudio(folderInfo,sourceFiles)

    

    
def menu():
    options = ['1','2','3']
    print("\nWelcome to CatskillNFTs AudioNFT File Extraction Tool")
    print("This script will Extact Image and Audio files from your local AudioNFT directory\n\n")
   
    
    print("Please select from one of the following options. ")
    print("1- Extract Image File")
    print("2- Extract Audio File(s)")
    print("3- Exit CatskillNFTs AudioNFT File Extraction Tool")
    choice = input("Select a valid option ")
    choice = str(choice)
    if choice in options:
        if choice == '1':
            print('Extracting Image Files\n')
            extract(choice)
            return menu()

        if choice == '2':
            print("Extracting Audio File(s)\n")
            extract(choice)
            return menu()

        if choice == '3':
            print("Thank you for using CatskillNFTs AudioNFT creation tool")
            sys.exit
    else:
        print("Invalid option selected. Please Try again\n\n")
        return(menu())





menu()