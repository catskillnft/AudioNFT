#   'ChiaAudioNFTProtocol@*-*@'(ProtocolHex) = 43686961417564696f4e465450726f746f636f6c402a2d2a40
#   'version 0.0.2' (Chia AudioNFT Version) current v. 002
#   Currently being developed in a Win11 environment. Possible file/folder/os issues on other systems.

import binascii
import os
import json
import csv
import uuid
import sys
import mutagen
#import eyed3
#import ffmpeg


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
                    print('Error: A CSV file was found, but it was not named metadata.csv.  If you wish to use that file, please rename it to metadata.csv\nerror in getImageFiles\n')
            else:
                imageFilesList.append(file)

    if len(csvFileList) > 1:
        return print('Error: more than one CSV file located in SouceImageFiles folder.  Only one CSV file is allowed\nerror in getImageFiles\n')
    
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
        return print("ERROR: CollectionData.txt does not exist. Please place file in AudioNFT-Creator main folder\nerror in getCollectionData\n")

def getCsvMetaDataFileInfo(folderInfo):
    #current functionality is using delim = ';'
    
   

    #Headers = File; Name; Description; trait_value; trait_value; trait_value; etc.. 
    #NFTInfo = filename; name of nft; description of nft; value; value; value, etc..

    #acceptable csv metadata file format follows requirements for use in mintgarden studio.

    #if image collection contains a CSV file with collection information this function is called
    #csv file must be in the image directory
    #returns obj with csv data
    metadataInfo = []
    imageDir = folderInfo[1]
    
    csvMetadataFile = os.path.join(imageDir, 'metadata.csv')
    
    if os.path.exists(csvMetadataFile):
        with open(csvMetadataFile, 'r') as c:
            csvFile = csv.reader(c, delimiter= ';')
            for row in csvFile:
                metadataInfo.append(row)
        
            headers = metadataInfo[0]
            metadataInfo.pop(0)
    

        if len(metadataInfo) < 1:
            print('ERROR: metadata.csv file has no information in it\nerror in getCsvMetaDataFileInfo\n')
            returnData = []
            return returnData

        #returnData  headers[0]
        #returnData  files metadata[1]
        returnData = [headers, metadataInfo]
        return returnData

    else:
        returnData = [None,None]
        return returnData

def createAudioNFTHexString(collectionData,imageInfo,audioTrackInfo):
    #takes file data, and creates the AudioNFT Hex String
    #AudioNFT Hex String is list with hexIDString, version.  Then 3 dicts converted to json strings, combined into a single json string. 
    #Dict1:keys- AudioNFTInfo: extract_image, extract_audio  --taken from collectionData.txt
    #Dict2:keys- image_info: size, file, name, description  --taken from metadata.csv when present. otherwise will only include size and file
    #Dict3:keys- audio_info: number_of_tracks, sample_playback_length, track_number #   -- track_number #, will contain a unique value # for each included audio track.
    #each audio track will have it's own info stored in a dict json string
    #Dict:keys- track_number #:original_fileNname, artist, title, id3_size, file_size, length

    #AudioNFTHexString: hexIDString, version,{AudioNFT:{AudioNFT_info: extract_image, extract_audio}{image_info:{size,file,name,description}{audio_info:{number_of_tracks, sample_playback_length, track_number #,...}}}
    
    #returns list with : AudioNFT Hex String in plain text, AudioNFTHexString encoded into hex, and hexIDString encoded into hex.
    hexIDString = 'ChiaAudioNFTProtocol@*-*@'
    version = '0.0.2@*-*@'
    returnData = []
    audioNFTInfo = {}
    audioNFTInfoDict = {}
    imageInfoDict = {}
    imageInfoTempDict = {}
    audioInfoDict = {}
    allInfoDict = {}
    audioNFTHexDict = {}

    audioNFTInfo.update({"extract_image": collectionData["collection"]["extract_image"]})
    audioNFTInfo.update({"extract_audio": collectionData["collection"]["extract_audio"]})

    
 
    imageInfoTempDict.update({"size": imageInfo["size"]})
    imageInfoTempDict.update({"file": imageInfo['file']})
    imageInfoTempDict.update({"name": imageInfo['name']})
    imageInfoTempDict.update({"description": imageInfo['description']})

    
    allInfoDict.update({"AudioNFT_info": audioNFTInfo})
    allInfoDict.update({"image_info": imageInfoTempDict})
    allInfoDict.update({"audio_info": audioTrackInfo})
    audioNFTHexDict.update({"AudioNFT": allInfoDict})
    audioNFTHexDict = json.dumps(audioNFTHexDict)

    audioNFTHexString = hexIDString + version + audioNFTHexDict + '@*-*@'
    returnData.append(audioNFTHexString)

    audioNFTHexString = audioNFTHexString.encode()
    audioNFTHexString = binascii.hexlify(audioNFTHexString)
    audioNFTHexString = audioNFTHexString.decode()

    returnData.append(audioNFTHexString)

    hexIDString = hexIDString.encode()
    hexIDString = binascii.hexlify(hexIDString)
    hexIDString = hexIDString.decode()

    returnData.append(hexIDString)

    return returnData

