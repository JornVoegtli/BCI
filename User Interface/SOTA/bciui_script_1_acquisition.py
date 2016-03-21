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
    # Called once when starting the scenario
        # Display class
        self.disp = display.MyPyglet()
        self.disp.loadingScreen()
        self.disp.update()

        # Operation variables
        self.loopCounter = 0
        self.target = [0,0]
        self.flash = 0 # Arbitrary initial flash value - won't be seen
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
        return

    def endExperiment(self):
        print("Quitting experiment.")
        self.sendOutput(1, 32770) # Experiment STOP 
        self.closeOutputs()
        self.disp.win.close()
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

    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        self.disp.win.dispatch_events()

        if self.disp.win.has_exit:
            self.endExperiment()
        else:
            self.disp.clear()
            # Show a target for the first target
            if (self.loopCounter <= targetDelay):
                if (self.loopCounter == 0):
                    self.getNextTarget()
                    self.sendOutput(2, self.target[0])
                    self.sendOutput(2, self.target[1])
                self.disp.stopFlash(self.flash)
                self.disp.drawTarget(self.target[0], self.target[1])
                self.disp.drawMatrix()
                self.disp.drawTextBox() 
                self.disp.update()

            # Flash for the next (flashDuration) loops
            elif (self.loopCounter <= targetDelay + flashDuration):
                newStim = self.readFlash()
                # Aim row/column flash
                if (33025 <= newStim and newStim <= 33036):
                    self.flash = self.hashTable[newStim - OVTK_StimulationId_Label_00]
                # Start flash
                elif (newStim == 32779): 
                    self.disp.startFlash(self.flash)
                # Stop flash
                elif (newStim == 32780):
                    self.disp.stopFlash(self.flash)
                self.disp.drawMatrix()
                self.disp.drawTextBox() 
                self.disp.update()
                self.sendOutput(1, newStim)
                # Reset counter on last loop
                if (self.loopCounter == targetDelay + flashDuration): 
                    self.loopCounter = -1

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
