import os, sys
import ctypes

# Get window parameters
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

############################# CONTROLS #############################
#P300 flash modes
isEnlargeTextMode = True
isHighlightTextMode = True
isDrawCircleMode = True
isCrazyKeyboardEnlargeColour = False
isCrazyHighlightTextMode = False
isCrazyDrawCircleMode = True
isDrawImageMode = True
#image mode parameters
imageWidth = 100
imageHeight = 100
#condition to draw image
isDrawVertImage = True
#condition to draw circle
isDrawVertCircle = True
isDrawHorizCircle = True
#circle mode parameters
circleRadius = 10
circleColourDefault = [1,0,1,1]
#condition to draw flash
isDrawVertFlash = False
isDrawHorizFlash = False
#condition to draw target
isDrawTarget = True
#target parameters
targetSize = [width/6,height/12]
#general UI display paramaters
backgroundColour = [0,0,1,1] #1 corresponds to 255 last value is alpha
#text parameters
keyboardFontSize = 36
keyboardFontColour = [230,230,230,255]
keyboardEnlargeFontSize = 50
keyboardEnlargeFontColourDefault = (255,0,255,255) #default
keyboardEnlargeFontColour = keyboardEnlargeFontColourDefault
#timing
targetDelay = 30
flashDuration = 200
#UIsuze
UISize = 10
#UIscaling based on UISize
widgetPositionY = UISize*height/12
widgetHeight = height-widgetPositionY
keyboardPositionTop = widgetPositionY - height/12
#highlight mode parameters
targetFontColour = [255,0,255,255]
targetColour = [0,1,0,1]
vertFlashColourDefault = [0,1,1,1]
vertFlashSize = [width/6,height]
horizFlashColourDefault = [0,1,1,1]
horizFlashSize = [width,keyboardPositionTop/12]
# Initial matrix choice
matIndex = 0
####################################################################

OVTK_StimulationId_Target = 33285
OVTK_StimulationId_Label_00 = 33024
OVTK_StimulationId_Label_01 = 33025
OVTK_StimulationId_Label_07 = 33031

textUC = [ ['PT1','PT2','PT3','A','B',u"\u2190"], 
                ['C','D','E','F','G','ENTER'], 
                ['H','I','J','K','L','123'], 
                ['M','N','O','P','Q','abc'], 
                ['R','S','T','U','V',u"\u25C4"], 
                ['W','X','Y','Z','SPACE',u"\u25BA"] ]

textLC = [ ['pt1','pt2','pt3','a','b',u"\u2190"], 
                ['c','d','e','f','g','ENTER'], 
                ['h','i','j','k','l','ABC'], 
                ['m','n','o','p','q','123'], 
                ['r','s','t','u','v',u"\u25C4"], 
                ['w','x','y','z','SPACE',u"\u25BA"] ]

textNum = [ ['pt1','pt2','pt3','Email','WhatsApp',u"\u2190"], 
                ['1','2','3','Facebook','Twitter','ENTER'], 
                ['4','5','6','Aaron','Javi','abc'], 
                ['7','8','9','Jorn','Jun','ABC'], 
                ['0','.',',','Nico','Sam',u"\u25C4"], 
                ['@','!','?','Vinay','SPACE', u"\u25BA"] ]