def createMetadataFile(folderInfo,collectionData, fileInfo, uuidNumber, audioNFTHexString):
    #creates metadatafiles for AudioNFT file
    outputDir = folderInfo[3]
    collectionMetadata = {}

  
    
    newMetadataFile = {'format':'CHIP-0007'}
    newMetadataFile.update({'name':fileInfo['name']})
    newMetadataFile.update({'description':fileInfo['description']})
    newMetadataFile.update({'sensitive_data':collectionData['collection']['NSFW']})
    
    seriesNumber = str(fileInfo['name']).split("#", maxsplit=1)
    seriesNumber = int(seriesNumber[1])
    newMetadataFile.update({'series_number':seriesNumber})
    newMetadataFile.update({'series_total':collectionData['collection']['series_total']})

    collectionMetadata.update({'name':collectionData['collection']['name']})
    collectionMetadata.update({'id': uuidNumber})

    collectionAttributes = []
    
    collectionDescription = {'type':'description', 'value':collectionData['collection']['description']}
    collectionIcon = {'type':'icon', 'value':collectionData['collection']['icon']}
    collectionBanner = {'type':'banner', 'value':collectionData['collection']['banner']}
    collectionAttributes.append(collectionDescription)
    collectionAttributes.append(collectionIcon)
    collectionAttributes.append(collectionBanner)

    for item in collectionData['socials']:
        thisItem = {'type':item, 'value':collectionData['socials'][item]}
        collectionAttributes.append(thisItem)
    
    newMetadataFile.update({'collection':collectionAttributes})
    
    imageAttributes = []

    del fileInfo['file']
    del fileInfo['name']
    del fileInfo['description']

    for item in fileInfo:
        thisItem = {'trait_type':item, 'value':fileInfo[item]}
        imageAttributes.append(thisItem)
    
    newMetadataFile.update({'attributes':imageAttributes})

    dataAttributes = {'AudioNFT':audioNFTHexString[1]}
    newMetadataFile.update({'data':dataAttributes})
    
    newMetadataFile = json.dumps(newMetadataFile, indent =4)
    
    metaFileName = audioNFTHexString[2] + " " + str(seriesNumber) + '.json'
    metaFileName = os.path.join(outputDir,metaFileName)
    #open(metaFileName, 'x',  encoding='utf-8')
    with open(metaFileName, 'w',encoding='utf-8') as f:
        f.write(newMetadataFile)



    return True

