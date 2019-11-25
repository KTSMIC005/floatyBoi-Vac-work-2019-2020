#**************************************************************************
#*  TRIDENT BUOY SBD LOG FILE DATA EXTRACTION AND VISUALISATION TOOL      *
#**************************************************************************
#   Created by:    R.A. Verrinder
#   Modified by:
#   Date created:  2019-11-13
#   Date modified: 2019-11-13
#**************************************************************************
#   Python ver.:   3.6
#   Libraries needed:  NumPy, SciPy, Matplotlib, datetime, os, csv
#==========================================================================
# IMPORT Libraries
#==========================================================================
import csv                               # imports csv data handling capabilites
import datetime                          # date/time proc. incl. epoch conversion
#import matplotlib.dates as mdates        # date/time conv. for plotting (renamed)
import matplotlib.pyplot as plt          # histogram plotting (renamed)
import numpy as np                       # maths functions (renamed)
import os                                # os module imported here
from bitstring import BitStream
import gmplot
import cartopy.crs as ccrs


#==========================================================================
# GLOBAL VARIABLES
#==========================================================================
pathLocation         = os.getcwd()                  # returns current directory
dataDirectoryName    = "DataOutputFiles"            # name of the directory where outputs will be stored
batchFilenameDefault = "completelogfile"            # generic log file name for all combined logs
#--------------------------------------------------------------------------
directoryOptionsList = ["C","D"]                    # directory menu options list
menuOptionsList      = ["S","B","X","P","L","R"]    # general menu options list
menuSelection        = "z"                          # default random selection not in menu list
#--------------------------------------------------------------------------
logFileNameList      = []                           # list to store all log files names
logNamePrefix        = "300434062125010"            # default log file name prefix
extension            = ".sbd"                       # default log file extension
extensionUpperCase   = extension.upper()            # default log file extension upper case
minimumFileSize      = 17                           # minimum file size in bytes
                                                    # output file name lookup table
fileDictionary       = {"filename"            :batchFilenameDefault,
                        "filenameOUTRaw"      :""}
axisInterval         = 1
#--------------------------------------------------------------------------
degreeSign           = u'\N{DEGREE SIGN}'           # degree circle symbol
year                 = 19
#--------------------------------------------------------------------------
GOOGLE_API_KEY       = "AIzaSyD6N1hU5osqkFErrxDmA0ygAvqAUtzkOAw"
#==========================================================================    
# FUCTIONS  
#==========================================================================
def column(matrix, i):
    return [row[i] for row in matrix]

# setDirectoryPath Function
#--------------------------------------------------------------------------
# Set working directory path and creates a new directory for resulting
# data (defined by dataDirectoryName) 
#--------------------------------------------------------------------------
def setDirectoryPath():
    pathSelection        = "z"
#--------------------------------------------------------------------------   
# check if option exists else prompt again
    while(pathSelection not in directoryOptionsList) :  
        # SELECTION PROMPT
        pathSelection = input("Change directiory to log files (D) or use current directory (C):\t")
        pathSelection = pathSelection.upper()
#--------------------------------------------------------------------------       
# USE CURRENT PATH
        if pathSelection == "C"  :                    # If current directory selected
            pathLocation = os.getcwd()                # Get current path location
            print("Current path is " +  pathLocation) # Display current path
#--------------------------------------------------------------------------        
# CHANGE PATH
        elif pathSelection == "D":                    # If change directory selected
            pathLocation = "path"                     # set random path to start loop
#--------------------------------------------------------------------------            
            while (not os.path.isdir(pathLocation)):  # while path location is not found
# NEW PATH PROMPT
                pathLocation = input("Enter the full path to log file directory:\t")
#--------------------------------------------------------------------------            
# check if path exists then change directory else prompt again
                if os.path.isdir(pathLocation):
                    os.chdir(pathLocation)            # Change directory to new path
                    print("\n")
                    print("Path changed to " + pathLocation)
                elif pathLocation == "C" or "c"  :    # If current directory selected
                    pathLocation = os.getcwd()        # Get path location
                    print("Current path is " + pathLocation)# Display current path
                    break                             # Break from loop and use current directory
                else:
                    print("The path you have entered is:  " + pathLocation)
                    print("Invalid path, please re-enter path or enter (C) to use current directory.")          
