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
#text = [ ['A','B','C','D','E',u"\u2190"], 
#                ['F','G','H','I','J','ENTER'], 
#                ['K','L','M','N','O','abc'], 
#                ['P','Q','R','S','T','123'], 
#                ['U','V','W','X',u"\u25B2",'{&='], 
#                ['Y','Z','SPACE',u"\u25C4",u"\u25BC", u"\u25BA"] ]

textUC = [ ['PT1','PT2','PT3','A','B',u"\u2190"], 
                ['C','D','E','F','G','ENTER'], 
                ['H','I','J','K','L','abc'], 
                ['M','N','O','P','Q','123'], 
                ['R','S','T','U','V','W'], 
                ['X','Y','Z','SPACE',u"\u25C4", u"\u25BA"] ]

textLC = [ ['pt1','pt2','pt3','a','b',u"\u2190"], 
                ['c','d','e','f','g','ENTER'], 
                ['h','i','j','k','l','ABC'], 
                ['m','n','o','p','q','123'], 
                ['r','s','t','u','v','w'], 
                ['x','y','z','SPACE',u"\u25C4", u"\u25BA"] ]

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
backgroundColour = [0,0,1,1]
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
#target timing
targetDelay = 30
#UIsize
UISize = 10
#UIscaling based on UISize
widgetPositionY = UISize*height/12
widgetHeight = height-widgetPositionY
keyboardPositionTop = widgetPositionY - height/12
#character casing
upperCase = False
####################################################################

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        # Called once when starting the scenario
        self.loopCounter = 0
        self.target = [0,0]
        self.selection = [0,0]
	self.rowIndex = 0
	self.colIndex = 0
        self.hashTable = {12:5,11:4,10:3,9:2,8:1,7:0,6:6,5:7,4:8,3:9,2:10,1:11}

        # I/O
        self.initOutputs() # Set output stimulation headers

        # Pyglet
        #create window
        self.win = window.Window(fullscreen = False)
        
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
        self.current_text = "" 
        if(upperCase):
            text = textUC
        else:
            text = textLC
        #set up user keyboard display
        self.words = []
        for j in range(0, len(text) ):
            for i in range(0, len(text[j]) ):
                line = text[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5)
                xpos  = i*width/6
                temp = pyglet.text.Label(line, 
                    font_name='Arial',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
                self.words.append(temp)

        #set up window rendering
        self.win.dispatch_events()
        self.win.flip()
        return

    def endExperiment(self):
        print("Quitting experiment.")
        self.closeOutputs()
        self.sendOutput(0, OVTK_StimulationId_Label_00)
        self.win.close()
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

        if self.win.has_exit:
            self.endExperiment()
        else:
            # Read target 
            for chunkIndex in range( len(self.input[1]) ):
                chunk = self.input[1].pop()
                if(type(chunk) == OVStimulationSet):
                    for stimIdx in range(len(chunk)):
                        stim=chunk.pop();
                        if (33025 <= stim.identifier and stim.identifier <= 33030): # Row
                            self.target[0] = stim.identifier
                        elif (33031 <= stim.identifier and stim.identifier <= 33036): # Column
                            self.target[1] = stim.identifier
                        self.drawTarget(self.target[0]-OVTK_StimulationId_Label_01, self.target[1]-OVTK_StimulationId_Label_07)

            # Read flashes
    	    for chunkIndex in range( len(self.input[0]) ):
    	    	chunk = self.input[0].pop()
                if (type(chunk) == OVStimulationSet):
                    for stimIdx in range(len(chunk)):
			stim = chunk.pop()
                        self.drawFlash(self.flashRC-OVTK_StimulationId_Label_00)

            # Read row selection
            for chunkIndex in range( len(self.input[2]) ):
                chunk = self.input[2].pop()
                if(type(chunk) == OVStimulationSet):
                    for stimIdx in range(len(chunk)):
                        stim=chunk.pop()
                        self.selection[0] = stim.identifier
                        self.rowIndex = self.selection[0] - OVTK_StimulationId_Label_01
                        
            # Read column selection
            for chunkIndex in range( len(self.input[3]) ):
                chunk = self.input[3].pop()
                if(type(chunk) == OVStimulationSet):
                    for stimIdx in range(len(chunk)):
                        stim=chunk.pop();
                        self.selection[1] = stim.identifier
                        self.colIndex = self.selection[1] - OVTK_StimulationId_Label_07
                        
            self.text_input = textUC[self.rowIndex][self.colIndex]
            self.current_text = self.current_text + self.text_input
            self.widget.caret.on_text(self.text_input)
            self.text_input = ""

            self.win.dispatch_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background


            if (self.keys[key.A]):
                self.text_input = "gr"
                self.current_text = self.current_text + self.text_input
                self.widget.caret.on_text(self.text_input)
                self.text_input = ""
                
            corrected_text = word_predictor.correct(self.current_text)
            ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
            xpos  = 0*width/6
            temp0 = pyglet.text.Label(corrected_text[0], 
                    font_name='monospace',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
           
            ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
            xpos  = 1*width/6
            temp1 = pyglet.text.Label(corrected_text[1], 
                    font_name='monospace',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
            
            ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
            xpos  = 2*width/6
            temp2 = pyglet.text.Label(corrected_text[2], 
                    font_name='monospace',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
            self.words[0] = temp0
            self.words[1] = temp1
            self.words[2] = temp2
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