def createAudioNFTCSVFile(folderInfo,imageCSVMetadataInfo,audioNFTHexString,collectionData,newFileName):
    #creates a csv file for the new AudioNFT collection that includes all trait/variation info 
    #adds a line to existing metadata.csv file for AudioNFT collection
    outputDir = folderInfo[3]
    audioNFTCSVFile = os.path.join(outputDir, 'metadata.csv')

    audioNFTHexStringInfo = audioNFTHexString[0].split("@*-*@")
    audioNFTHexStringInfo = json.loads(audioNFTHexStringInfo[2])
    audioNFTHexInfo = audioNFTHexStringInfo["AudioNFT"]["AudioNFT_info"]
    imageHexInfo = audioNFTHexStringInfo["AudioNFT"]["image_info"]
    audioHexInfo= audioNFTHexStringInfo["AudioNFT"]["audio_info"]
    imageTraits = imageCSVMetadataInfo[1]
    
    newHeaders= ['file','name','description']
    imageAttributesHeaders = ["Image Artist","Image Name"]
    if collectionData["image"]["use_file_description"] != "True":
        imageAttributesHeaders.append("Image Description")
    
    audioAttributesHeaders = ["Number Of Tracks"]
    
    for track in audioHexInfo:
        if "track_number" in str(track):
            trackNumber = str(track).split()
            trackNumber = "Track Number " + str(trackNumber[1])
            audioAttributesHeaders.append(trackNumber)

    if (imageCSVMetadataInfo[0] != None) and (imageCSVMetadataInfo[1] != None):
       
        headers = imageCSVMetadataInfo[0]
        
        #print(headers)
        for item in headers[3:]:
            
            imageAttributesHeaders.append("Image Trait: " + str(item))

    for item in imageAttributesHeaders:
        newHeaders.append(item)
    
    for item in audioAttributesHeaders:
        newHeaders.append(item)

    if not os.path.exists(audioNFTCSVFile):
        open(audioNFTCSVFile, 'x', encoding='utf-8')
        with open(audioNFTCSVFile, 'w',newline='') as csvFile:
            csvWriter = csv.writer(csvFile,delimiter=";")
            csvWriter.writerow(newHeaders)
        print('AudioNFT .csv file with headers created')
    return newHeaders

    

    


def addRowToAudioNFTCSVFile(folderInfo,imageCSVMetadataInfo,audioNFTHexString,collectionData,newFileName,fileNumber):
    #adds a row to a .csv file that contains information about this AudioNFT file.
    # if metadata.csv does not exist, the file will be created. 
    # the header row is returned from createAudioNFTCSVFile
    outputDir = folderInfo[3]
    audioNFTCSVFile = os.path.join(outputDir, 'metadata.csv')
    newFile = os.path.join(outputDir, newFileName)
    
    rowImageInfo = []
    rowAudioInfo = []
    rowGenericInfo = []
    allRowInfo = []
    newRowDict = {}
    rowAudioTrackInfo = {}
    newRow = []
    audioNFTName = collectionData["collection"]["name"]
    
    audioNFTHexStringInfo = audioNFTHexString[0].split("@*-*@")
    audioNFTHexStringInfo = json.loads(audioNFTHexStringInfo[2])
    audioNFTHexInfo = audioNFTHexStringInfo["AudioNFT"]["AudioNFT_info"]
    imageHexInfo = audioNFTHexStringInfo["AudioNFT"]["image_info"]
    audioHexInfo= audioNFTHexStringInfo["AudioNFT"]["audio_info"]
    imageTraits = imageCSVMetadataInfo[1]
    originalImageName = imageHexInfo["file"]
    rowGenericInfo.append(str(newFileName))
    rowGenericInfo.append(str(collectionData["collection"]["name"]) + " #" + str(fileNumber))
    if collectionData["image"]["use_file_description"] != "True":
        rowGenericInfo.append(str(collectionData["collection"]["description"]))
    else:
        rowGenericInfo.append(str(imageHexInfo["description"]))
    
    rowImageInfo.append(collectionData["image"]["image_artist"])

    rowImageInfo.append(imageHexInfo["name"])
    if collectionData["image"]["use_file_description"] != "True":
        rowImageInfo.append(imageHexInfo["description"])
    
    if imageCSVMetadataInfo[1] != None:
        for row in imageCSVMetadataInfo[1]:
          
            if row[0] == originalImageName:
                for trait in row[3:]:
                    rowImageInfo.append(trait)
    rowAudioInfo.append(audioHexInfo["number_of_tracks"])
    for item in audioHexInfo:
        if "track_number" in str(item):
            rowAudioInfo.append(audioHexInfo[item]["original_filename"])

    headers = createAudioNFTCSVFile(folderInfo,imageCSVMetadataInfo,audioNFTHexString,collectionData,newFileName)
    for item in rowGenericInfo:
        allRowInfo.append(item)
    for item in rowImageInfo:
        allRowInfo.append(item)
    for item in rowAudioInfo:
        allRowInfo.append(item)

    with open(audioNFTCSVFile, 'a',newline='') as csvFile:
        csvWriter = csv.writer(csvFile,delimiter=";")
        csvWriter.writerow(allRowInfo)
    
    returnData = dict(zip(headers,allRowInfo))
    
    return returnData
    