#--------------------------------------------------------------------------       
# INVALID OPTION MESSAGE
        else:
            print("Invalid selection")            
            pathLocation = os.getcwd()                # get present working directory location
            print("Current path is " + pathLocation)
#==========================================================================
# extensionCheck Function
#--------------------------------------------------------------------------
# Creates a list of log files (single or full list)
#--------------------------------------------------------------------------           
def extensionCheck(fileName):
    if (extension or extensionUpperCase) in fileName:
        filenameIN  = fileName     # Input data log file path/name
    else:
        filenameIN  = fileName + extension
    return filenameIN
#==========================================================================           
# createLogList Function
#--------------------------------------------------------------------------
# Creates a list of log files (single or full list)
#--------------------------------------------------------------------------  
def createLogList(selection):
#---------------------------------------------------------------------------     
    logCounter   = 0                         # keep count of total number of log files
    otherCounter = 0                         # keep count of all other files found
    filenameIN=extensionCheck(fileDictionary["filename"])
    logFileNameList = []
#---------------------------------------------------------------------------   
    if (selection == "B"): 
#---------------------------------------------------------------------------         
        for file in os.listdir(pathLocation):
            try:
                if file.startswith(logNamePrefix) and file.endswith(extension):
                    print("log file found:\t"+ file)
                    logFileNameList.append(str(file))
                    logCounter = logCounter+1
                else:
                    otherCounter = otherCounter+1
            except Exception as e:
                raise e
                print("No log files found!")
                
            filenameOUT = fileDictionary["filename"] + extension
#---------------------------------------------------------------------------                
    elif (selection == "S"):
#---------------------------------------------------------------------------        
        if os.path.isfile(filenameIN):
            print("log file found:\t"+ filenameIN)
            logFileNameList.append(str(filenameIN))
            logCounter = logCounter+1
        else:
            while(not os.path.isfile(filenameIN)):
                print("File does not exist in current directory!")
                print("You entered: "+ filenameIN)
                fileDictionary["filename"] = input("Please enter the log file name:\t")
                fileDictionary["filename"] = fileDictionary["filename"].upper()
                filenameIN=extensionCheck(fileDictionary["filename"])
        filenameOUT = fileDictionary["filename"] + extension
#---------------------------------------------------------------------------                        
    else:
#---------------------------------------------------------------------------         
        print("Invalid selection")           
#---------------------------------------------------------------------------
        print ("Total log files found:\t" + str(logCounter))
        print ("Total other files found:\t" + str(otherCounter))
#---------------------------------------------------------------------------
# Creates a dictionary of the files      
    fileDictionary["filename"]            = fileDictionary["filename"]
    fileDictionary["filenameOUTRaw"]      = fileDictionary["filename"][:-4]+"Raw.csv"        # Output filename for csv file with epoch time
    sortedlogFileNameList = sorted(logFileNameList, key=lambda x:x[-10:])
 #---------------------------------------------------------------------------       
# Creates csv file header     
    with open(fileDictionary["filenameOUTRaw"], "w+") as f:
        f.write("UTC Date Time"+","+\
                "Latitude"+","+\
                "Longitude"+","+\
                "Latitude"+","+\
                "Longitude"+","+\
                "Altitude"+","+\
                "Temperature"+","+\
                "Battery Voltage"+","+\
                "File Name\n")  
        f.write("UTC Date Time"+","+\
                "[DMS]"+","+\
                "[DMS]"+","+\
                "[DD]"+","+\
                "[DD]"+","+\
                ""+","+\
                "[m]"+","+\
                "[Degrees Celcius]"+","+\
                "[volts]"+","+\
                "\n")  
#---------------------------------------------------------------------------
# Checks to see if the log files are above a minimum size defined by minimumFileSize and appends them to one file
# for processing
#    with open(filenameOUT, "w+") as fnew:
    for fileNumber in range(len(sortedlogFileNameList)):
 #       with open(logFileNameList[fileNumber]) as currentLog:
        if os.path.getsize(sortedlogFileNameList[fileNumber])>=minimumFileSize:
             print(sortedlogFileNameList[fileNumber])
             extractLogFile(sortedlogFileNameList[fileNumber])
        else:
            print (sortedlogFileNameList[fileNumber]+" does not contain enough data "+str(np.round(os.path.getsize(sortedlogFileNameList[fileNumber]),1))+" < "+str(minimumFileSize)+" bytes")
            logCounter = logCounter - 1

