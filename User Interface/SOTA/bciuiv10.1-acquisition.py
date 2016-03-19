from __future__ import division, print_function, unicode_literals
import os, sys
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import primitives
import user_input
import word_predictor
import random
import string
import ctypes
from random import randint
#sys.path.append(r'C:\Users\AARON\Dropbox\EE2 BCI Project\User Interface\bciuiv7')
#c:/"program files (x86)"/openvibe/openvibe-designer

#keyboard text
text = [ ['A','B','C','D','E',u"\u2190"], 
                ['F','G','H','I','J','ENTER'], 
                ['K','L','M','N','O','abc'], 
                ['P','Q','R','S','T','123'], 
                ['U','V','W','X',u"\u25B2",'{&='], 
                ['Y','Z','SPACE',u"\u25C4",u"\u25BC", u"\u25BA"] ]

# textLC = [ ['a','b','c','d','e',u"\u2190"], 
#         ['f','g','h','i','j','ENTER'], 
#         ['k','l','m','n','o','ABC'], 
#         ['p','q','r','s','t','123'], 
#         ['u','v','w','x',u"\u25B2",'{&='], 
#         ['y','z','SPACE',u"\u25C4",u"\u25BC", u"\u25BA"] ]

#get window parameters
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
width = width
height = height     
############################# CONTROLS #############################
#P300 flash modes
isEnlargeTextMode = False
isHighlightTextMode = False
isDrawCircleMode = True
isCrazyKeyboardEnlargeColour = True
isCrazyHighlightTextMode = True
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
isDrawVertFlash = True
isDrawHorizFlash = True
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
#timing
targetDelay = 30
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
####################################################################

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        # Called once when starting the scenario
        self.imageLoad = [pyglet.image.load('img/Vinay.jpg'), 
                pyglet.image.load('img/Sam.jpg'), 
                pyglet.image.load('img/Jorn.jpg'),
                pyglet.image.load('img/Jun.jpg'),
                pyglet.image.load('img/Nico.jpg'),
                pyglet.image.load('img/javi.jpg')]
        self.loopCounter = 0
        self.target = [0,0]
        self.hashTable = {12:5,11:4,10:3,9:2,8:1,7:0,6:6,5:7,4:8,3:9,2:10,1:11}
        # Read files into lists for flashes and targets, and convert strings to ints
        with open('dep_files/flash_stims.txt') as f:
            self.flashes = f.read().splitlines()
            self.flashes = [int(x) for x in self.flashes]
        with open('dep_files/target_stims.txt') as f:
            self.targets = f.read().splitlines()
            self.targets = [int(x) for x in self.targets]

        # I/O
        self.initOutputs() # Set output stimulation headers

        # Pyglet
        #create window
        self.win = window.Window(fullscreen = True)
        
        #colour background and set up openGL rendering
        glClearColor(backgroundColour[0], backgroundColour[1], backgroundColour[2], backgroundColour[3])
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        #set up keyboard input
        self.keys = key.KeyStateHandler()
        self.win.push_handlers(self.keys)
        
        #set up user input text display
        self.batch = pyglet.graphics.Batch()
        self.widget = user_input.TextWidget('', 0, int(widgetPositionY), int(width),int(widgetHeight), self.batch)
        self.text_input = ""
        self.widget.caret.on_text(self.text_input)
        
        #set up user keyboard display
        self.words = []
        for j in range(0, len(text) ):
            for i in range(0, len(text[j]) ):
                line = text[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5)
                xpos  = i*width/6
                temp = pyglet.text.Label(line, 
                    font_name='monospace',
                    font_size=keyboardFontSize,
                    color=keyboardFontColour,
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
                self.words.append(temp)

        #set up window rendering
        self.win.dispatch_events()
        self.win.flip()
        return

    def predictText(string):
        words = string.split(' ')
        if len(words[-1]) > 0: 
            w1 = word_predictor.correct(words[-1])
            w2 = words[-1] + 'ing'
            w3 = words[-1] + 'ed'
        else:
            rick = "never gonna give" # you up
            [w1,w2,w3] = rick.split(' ')
        return [w1, w2, w3]

    def endExperiment(self):
        print("Quitting experiment.")
        self.closeOutputs()
        self.sendOutput(0, OVTK_StimulationId_Label_00)
        self.win.close()
        return 

    def getNextFlash(self):
        if len(self.flashes) < 1:
            print("Reached end of flashes file.")
            self.endExperiment()
        else:
            self.flashRC = self.flashes.pop(0)
        return

    def getNextTarget(self):
        if len(self.targets) < 1:
            print("Reached end of target file.")
            self.endExperiment()
        else:
            self.target[0] = self.targets.pop(0) 
            self.target[1] = self.targets.pop(0)
        return 

    def drawTarget(self, targetRow, targetCol):
        if(isDrawTarget):
            primitives.drawRect(targetCol*width/6, (5-targetRow)*(keyboardPositionTop/5), targetSize[0], targetSize[1], targetColour[0],targetColour[1],targetColour[2],targetColour[3])
        return

    def generateRandomColour(self,saturation=1,lightness=0.5):
        hue = randint(0,360)
        while hue > 120 and hue <290:
            hue = randint(0,360)

        chroma = 1 - abs(2*lightness-1)*saturation
        huePrime = hue/60
        intermediateValue = chroma*(1-abs(huePrime%2-1))
        red = 0
        blue = 0
        green = 0
        if huePrime < 1:
            red = chroma
            blue = intermediateValue
            green = 0
        elif huePrime < 2:
            red = intermediateValue
            blue = chroma
            green = 0
        elif huePrime < 3:
            red = 0
            blue = chroma
            green = intermediateValue
        elif huePrime < 4:
            red = 0
            blue = intermediateValue
            green = chroma
        elif huePrime < 5:
            red = intermediateValue
            blue = 0
            green = chroma
        elif huePrime < 6:
            red = chroma
            blue = 0
            green = intermediateValue
        m = lightness - 0.5*chroma
        red = (red+m)
        blue = (blue+m)
        green = (green+m)
        self.colourCrazyNormalized = (red,blue,green,1)
        self.colourCrazy = (int(red*255),int(blue*255),int(green*255),255)
        return 

    def drawFlash(self, rowcol):
        if isCrazyKeyboardEnlargeColour:
            self.generateRandomColour()
            keyboardEnlargeFontColour = self.colourCrazy
        else:
            keyboardEnlargeFontColour = keyboardEnlargeFontColourDefault
        #text enlargement mode
        if(isEnlargeTextMode):
            if(rowcol < 6 and isDrawVertFlash):
                tmp = rowcol
                for i in range (len(self.words)):
                    if(i == tmp):
                        self.words[i].font_size = keyboardEnlargeFontSize
                        self.words[i].color = keyboardEnlargeFontColour
                        self.words[i].bold = True
                        tmp = tmp +6
                    else:
                        self.words[i].font_size = keyboardFontSize
                        self.words[i].color = keyboardFontColour
                        self.words[i].bold = False
            elif(rowcol < 12 and isDrawHorizFlash):
                tmp = (rowcol-11)*-6
                for i in range (len(self.words)):
                    if(i == tmp and i < (rowcol-11)*-6 + 6):
                        self.words[i].font_size = keyboardEnlargeFontSize
                        self.words[i].color = keyboardEnlargeFontColour
                        self.words[i].bold = True
                        tmp = tmp + 1
                    else:
                        self.words[i].font_size = keyboardFontSize                        
                        self.words[i].color = keyboardFontColour
                        self.words[i].bold = False
        
        if(isHighlightTextMode):
            if(isCrazyHighlightTextMode):
                self.generateRandomColour()
                vertFlashColour = self.colourCrazyNormalized
                self.generateRandomColour()
                horizFlashColour = self.colourCrazyNormalized
            else:
                vertFlashColour = vertFlashColourDefault
                horizFlashColour = horizFlashColourDefault
            if (rowcol < 6 and isDrawVertFlash):
                primitives.drawRect(rowcol*width/6, 0, vertFlashSize[0], vertFlashSize[1], vertFlashColour[0],vertFlashColour[1],vertFlashColour[2],vertFlashColour[3])
            elif (rowcol < 12 and isDrawHorizFlash):
                primitives.drawRect(0, rowcol%6*keyboardPositionTop/5, horizFlashSize[0], horizFlashSize[1], horizFlashColour[0], horizFlashColour[1], horizFlashColour[2], horizFlashColour[3])
        if(isDrawCircleMode):
            self.drawCircle(rowcol)
        if(isDrawImageMode):
            self.drawImage(rowcol)
        return         
  
    def drawCircle(self,rowcol):
        if(isDrawCircleMode):
            if(isCrazyDrawCircleMode):
                self.generateRandomColour()
                circleColourVert = self.colourCrazyNormalized
                self.generateRandomColour()
                circleColourHoriz = self.colourCrazyNormalized
            else:
                circleColourHoriz = circleColourDefault
                circleColourVert = circleColourDefault
            if (rowcol < 6 and isDrawVertCircle):
                for j in range (0,6):
                    ypos  = j*(keyboardPositionTop)/5 + circleRadius/4
                    xpos  = rowcol*width/6 + circleRadius/4
                    primitives.drawCircle(xpos,ypos,circleRadius,circleColourVert[0],circleColourVert[1],circleColourVert[2],circleColourVert[3])
            elif(rowcol < 12 and isDrawHorizCircle):
                for j in range (0,6):
                    ypos  = rowcol%6*(keyboardPositionTop)/5 + circleRadius/4
                    xpos  = j*width/6 + circleRadius/4
                    primitives.drawCircle(xpos,ypos,circleRadius,circleColourHoriz[0],circleColourHoriz[1],circleColourHoriz[2],circleColourHoriz[3])        
        return

    def drawImage(self,rowcol):
        if(isDrawImageMode):
            if(rowcol<6 and isDrawVertImage):
                for j in range(0,6):
                    ypos  = j*(keyboardPositionTop)/5
                    xpos  = rowcol*width/6
                    self.imageLoad[randint(0,5)].blit(xpos,ypos,width=imageWidth,height=imageHeight)
            elif(rowcol < 12 and isDrawHorizCircle):
                for j in range (0,6):
                    ypos  = rowcol%6*(keyboardPositionTop)/5
                    xpos  = j*width/6
                    self.imageLoad[randint(0,5)].blit(xpos,ypos,width=imageWidth,height=imageHeight)
        return

    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        self.win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background

        if self.win.has_exit:
            self.endExperiment()
        else:
            self.batch.draw()
            # Draw background
            #primitives.drawRect(0,height/2,width,height/2,4/51,4/51,4/51,255)
            # Show a target for the first targetDelay loops
            if (self.loopCounter <= targetDelay):
                if (self.loopCounter == 0):
                    self.getNextTarget()
                    self.sendOutput(2, self.target[0])
                    self.sendOutput(2, self.target[1])
                self.drawTarget(self.target[0]-OVTK_StimulationId_Label_01, self.target[1]-OVTK_StimulationId_Label_07)
                self.wordNum = (self.target[0]-OVTK_StimulationId_Label_01)*6 + (self.target[1]-OVTK_StimulationId_Label_07)
                for i in range (0,len(self.words)):
                    self.words[i].font_size = keyboardFontSize
                    self.words[i].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
                    self.words[i].bold = False
                self.words[self.wordNum].color = targetFontColour
                self.words[self.wordNum].font_size = keyboardEnlargeFontSize
                self.words[self.wordNum].bold = True
            # Flash for the next 50 loops
            elif (self.loopCounter <= targetDelay + 50):
                if(self.loopCounter == targetDelay + 1):
                    self.words[self.wordNum].color = keyboardFontColour
                    self.words[self.wordNum].font_size = keyboardFontSize
                self.words[self.wordNum].bold = False
                self.getNextFlash()
                if (33025 <= self.flashRC and self.flashRC <= 33036):
                    rowcol = self.hashTable[self.flashRC-OVTK_StimulationId_Label_00] 
                    self.drawFlash(rowcol)
                #print(self.flashRC)
                # Send output
                self.sendOutput(1, self.flashRC)
                # Reset counter on last loop
                if (self.loopCounter == targetDelay + 50): 
                    self.loopCounter = -1

            # Pyglet/GL updates        
            #draw input display
            
            #draw keyboard text
            for i in range (0,len(self.words)):
                self.words[i].draw()
            self.win.flip()
            self.loopCounter += 1
        return

    def uninitialize(self): # Called once when stopping the scenario
        return

    def initOutputs(self):
        print(len(self.output))
        for index in range(len(self.output)):
            # OV protocol requires an output stim header; dates are 0
            self.output[index].append(OVStimulationHeader(0., 0.))
        return

    def sendOutput(self, index, stimLabel):
        # A stimulation set is a chunk which starts at current time and end time is the time step between two calls
        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append( OVStimulation(stimLabel, self.getCurrentTime(), 0.) )
        self.output[index].append(stimSet)
        return

    def closeOutputs(self):
        for index in range(len(self.output)):
            # OV protocol requires an output stim end
            end = self.getCurrentTime()
            self.output[index].append(OVStimulationEnd(end, end))
        return 

OVTK_StimulationId_Target = 33285
OVTK_StimulationId_Label_00 = 33024
OVTK_StimulationId_Label_01 = 33025
OVTK_StimulationId_Label_07 = 33031
box = MyOVBox()