def createPlaylistFile(audioFiles):
    #creates a playlist file that contains information on all Audio file(s) in the AudioNFT
    audioFileInfo = {}
    #for each audio file, getID3Info()
    #construct playlist with ID3 data
    #create playlist for all files, and return ID3 data for each audio file
    #will need ID3 tag length in bytes, and for each audio will need total song length in seconds. 
    returnData = "placeholder for playlist file info"
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

def getAudioTrackInfo(audioDir,audioFiles,collectionData):
    #creates dict with audioTrack info. 
    #returns dict with totalNumber of tracks, sample_playback_length, and a dict for each track that contains track specific info 
    # [Total number of Tracks, [TrackNumber, Original File Name,Artist Name, Song Title, ID3 Tag y/n, ID3 Tag Size in bytes, Total File Size in bytes, Track Length in seconds]]

    #returnData formatted as list. Ex: [1,[1,'1 DJ CatskillNFT - Speedy-go-go.mp3','DJ CaktskillNFT','Speedy-gogo', 23454,56234526,220]]
    returnData = {}
    filesHaveTrackNumber = collectionData["audio"]["track_numbers_labeled"]
    playbackLength = collectionData["audio"]["sample_playback_length"]
    totalNumberOfTracks = len(audioFiles)
    returnData.update({"number_of_tracks": totalNumberOfTracks})
    returnData.update({"sample_playback_length": playbackLength})
    
    trackNumber = 1
    for track in audioFiles:
        thisTrackInfo = {}
        
        thisTrackNumberArtistSong = str(track)
        
        thisTrackNumberArtistSong = thisTrackNumberArtistSong.split(maxsplit=1)
        
        if (str(thisTrackNumberArtistSong[0]).isdigit() == True) and (str(filesHaveTrackNumber) == "True"):
            thisTrackNumber = int(thisTrackNumberArtistSong[0])
            
            thisTrackArtistSong = thisTrackNumberArtistSong[1].split(" - ")
 
            thisTrackArtist = thisTrackArtistSong[0]
            thisTrackSong = thisTrackArtistSong[1]
            thisTrackSong = thisTrackSong.split(".")
            thisTrackSong = thisTrackSong[0]
            

        else:
            if (str(thisTrackNumberArtistSong[0]).isdigit() == False) and (str(filesHaveTrackNumber) == "True"):
                print('Error: A file has an invalid track number. CollectionData has indicated tracks should have track numbers assigned. Unexpected/incorrect track information may occur ')
                print('error in getAudioTrackInfo')
                thisTrackNumber = int(trackNumber) * int(100)
                thisTrackArtistSong = str(track).split(" - ")
                thisTrackArtist = thisTrackArtistSong[0]
                thisTrackSong = thisTrackArtistSong[1]
                thisTrackSong = thisTrackSong.split(".")
                thisTrackSong = thisTrackSong[0]

        if str(filesHaveTrackNumber) != "True":
            thisTrackNumber = trackNumber
            thisTrackArtistSong = str(track).split(" - ")
            thisTrackArtist = thisTrackArtistSong[0]
            thisTrackSong = thisTrackArtistSong[1]
            thisTrackSong = thisTrackSong.split(".")
            thisTrackSong = thisTrackSong[0]

        #thisTrackInfoTrack.update({"track_number": int(thisTrackNumber)})
        trackNumberField = "track_number " + str(thisTrackNumber)
        thisTrackInfo.update({"original_filename": str(track)})
        thisTrackInfo.update({"artist": thisTrackArtist})
        thisTrackInfo.update({"title": thisTrackSong})

        
        currentAudioFile = os.path.join(audioDir,track)
        totalFileSize = os.path.getsize(currentAudioFile)  #file size in bytes
        currentAudioFile = mutagen.File(currentAudioFile)   #using mutagen to get id3 tag info
        if currentAudioFile.tags == None:
            thisTrackInfo.update({"id3_size": 0})
            id3TagSize = 0
        else:
            
            id3TagSize = currentAudioFile.tags.size
            thisTrackInfo.update({"id3_size": id3TagSize})

        trackLength = currentAudioFile.info.length
        thisTrackInfo.update({"file_size": totalFileSize})
        thisTrackInfo.update({"length": trackLength})

        #thisTrackInfoTrack.update({"info":thisTrackInfo})

        returnData.update({trackNumberField: thisTrackInfo})
        
        trackNumber = trackNumber + 1

    return returnData