#==========================================================================
# extractLogFile Function
#--------------------------------------------------------------------------
# LOG FILE CLEANING TO DATA INTO CSV FILE
#--------------------------------------------------------------------------
# 1. Opens log binary .sbd file defined by filenameIN
# 2. Creates/opens CSV file to write raw data to
# 3. Searches through the 17 byte binary string and extracts message
# 4. Each line in the new file has this form from start bit 0 in byte 0
#               ===============================================
#              |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |
#     =========|=====|=====|=====|=====|=====|=====|=====|=====|
#     BYTE0:   | ID                                | MSG       | 
#     _________|___________________________________|___________|  
#     BYTE1:   | SW              | Hour                        | 
#     _________|_________________|_____________________________|   
#     BYTE2:   | HLat| HLon| Minute                            | 
#     _________|_____|_____|___________________________________|  
#     BYTE3:   | Second                            | LatMinDec | 
#     _________|___________________________________|___________| 
#     BYTE4:   | LatMinDec                                     | 
#     _________|_______________________________________________|       
#     BYTE5:   | LatDegree                               | LatM| 
#     _________|_________________________________________|_____| 
#     BYTE6:   | LatMin                            | LonMinDec | 
#     _________|___________________________________|___________|
#     BYTE7:   | LonMinDec                                     | 
#     _________|_______________________________________________|      
#     BYTE8:   | LonDegree                                     | 
#     _________|_______________________________________________| 
#     BYTE9:   | LonMin                                  | Bat | 
#     _________|_________________________________________|_____|
#     BYTE10:  | BattRead        | Altitude                    | 
#     _________|_________________|_____________________________| 
#     BYTE11:  | Altitude                                      | 
#     _________|_______________________________________________|     
#     BYTE12:  | Mot | TempRead                                |  
#     _________|_____|_________________________________________|        
#     BYTE13:  | JDay                                          |
#     _________|_______________________________________________|          
#     BYTE14:  | JDay| Course                                  | 
#     _________|_____|_________________________________________|        
#     BYTE15:  | Course    | SOG                               | 
#     _________|___________|___________________________________|        
#     BYTE16:  | SOG                   | F1  | F2  | F3  | F4  |         
#     =========|=======================|=====|=====|=====|=====|      
#--------------------------------------------------------------------------    
#    Data output format (packetsize = 17-bytes*8-bits = 136-bits)
#--------------------------------------------------------------------------       
#   ID:         (6-bits)    (1 to 63)                
#   MSG:        (2-bits)    (1 to 3)                 
#   SW:         (3-bits)    (0 to 7) 
#   Hour:       (5-bits)    (00 to 23) 
#   HEMLat:     (1-bit)     (0: North [+ve]; 1: South [-ve])
#   HEMLon:     (1-bit)     (0: East [+ve]; 1: West [-ve]) 
#   Minute:     (6-bits)    (00 to 59)      
#   Second:     (6-bits)    (00 to 59)      
#   LatMinDec:  (10-bits)   (000 to 999)   
#   LatDegree:  (7-bits)    (0 to 89)       
#   LatMin:     (7-bits)    (0 to 59)        
#   LonMinDec:  (10-bits)   (000 to 999)   
#   LonDegree:  (8-bits)    (0 to 179)       
#   LonMin:     (7-bits)    (0 to 59)   
#   BattRead:   (4-bits)    (0 to 15 = 5 to 6.5; (BattRead/10)+5= BattVoltage))                  
#   Altitude:   (13-bits)   (0 to 8191)  
#   Motion:     (1-bit)     (0 to 1)        
#   TempRead:   (7-bits)    (0 to 100 = -40 to +60; (Temperature -40) = Temperature))   
#   JDay:       (9-bits)    (1 to 366)  
#   Course:     (9-bits)    (1 to 359)  
#   SOG:        (10-bits)   (1 to 359)  
#   Flag1:      (1-bit)     (0/1)  
#   Flag2:      (1-bit)     (0/1) 
#   Flag3:      (1-bit)     (0/1) 
#   Flag4:      (1-bit)     (0/1)        
#--------------------------------------------------------------------------
def extractLogFile(fileName):
#--------------------------------------------------------------------------
# Read in the binary data from the file into rawData
#--------------------------------------------------------------------------
    rawData =  BitStream(filename=fileName)
