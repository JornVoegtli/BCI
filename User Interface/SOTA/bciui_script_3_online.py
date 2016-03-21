#c:/"program files (x86)"/openvibe/openvibe-designer
from __future__ import division, print_function, unicode_literals
import os, sys
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import random
import string
import ctypes
from controls import *
import display

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): 
        self.initOutputs() # Set output stimulation headers

        # Called once when starting the scenario
        self.target = [0,0]
        self.selection = [33034,33034]
    	self.rowIndex = 0
    	self.colIndex = 0
        self.hashTable = {12:5,11:4,10:3,9:2,8:1,7:0,6:6,5:7,4:8,3:9,2:10,1:11}

        # Display class
        self.disp = display.MyPyglet()
        self.disp.loadingScreen()
        self.disp.update()

        # I/O
        self.initOutputs() # Set output stimulation headers
        return

    def endExperiment(self):
        print("Quitting experiment.")
        self.sendOutput(0, 32770)
        self.closeOutputs()
        self.disp.win.close()
        return 

    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        self.disp.win.dispatch_events()
        # Stop 
        if self.disp.win.has_exit:
            self.endExperiment()
        # Fast forward
        if (self.disp.keys[key.F]):
            self.sendOutput(0, OVTK_StimulationId_Label_00)
        # Play 
        if (self.disp.keys[key.P]):
            self.sendOutput(0, OVTK_StimulationId_Label_01)

        # Read flashes
        for chunkIndex in range( len(self.input[0]) ):
            chunk = self.input[0].pop()
            if (type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim = chunk.pop(0) # OMGGGGGGG WHAT A CRAZY DETAIL JUN SHERN YOU'RE A GENIUS.
                    newStim = stim.identifier
                    # Aim row/column flash
                    if (33025 <= newStim and newStim <= 33036):
                        self.flash = self.hashTable[newStim - OVTK_StimulationId_Label_00]
                    # Start flash
                    elif (newStim == 32779): 
                        self.disp.clear()
                        self.disp.drawTextBox()
                        self.disp.drawMatrix()
                        self.disp.startFlash(self.flash)
                        # Draw 
                        self.disp.update()
                    # Stop flash
                    elif (newStim == 32780):
                        self.disp.clear()
                        self.disp.stopFlash(self.flash)
                        # Draw 
                        self.disp.drawTextBox()
                        self.disp.drawMatrix()
                        self.disp.update()

        # Read row selection
        for chunkIndex in range( len(self.input[2]) ):
            chunk = self.input[2].pop()
            if(type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop(0)
                    if (33025 <= stim.identifier and stim.identifier <= 33030): # Row
                        self.selection[0] = stim.identifier
                        # Only draw target upon registering new ROW, so the pair will be complete - This is special! Column is received before row
                        self.disp.clear()
                        self.disp.drawTarget(self.selection[0], self.selection[1]) # Drawing selection actually, but same la
                        print("Selection", self.selection)
                        self.disp.makeSelection(self.selection)
                        self.disp.drawTextBox() 
                        self.disp.drawMatrix()
                        self.disp.update()
        
        # Read column selection
        for chunkIndex in range( len(self.input[3]) ):
            chunk = self.input[3].pop()
            if(type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop(0);
                    if (33031 <= stim.identifier and stim.identifier <= 33036): # Column
                        self.selection[1] = stim.identifier
                        #print("Column select", stim.identifier)
		
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