def getImageInfo(imageFile, imageDir, imageCSVMetadataInfo):
    #takes an image file
    #returns list of image File info:  file name, file size in bytes
    returnData = {}
    imageName = str(imageFile)
    currentImage = os.path.join(imageDir,imageFile)
    imageSize = os.path.getsize(currentImage)
    returnData.update({"file": imageName})
    returnData.update({"size": imageSize})

    if imageCSVMetadataInfo[0] != None:
        headers = imageCSVMetadataInfo[0]
        rows = imageCSVMetadataInfo[1]

        for row in rows:
            if str(row[0]) == imageName:
                columnNumber = 1
                for column in headers[1:]:
                    returnData.update({str(column):str(row[columnNumber])})
                    columnNumber = columnNumber + 1


    
    return returnData

def fileCreator(audioNFTHexString,imageFile, audioFiles, collectionData,folderInfo,fileNumber):
    #creates a new AudioNFT file. 
    #returns the name of the new file.
    workingDir = folderInfo[0]
    imageDir = folderInfo[1]
    audioDir = folderInfo[2]
    outputDir = folderInfo[3]
    fileNumber = str(fileNumber)
    
    imageFileName = str(imageFile).split(".")
    audioCollectionName = collectionData["audio"]["audio_collection_name"]
    newFileName = str(fileNumber + audioCollectionName + "." + imageFileName[1])
    newFileName = newFileName.replace(" ", "")
    newFile = os.path.join(outputDir, newFileName)
    imageFile = os.path.join(imageDir, imageFile)
    audioNFTHexString = audioNFTHexString[1].encode()
    
    open(newFile, 'x')
    with open(newFile, 'ab') as nf, open(imageFile, 'rb') as imgf:
        nf.write(imgf.read())
        nf.write(audioNFTHexString)

    for audioFile in audioFiles:
        audioFile = os.path.join(audioDir,audioFile)
        with open(newFile, 'ab') as nf, open(audioFile, 'rb') as af:
            nf.write(af.read())

    print('AudioNFT File Created')

    return newFileName
    
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
    imageCSVMetadataInfo = getCsvMetaDataFileInfo(folderInfo)
    audioTrackInfo = getAudioTrackInfo(audioDir, audioFiles, collectionData)
    
    uuidNumber = str(uuid.uuid4())
    
    fileNumber = 1
    for imageFile in imageFiles[0]:

            imageInfo = getImageInfo(imageFile,imageDir,imageCSVMetadataInfo)
            audioNFTHexString = createAudioNFTHexString(collectionData,imageInfo,audioTrackInfo)
            newFileName = fileCreator(audioNFTHexString, imageFile, audioFiles, collectionData, folderInfo,fileNumber)

            newFileInfo = addRowToAudioNFTCSVFile(folderInfo,imageCSVMetadataInfo,audioNFTHexString,collectionData,newFileName, fileNumber)
            success = createMetadataFile(folderInfo,collectionData,newFileInfo,uuidNumber,audioNFTHexString)
            fileNumber = fileNumber + 1
   
    return

def menu():
    options = ['1','2']
    print("\nWelcome to CatskillNFTs AudioNFT Creation Tool")
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