#--------------------------------------------------------------------------
# Extract each parameter from the binary data and convert to unsigned integers 
#--------------------------------------------------------------------------
    ID,         \
    MSG,        \
    SW,         \
    Hour,       \
    HEMLat,     \
    HEMLon,     \
    Minute,     \
    Second,     \
    LatMinDec,  \
    LatDegree,  \
    LatMin,     \
    LonMinDec,  \
    LonDegree,  \
    LonMin,     \
    BattRead,   \
    Altitude,   \
    Motion,     \
    TempRead,   \
    JDay,       \
    Course,     \
    SOG,        \
    Flag1,      \
    Flag2,      \
    Flag3,      \
    Flag4       = rawData.readlist('uint:6,2,3,5,1,1,6,6,10,7,7,10,8,7,4,13,1,7,9,9,10,1,1,1,1')
#--------------------------------------------------------------------------
# Convert each parameter into the correct format before writing to the .csv
#--------------------------------------------------------------------------
# Date/Time: YYYY-MM-DDTHH:mm:ss+00:00 (UTC time)
#--------------------------------------------------------------------------
    CalendarDate = datetime.datetime.strptime(str(year)+str(JDay), "%y%j").date()
    DateTimeUTC  = datetime.datetime(CalendarDate.year, CalendarDate.month, CalendarDate.day, Hour, Minute, Second, 0,tzinfo=datetime.timezone.utc)
#--------------------------------------------------------------------------
# Latitude: Degrees°Minutes'Seconds.dec Hemisphere [N/S]
#--------------------------------------------------------------------------
    LatSec = round(((LatMinDec)*0.06),5)
    
    if      (HEMLat == 0):
        LatNS   = "N"
        LatSign = 1
    elif    (HEMLat == 1):
        LatNS = "S"
        LatSign = -1
    else:
        LatNS = "Error"
    
    LatDMSString = str(LatDegree)+"deg"+str(LatMin)+"'"+str(LatSec)+"\" "+LatNS
    LatDDString  = str(LatSign*(LatDegree+(LatMin/60)+(LatSec/3600)))

#--------------------------------------------------------------------------
# Longitude: Degrees°Minutes'Seconds.dec Hemisphere [E/W]
#--------------------------------------------------------------------------
    LonSec = round(((LonMinDec)*0.06),5)
    
    if      (HEMLon == 0):
        LonEW = "E"
        LonSign = 1
    elif    (HEMLon == 1):
        LonEW = "W"
        LonSign = -1
    else:
        LonEW = "Error"
    
    LonDMSString = str(LonDegree)+"deg"+str(LonMin)+"'"+str(LonSec)+"\" "+LonEW
    LonDDString  = str(LonSign*(LonDegree+(LonMin/60)+(LonSec/3600)))
#--------------------------------------------------------------------------
# Battery Voltage: voltage V [+5 V to +6.5 V]
#--------------------------------------------------------------------------
    BattVoltage   = str((BattRead/10)+5)+" V"
#--------------------------------------------------------------------------
# Temperature: temp °C [-40 to +60 °C]
#--------------------------------------------------------------------------
    Temperature = str(TempRead-40)
#--------------------------------------------------------------------------                     
    with open(fileDictionary["filenameOUTRaw"], "a+") as f:
        f.write(DateTimeUTC.isoformat()+","+\
                LatDMSString+","+\
                LonDMSString+","+\
                LatDDString+","+\
                LonDDString+","+\
                str(Altitude)+","+\
                Temperature+","+\
                BattVoltage+","+\
                str(fileName)+"\n")        
    
    print("log file processing...\n")
    print(fileDictionary["filenameOUTRaw"] + " created/overwritten")
#==========================================================================
# moveFiles Function
#-------------------------------------------------------------------------- 
# moves generated files into directory defined by dataDirectoryName
# default value is "DataOutputFiles"
#--------------------------------------------------------------------------                                       
def moveFiles():
#--------------------------------------------------------------------------      
    # MAKE A NEW DIRECTORY TO STORE OUTPUT FILES      
    if not os.path.exists(dataDirectoryName):
        os.makedirs(dataDirectoryName)
#--------------------------------------------------------------------------     
    source      = os.getcwd()                           # returns current directory 
    destination = os.getcwd() + "/" + dataDirectoryName # points to output directory
#--------------------------------------------------------------------------     
    print ("*********************************************************")
    print ("MOVING FILES...")
    print ("*********************************************************")
