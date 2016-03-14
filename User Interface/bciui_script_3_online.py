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

OVTK_StimulationId_Target = 33285
OVTK_StimulationId_Label_00 = 33024
OVTK_StimulationId_Label_01 = 33025
OVTK_StimulationId_Label_07 = 33031

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
upperCase = True
####################################################################

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        self.initOutputs() # Set output stimulation headers

        # Called once when starting the scenario
        self.loopCounter = 0
        self.target = [0,0]
        self.selection = [0,0]
    	self.rowIndex = 0
    	self.colIndex = 0
        self.hashTable = {12:5,11:4,10:3,9:2,8:1,7:0,6:6,5:7,4:8,3:9,2:10,1:11}

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
        self.widget = user_input.TextWidget('', 0, int(widgetPositionY), int(width), int(widgetHeight), self.batch)
        self.text_input = ""
        self.widget.caret.on_text(self.text_input)
        self.current_text = "" 
        if(upperCase):
            text = textUC
        else:
            text = textLC
        self.alphabet = "NEUROSPELL"
        self.numberalph = 0

        #set up user keyboard matrix
        self.matrix = []
        for j in range(0, len(text) ):
            row = []
            for i in range(0, len(text[j]) ):
                line = text[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5)
                xpos = i*width/6
                temp = pyglet.text.Label(line, 
                    font_name='Courier New',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
                row.append(temp)
            self.matrix.append(row)

        #set up window rendering
        self.win.dispatch_events()
        self.win.flip()
        return

    def endExperiment(self):
        print("Quitting experiment.")
        self.sendOutput(0, OVTK_StimulationId_Label_00)
        self.win.close()
        return 

    def drawTarget(self, rowStim, colStim):
        if (isDrawTarget):
            rowNum = rowStim - OVTK_StimulationId_Label_01
            colNum = colStim - OVTK_StimulationId_Label_07
            x = colNum * width / 6
            y = (5-rowNum) * (keyboardPositionTop/5)
            primitives.drawRect(x, y, targetSize[0], targetSize[1], targetColour[0],targetColour[1],targetColour[2],targetColour[3])
        return

    def startFlash(self, rowcol):
        # If column
        if (rowcol <= 5 and isDrawVertFlash):
            if (isEnlargeTextMode):
                c = rowcol
                for r in range(0, len(self.matrix)):
                    self.matrix[r][c].font_size = keyboardEnlargeFontSize
                    self.matrix[r][c].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
            if (isHighlightTextMode):
                primitives.drawRect(rowcol*width/6, 0, vertFlashSize[0], vertFlashSize[1], vertFlashColour[0],vertFlashColour[1],vertFlashColour[2],vertFlashColour[3])
        # If row
        elif (rowcol <= 11 and isDrawHorizFlash):
            if (isEnlargeTextMode):
                r = rowcol%6
                for c in range(0, len(self.matrix[r])):
                    self.matrix[r][c].font_size = keyboardEnlargeFontSize
                    self.matrix[r][c].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
            if (isHighlightTextMode):
                primitives.drawRect(0, rowcol%6*height/12, horizFlashSize[0], horizFlashSize[1], horizFlashColour[0], horizFlashColour[1], horizFlashColour[2], horizFlashColour[3])
        return

    def stopFlash(self, rowcol):
        if (isEnlargeTextMode == False): 
            return # No need to stopFlash if text is not enlarged

        # If column
        if (rowcol <= 5 and isDrawVertFlash):
            c = rowcol
            for r in range(0, len(self.matrix)):
                self.matrix[r][c].font_size = keyboardFontSize
                self.matrix[r][c].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
        # If row
        elif (rowcol <= 11 and isDrawHorizFlash):
            r = rowcol%6
            for c in range(0, len(self.matrix[r])):
                self.matrix[r][c].font_size = keyboardFontSize
                self.matrix[r][c].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
        return 
    
    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        self.win.dispatch_events()
        # Stop 
        if self.win.has_exit:
            self.endExperiment()
        # Fast forward
        if (self.keys[key.F]):
            self.sendOutput(1, OVTK_StimulationId_Label_00)
        # Play 
        if (self.keys[key.P]):
            self.sendOutput(2, OVTK_StimulationId_Label_00)

        # Read flashes
        for chunkIndex in range( len(self.input[0]) ):
            chunk = self.input[0].pop()
            if (type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim = chunk.pop(0)
                    newStim = stim.identifier
                    # Aim row/column flash
                    if (33025 <= newStim and newStim <= 33036):
                        self.flash = self.hashTable[newStim - OVTK_StimulationId_Label_00]
                    # Start flash
                    elif (newStim == 32779): 
                        self.startFlash(self.flash)
                        # Draw 
                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
                        #self.batch.draw() 
                        for r in range (0,len(self.matrix)):
                            for c in range(0, len(self.matrix[r])):
                                self.matrix[r][c].draw()
                        self.win.flip()
                    # Stop flash
                    elif (newStim == 32780):
                        self.stopFlash(self.flash)
                        # Draw 
                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
                        #self.batch.draw() 
                        for r in range (0,len(self.matrix)):
                            for c in range(0, len(self.matrix[r])):
                                self.matrix[r][c].draw()
                        self.win.flip()
    
        # Read target
        for chunkIndex in range( len(self.input[1]) ):
            chunk = self.input[1].pop()
            if(type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop(0); # OMGGGGGGG WHAT A CRAZY DETAIL JUN SHERN YOU'RE A GENIUS.
                    if (33025 <= stim.identifier and stim.identifier <= 33030): # Row
                        self.target[0] = stim.identifier
                    elif (33031 <= stim.identifier and stim.identifier <= 33036): # Column
                        self.target[1] = stim.identifier
                        # Only draw target upon registering new column, so the pair will be complete
                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
                        self.drawTarget(self.target[0]-OVTK_StimulationId_Label_01, self.target[1]-OVTK_StimulationId_Label_07)
                        #self.batch.draw() 
                        # for r in range (0,len(self.matrix)):
                        #     for c in range(0, len(self.matrix[r])):
                        #         self.matrix[r][c].draw()
                        self.win.flip()
                        #print("Target", self.target[0], " ", self.target[1])

        # """
        # if self.win.has_exit:
        #     self.endExperiment()
        # else:
            
        #     print("Running loop")
        #     # Read target 
        #     for chunkIndex in range( len(self.input[1]) ):
        #         self.win.dispatch_events()
        #         chunk = self.input[1].pop()
        #         if(type(chunk) == OVStimulationSet):
        #             for stimIdx in range(len(chunk)):
        #                 stim=chunk.pop();
        #                 if (33025 <= stim.identifier and stim.identifier <= 33030): # Row
        #                     self.target[0] = stim.identifier
        #                 elif (33031 <= stim.identifier and stim.identifier <= 33036): # Column
        #                     self.target[1] = stim.identifier
        #                 self.drawTarget(self.target[0]-OVTK_StimulationId_Label_01, self.target[1]-OVTK_StimulationId_Label_07)
        #                 print("Target", self.target[0], " ", self.target[1])
            

        #     # Read flashes
    	   #  for chunkIndex in range( len(self.input[0]) ):
    	   #  	chunk = self.input[0].pop()
        #         if (type(chunk) == OVStimulationSet):
        #             for stimIdx in range(len(chunk)):
        #                 stim = chunk.pop()
        #                 newStim = stim.identifier
        #                 # Aim row/column flash
        #                 if (33025 <= newStim and newStim <= 33036):
        #                     self.flash = self.hashTable[newStim - OVTK_StimulationId_Label_00]
        #                 # Start flash
        #                 elif (newStim == 32779): 
        #                     self.startFlash(self.flash)
        #                 # Stop flash
        #                 elif (newStim == 32780):
        #                     self.stopFlash(self.flash)
        #                 #print("Flash", newStim)
            
        #     # Read row selection
        #     for chunkIndex in range( len(self.input[2]) ):
        #         chunk = self.input[2].pop()
        #         if(type(chunk) == OVStimulationSet):
        #             for stimIdx in range(len(chunk)):
        #                 stim=chunk.pop()
        #                 self.selection[0] = stim.identifier
        #                 self.rowIndex = self.selection[0] - OVTK_StimulationId_Label_01
        #                 print("Row select", stim.identifier)
                        
        #     # Read column selection
        #     for chunkIndex in range( len(self.input[3]) ):
        #         chunk = self.input[3].pop()
        #         if(type(chunk) == OVStimulationSet):
        #             for stimIdx in range(len(chunk)):
        #                 stim=chunk.pop();
        #                 self.selection[1] = stim.identifier
        #                 self.colIndex = self.selection[1] - OVTK_StimulationId_Label_07
        #                 print("Column select", stim.identifier)
        #     """
        #     """
        #     self.current_text = self.current_text + self.text_input
        #     self.widget.caret.on_text(self.text_input)
        #     self.text_input = ""

        #     if (self.keys[key.A]):
        #         self.text_input = self.alphabet[self.numberalph]
        #         self.current_text = self.current_text + self.text_input
        #         self.widget.caret.on_text(self.text_input)
        #         self.text_input = ""
        #         self.numberalph += 1
        #         self.numberalph = self.numberalph % 10

        #     ## Predictive text
        #     corrected_text = [".", ",", "@"] #word_predictor.correct(self.current_text)
        #     ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
        #     xpos  = 0*width/6
        #     temp0 = pyglet.text.Label(corrected_text[0], 
        #             font_name='Courier New',
        #             font_size=keyboardFontSize,
        #             color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
        #             x=xpos, y=ypos,
        #             anchor_x='left', anchor_y='bottom')
           
        #     ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
        #     xpos  = 1*width/6
        #     temp1 = pyglet.text.Label(corrected_text[1], 
        #             font_name='Courier New',
        #             font_size=keyboardFontSize,
        #             color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
        #             x=xpos, y=ypos,
        #             anchor_x='left', anchor_y='bottom')
            
        #     ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
        #     xpos  = 2*width/6
        #     temp2 = pyglet.text.Label(corrected_text[2], 
        #             font_name='Courier New',
        #             font_size=keyboardFontSize,
        #             color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
        #             x=xpos, y=ypos,
        #             anchor_x='left', anchor_y='bottom')
        #     self.matrix[0][0] = temp0
        #     self.matrix[0][1] = temp1
        #     self.matrix[0][2] = temp2
        # """
            
        #     # Pyglet/GL updates        
        #     #self.win.dispatch_events()
        #     """
        #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
        #     self.batch.draw() 
        #     # Draw keyboard matrix
        #     for r in range (0,len(self.matrix)):
        #         for c in range(0, len(self.matrix[r])):
        #             self.matrix[r][c].draw()
            
            
        #     self.win.flip()
            
        #     self.loopCounter += 1
        #     """   
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

box = MyOVBox()
