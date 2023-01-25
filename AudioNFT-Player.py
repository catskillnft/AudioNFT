##This script requires ffmpeg to be installed on your system
##if encountering errors download ffmpeg for your OS and place files into the main directory.


import binascii
import os
import json
import sys
import io
import pydub
from pydub.playback import play
from pathlib import Path

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

def getAudioNFTFile():
    #returns a list with an audioNFT file and it's correspoining metadata.json file
    #Player-Test folder should only have one AudioNFT and it's metadata.json for this to work.

    returnData = []
    currentDir = os.path.join(os.getcwd(), 'Player-Test')
    files = os.listdir(currentDir)
    for item in files:
        file = str(item).split(".")
        if file[1] == 'png':
            fileName = item
        if file[1] == 'mp3':
            audioTestFile = item
            
        else: metaFile = item

    returnData.append(fileName)
    returnData.append(metaFile)
    return returnData

def getAudioTrack(audioNFTInfo):
    audioNFTInfo = audioNFTInfo[2]
    audioTrackList = []
    returnData = []
    for item in audioNFTInfo['AudioNFT']['audio_info']:
        if 'track_number' in item:
            audioTrackList.append(item)
            
    if len(audioTrackList) > 1:
        print('\n\nThis AudioNFT contains multiple tracks.  Please select which track to play')
        choiceNumbers = len(audioTrackList)
        selectionNumber = 1
        for item in audioTrackList:
            print(str(selectionNumber) + " - Track: " + audioNFTInfo['AudioNFT']['audio_info'][item]['original_filename'])
            selectionNumber = selectionNumber + 1

        print(str(selectionNumber) + " - Return to main menu")
        choice = input("Select a valid option ")
        if (int(choice) > choiceNumbers):
            return menu()
        index = 1
        for i in range(choiceNumbers):
        
            if int(choice) == index:
            
                returnData.append(audioTrackList[i])
                returnData.append(audioNFTInfo['AudioNFT']['audio_info'][audioTrackList[i]])
                return returnData
            index = index + 1
    else:
        returnData.append(audioTrackList[0])
        returnData.append(audioNFTInfo['AudioNFT']['audio_info'][audioTrackList[0]])
        return returnData

def getAudioTrackOffset(audioNFTInfo, audioTrack):
    #returns the offset value for audioTrack.  
    #return value = imageFileSize + AudioNFTHexString fileSize + any preceding audio tracks fileSize
    fileInfo = audioTrack[1]
    
    audioNFTData = audioNFTInfo[2]
    audioNFTHexStringLength = audioNFTInfo[3]
    offset = int(audioNFTData['AudioNFT']['image_info']['file_size']) + int(audioNFTHexStringLength)
    
    returnData = offset + int(fileInfo['track_offset'])
    
    return returnData


def playAudioTrack(currentDir,audioNFTFile, audioNFTInfo,audioTrack,audioTrackOffset):
    audioNFTData = audioNFTInfo[2]
    samplePlayback = int(audioNFTData['AudioNFT']['audio_info']['sample_playback_length'])
    trackNumber = audioTrack[0]
    audioTrackInfo = audioTrack[1]

    audioFileSize = int(audioTrackInfo['file_size'])
    
    thisTrack = os.path.join(currentDir, audioNFTFile)
    with open(thisTrack, 'rb') as tT:
        tT.seek(audioTrackOffset)
        songFile = tT.read(audioFileSize)

    mp3Data = pydub.AudioSegment.from_file(io.BytesIO(songFile), format='mp3').set_frame_rate(40800)
    print('\n\n\nArtist: ' + audioTrackInfo['artist'])
    print('Audio Track : ' + audioTrackInfo['title'])
    play(mp3Data)

def playAudioNFT():

    currentDir = os.path.join(os.getcwd(), 'Player-Test')
    audioNFTFiles = getAudioNFTFile()

    audioNFTFile = audioNFTFiles[0]
    metaFile = audioNFTFiles[1]

    metadataFile = os.path.join(currentDir, metaFile)
    metadataFile = open(metadataFile)
    metadataFile = json.load(metadataFile)
    audioNFTHexString = metadataFile['data']['AudioNFT']
    audioNFTInfo = convertAudioNFTHexString(audioNFTHexString)
    
    
    

    audioTrack = getAudioTrack(audioNFTInfo)
    audioTrackOffset = getAudioTrackOffset(audioNFTInfo, audioTrack)
    playAudioTrack(currentDir, audioNFTFile,audioNFTInfo, audioTrack, audioTrackOffset)
    
    




    return


def menu():
    options = ['1','2']
    print("\nWelcome to CatskillNFTs AudioNFT Player")
    print('\n Plays tracks embedded in AudioNFT file found in Player-Test Folder\n\n')
    
    print("Please select from one of the following options. ")
    print("1- Play AudioNFT")
    print("2- Exit CatskillNFTs AudioNFT Creation Tool")
    choice = input("Select a valid option ")
    choice = str(choice)
    if choice in options:
        if choice == '1':
            
            playAudioNFT()
            return menu()

        if choice == '2':
            print("Thank you for using CatskillNFTs AudioNFT creation tool")
            sys.exit
    else:
        print("Invalid option selected. Please Try again\n\n")
        return(menu())





menu()