#--------------------------------------------------------------------------  
    # IF BATCH CONCATENATED LOGFILE EXISTS MOVE IT TO OUTPUT DIRECTORY    
    if(fileDictionary["filename"].upper()=="COMPLETELOGFILE.TXT"):
        os.rename(source+"/"+fileDictionary["filename"]     , destination+"/"+fileDictionary["filename"])
        print(fileDictionary["filename"] +" moved to "+ destination+"\n")
#--------------------------------------------------------------------------
    # MOVE CSV FILES AND HISTOGRAM PLOT
    os.rename(source+"/"+fileDictionary["filenameOUTRaw"]     , destination+"/"+fileDictionary["filenameOUTRaw"])
#    os.rename(source+"/"+fileDictionary["filenameOUTFig"]     , destination+"/"+fileDictionary["filenameOUTFig"])               
#--------------------------------------------------------------------------
    # PRINT MESSAGES 
    print(fileDictionary["filenameOUTRaw"] +" moved to "+ destination+"\n")
#    print(fileDictionary["filenameOUTFig"] +" moved to "+ destination+"\n")
#==========================================================================c
# generateDateTimeLogFile Function
#-------------------------------------------------------------------------- 
# 1. Opens/reads cleaned data csv file defined by filenameOUTRaw
# 2. Writes the data to a matrix: dataMatrix = [[epochTime],[guessedWeight]]
# 3. Extracts the time data and writes it to timeList
#-------------------------------------------------------------------------- 
def plotMap(latitude, longitude):
    gmap = gmplot.GoogleMapPlotter(latitude[2],longitude[2], 3)   
    gmap.apikey = GOOGLE_API_KEY         
    gmap.scatter(latitude[1:], longitude[1:], 'darkgoldenrod',size = 1000, marker = False ) 
    
    gmap.draw("C:\\Users\\user\\Desktop\\map.html")

    fig, ax = plt.subplots(1,1)
    
#    central_lon, central_lat = 0, -55
    extent = [8, 18, -58, -60]


    ax = plt.axes(projection=ccrs.Orthographic())
    ax.set_extent(extent)
    ax.gridlines()
    ax.coastlines(resolution='50m')
    ax.stock_img()
    plt.scatter(longitude[1:], latitude[1:],
        marker = ".",       
        alpha=0.5,
        linewidths=1, 
        edgecolors='midnightblue', 
        transform=ccrs.Geodetic(),
         )
    plt.scatter(longitude[0], latitude[0],
        marker = ".",       
        alpha=0.5,
        linewidths=1, 
        edgecolors='red', 
        transform=ccrs.Geodetic(),
         )

    
#    ax.set_global() 
    
    plt.show()
    fig.savefig("fig",dpi=300, bbox_inches='tight', pad_inches=0.2)
    
#==========================================================================c
# generateDateTimeLogFile Function
#-------------------------------------------------------------------------- 
# 1. Opens/reads cleaned data csv file defined by filenameOUTRaw
# 2. Writes the data to a matrix: dataMatrix = [[epochTime],[guessedWeight]]
# 3. Extracts the time data and writes it to timeList
#-------------------------------------------------------------------------- 
def extractCSVData(filename):
    csvfile    = open(filename, 'r')
    reader     = csv.reader(csvfile, delimiter=',')
    dataMatrix = list(reader)
    return dataMatrix       
#**************************************************************************
# END OF FUNCTIONS    
#**************************************************************************
# WELCOME MESSAGE
#==========================================================================
print("*******************************************************************")
print("          TRIDENT BUOY SBD LOG FILE PROCESSING SCRIPT")
print("*******************************************************************")
#---------------------------------------------------------------------------
# PROMPT FOR PATH TO LOG FILES
#---------------------------------------------------------------------------
setDirectoryPath()
#==========================================================================
# Select file processing options
#==========================================================================
# This script does not modify exisiting log files except when delete is used.
# Path and file name must be defined correctly.
#---------------------------------------------------------------------------
# MENU PROMPT 
#---------------------------------------------------------------------------
while(menuSelection not in menuOptionsList) :    # Run while X is not selected (or other menu options)
#---------------------------------------------------------------------------
# Display menu
#---------------------------------------------------------------------------
    print("\n")
    print("------------------------------- MENU ------------------------------")
    print(" P\t Set new path to log files ")
    print(" S\t Process a single log file ")
    print(" B\t Process a batch of log files in same directory ")   
    print(" M\t Make a map ")
    print(" L\t List LOG files in current directory")
    print(" R\t Delete LOG file from current directory")
    print(" X\t Exit script ")
    print("-------------------------------------------------------------------")
    print("\n")
