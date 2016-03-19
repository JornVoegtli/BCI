#c:/"program files (x86)"/openvibe/openvibe-designer
from __future__ import division, print_function, unicode_literals
import os, sys
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import primitives
import user_input
import random
from random import randint
import string
import ctypes
from controls import *

text = textUC # Defined in controls.py

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        # Called once when starting the scenario
        self.loopCounter = 0
        self.target = [0,0]
        self.flash = 33000 # Arbitrary initial flash value - won't be seen
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
        
        #set up user keyboard matrix
        self.matrix = []
        for j in range(0, len(text) ):
            row = []
            for i in range(0, len(text[j]) ):
                line = text[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5)
                xpos = i*width/6 + width/40 
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
        self.sendOutput(0, 32770) # Experiment STOP
        self.closeOutputs()
        self.win.close()
        return 

    def readFlash(self):
        if len(self.flashes) < 1:
            print("Reached end of flashes file.")
            self.endExperiment()
        else:
            return self.flashes.pop(0)
        return None

    def getNextTarget(self):
        if len(self.targets) < 1:
            print("Reached end of target file.")
            self.endExperiment()
        else:
            self.target[0] = self.targets.pop(0) 
            self.target[1] = self.targets.pop(0)
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background

        if self.win.has_exit:
            self.endExperiment()
        else:
            # Show a target for the first target
            if (self.loopCounter <= targetDelay):
                if (self.loopCounter == 0):
                    self.getNextTarget()
                    self.sendOutput(2, self.target[0])
                    self.sendOutput(2, self.target[1])
                self.stopFlash(self.flash)
                self.drawTarget(self.target[0], self.target[1])

            # Flash for the next (flashDuration) loops
            elif (self.loopCounter <= targetDelay + flashDuration):
                newStim = self.readFlash()
                # Aim row/column flash
                if (33025 <= newStim and newStim <= 33036):
                    self.flash = self.hashTable[newStim - OVTK_StimulationId_Label_00]
                # Start flash
                elif (newStim == 32779): 
                    self.startFlash(self.flash)
                # Stop flash
                elif (newStim == 32780):
                    self.stopFlash(self.flash)

                self.sendOutput(1, newStim)
                # Reset counter on last loop
                if (self.loopCounter == targetDelay + flashDuration): 
                    self.loopCounter = -1

            # Draw keyboard matrix
            for r in range (0,len(self.matrix)):
                for c in range(0, len(self.matrix[r])):
                    self.matrix[r][c].draw()
            
            # Pyglet/GL updates        
            self.batch.draw() 

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

box = MyOVBox()
