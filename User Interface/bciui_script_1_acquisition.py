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
isEnlargeTextMode = True
isHighlightTextMode = False
#condition to draw flash
isDrawVertFlash = True
isDrawHorizFlash = True
#condition to draw target
isDrawTarget = True
#target parameters
targetSize = [width/6,height/12]
#general UI display paramaters
backgroundColour = [0,0,1,1] #1 corresponds to 255 last value is alpha
#highlight mode parameters
targetColour = [0,1,0,1]
vertFlashColour = [0,1,1,1]
vertFlashSize = [width/6,height/2]
horizFlashColour = [0,1,1,1]
horizFlashSize = [width,height/12]
#text parameters
keyboardFontSize = 36
keyboardFontColour = [230,230,230,255]
keyboardEnlargeFontSize = 50
keyboardEnlargeFontColour = [255,255,0,255]
#timing
targetDelay = 30
#UIsuze
UISize = 10
#UIscaling based on UISize
widgetPositionY = UISize*height/12
widgetHeight = height-widgetPositionY
keyboardPositionTop = widgetPositionY - height/12
####################################################################

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        # Called once when starting the scenario
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
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
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
    
    def drawFlash(self, rowcol):
        rowcolMap = self.hashTable[rowcol]
        #text enlargement mode
        if(isEnlargeTextMode):
            if(rowcolMap < 6 and isDrawVertFlash):
                tmp = rowcolMap
                for i in range (len(self.words)):
                    if(i == tmp):
                        self.words[i].font_size = keyboardEnlargeFontSize
                        self.words[i].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
                        tmp = tmp +6
                    else:
                        self.words[i].font_size = keyboardFontSize
                        self.words[i].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
            elif(rowcolMap < 12 and isDrawHorizFlash):
                tmp = (rowcolMap-11)*-6
                for i in range (len(self.words)):
                    if(i == tmp and i < (rowcolMap-11)*-6 + 6):
                        self.words[i].font_size = keyboardEnlargeFontSize
                        self.words[i].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
                        tmp = tmp + 1
                    else:
                        self.words[i].font_size = keyboardFontSize                        
                        self.words[i].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
        
        if(isHighlightTextMode):    
            if (rowcol < 6 and isDrawVertFlash):
                primitives.drawRect(rowcol*width/6, 0, vertFlashSize[0], vertFlashSize[1], vertFlashColour[0],vertFlashColour[1],vertFlashColour[2],vertFlashColour[3])
            elif (rowcol < 12 and isDrawHorizFlash):
                primitives.drawRect(0, rowcol%6*height/12, horizFlashSize[0], horizFlashSize[1], horizFlashColour[0], horizFlashColour[1], horizFlashColour[2], horizFlashColour[3])
        return         

    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        self.win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background

        if self.win.has_exit:
            self.endExperiment()
        else:
            # Draw background
            #primitives.drawRect(0,height/2,width,height/2,4/51,4/51,4/51,255)
            # Show a target for the first targetDelay loops
            if (self.loopCounter <= targetDelay):
                if (self.loopCounter == 0):
                    self.getNextTarget()
                    self.sendOutput(2, self.target[0])
                    self.sendOutput(2, self.target[1])
                self.drawTarget(self.target[0]-OVTK_StimulationId_Label_01, self.target[1]-OVTK_StimulationId_Label_07)
            # Flash for the next 50 loops
            elif (self.loopCounter <= targetDelay + 50):
                self.getNextFlash()
                self.drawFlash(self.flashRC-OVTK_StimulationId_Label_00)
                print(self.flashRC)
                # Send output
                self.sendOutput(1, self.flashRC)
                # Reset counter on last loop
                if (self.loopCounter == targetDelay + 50): 
                    self.loopCounter = -1

            # Pyglet/GL updates        
            #draw input display
            self.batch.draw() 
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