#---------------------------------------------------------------------------
    pathLocation = os.getcwd()
    print("Current path is " + pathLocation)      # Display current path
    
    menuSelection = input("Enter selection:  ")   # Prompt user to enter menu option
    menuSelection = menuSelection.upper()         # Convert selection to upper case  
#===========================================================================
# OPTION P: Set new path to log files
#---------------------------------------------------------------------------  
    if  menuSelection == ("P"):
#---------------------------------------------------------------------------
        setDirectoryPath()
        menuSelection = "z"                       # Reset menu option so that loop repeats
#===========================================================================
# OPTION S: Single log file processing
#---------------------------------------------------------------------------
    elif menuSelection == ("S"):
#---------------------------------------------------------------------------
        fileDictionary["filename"] = input("Please enter the log file name:\t")
        fileDictionary["filename"] = fileDictionary["filename"].upper()
        
        createLogList(menuSelection) 
#        extractLogFile()

       # filenameOUT = fileDictionary["filename"][:-4]+"OUT.txt"
       # os.remove(filenameOUT)
        
        dataMatrix = extractCSVData(fileDictionary["filenameOUTRaw"]);
  #      generateDateTimeFile(dataMatrix)
        moveFiles()  
        print("Log cleaning and extraction of file complete!")
        menuSelection = "z"                       # Reset menu option so that loop repeats
            
#===========================================================================
# OPTION B: Batch of log files processing
#---------------------------------------------------------------------------
    elif menuSelection == ("B"):
#---------------------------------------------------------------------------
        print("\n")    
        createLogList(menuSelection) 

        dataMatrix    = extractCSVData(fileDictionary["filenameOUTRaw"]);
        latitudeList  = column(dataMatrix,3)
        latitudeList  = latitudeList[2:]
        latitudeList  =  [float(x) for x in latitudeList]
        longitudeList = column(dataMatrix,4)
        longitudeList = longitudeList[2:]
        longitudeList =  [float(x) for x in longitudeList]   
 #       generateDateTimeFile(dataMatrix)
        moveFiles()  
        print("Log file cleaning and extraction complete for current directory!")
        menuSelection = "z"                      # Reset menu option so that loop repeat
#===========================================================================
# OPTION M: Maps the points
#---------------------------------------------------------------------------
    elif menuSelection == ("M"):
#---------------------------------------------------------------------------
        print("\n")    
        plotMap(latitudeList[2:],longitudeList[2:])
        menuSelection = "z"                      # Reset menu option so that loop repeat        
#===========================================================================
# OPTION L: List log files in current directory
#---------------------------------------------------------------------------      
    elif menuSelection == ("L"):
#---------------------------------------------------------------------------             
         for file in os.listdir(pathLocation):
            if file.startswith(logNamePrefix) and file.endswith(extension):
                print(file+"\t"+str(np.round(os.path.getsize(file),1))+" "+"bytes")
         menuSelection = "z"                    # Reset menu option so that loop repeat
#===========================================================================
# OPTION R: Delete log files in current directory
#---------------------------------------------------------------------------      
    elif menuSelection == ("R"):
#---------------------------------------------------------------------------             
        file = input("Enter name of file to delete:\t ")
        file = file.upper()
        file = extensionCheck(file)
        
        if file in os.listdir(pathLocation):
            print("You have entered: "+ file)
            
            if np.round(os.path.getsize(file),1)>0:
                print("This file contains data (> 0 bytes)")
            else:
                print("This file is empty")
            
            check = input("Are you sure that you wish to delete this file (Y/N)?  ")
            
            check=check.upper()
            if check == "Y":
                 os.remove(file)
                 print(file+" deleted")
            else:
                print("No file has been deleted.")
        else:
            print("You entered: "+file)
            print("File does not exist!")
        menuSelection = "z"
#===========================================================================
# OPTION X: Exit script
#---------------------------------------------------------------------------
    elif menuSelection == ("X"):
#---------------------------------------------------------------------------
        print("Exitting script")
        break
#===========================================================================   
    else:
        print("Invalid Selection")
        
#**************************************************************************
# END OF SCRIPT
#**************************************************************************
