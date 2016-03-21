import os, sys
import ctypes

# Get window parameters
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

############################# CONTROLS #############################
#UIsize
UISize = 10
#UIscaling based on UISize
widgetPositionY = UISize*height/12
widgetHeight = height-widgetPositionY
keyboardPositionTop = widgetPositionY 
#FLASHING MODES
isDrawCircleMode = True
isHighlightTextMode = False
isDrawTriMode = True
isDrawImageMode = True
isEnlargeTextMode = True
#CRAZY FLASHING MODES
isDrawCrazyFlashMode = True
isCrazyDrawCircleMode = True
isCrazyHighlightTextMode = True
isCrazyKeyboardEnlargeColour = True
isCrazyDrawTriMode = True
#CIRCLE MODE
isDrawVertCircle = True
isDrawHorizCircle = True
circleRadius = 100
circleColourDefault = [1,0,1,1]
#HIGHLIGHT MODE
isDrawVertFlash = True
isDrawHorizFlash = True
vertFlashColourDefault = [0,1,1,1]
vertFlashSize = [width/6,height]
horizFlashColourDefault = [0,1,1,1]
horizFlashSize = [width,keyboardPositionTop/12]
#ENLARGE TEXT MODE
isDrawHorizEnlarge = True
isDrawVertEnlarge = True
keyboardEnlargeFontSize = 50
keyboardEnlargeFontColourDefault = (255,0,255,255) #default
#TRIANGLE MODE
isDrawVertTri = True
isDrawHorizTri = True
triColourDefault = [1,1,0,1]
triHeight = 87
triWidth = 100
#IMAGE MODE
isDrawVertImage = True
isDrawHorizImage = True
imageWidth = 100
imageHeight = 100
#TARGET
isDrawTarget = True
targetSize = [width/6,height/12]
targetFontColour = [255,0,255,255]
targetColour = [1,1,0.3,1]
#general UI display paramaters
backgroundColour = [0,0,0.5,1] #1 corresponds to 255 last value is alpha
#text parameters
keyboardFontSize = 36
keyboardFontColour = [230,230,230,255]
keyboardEnlargeFontSize = 50
keyboardEnlargeFontColourDefault = (255,0,255,255) #default
keyboardEnlargeFontColour = keyboardEnlargeFontColourDefault
selectTextFontSize = 100
selectTextFontColour = (0,0,0,255)
#timing
targetDelay = 30
flashDuration = 300
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
