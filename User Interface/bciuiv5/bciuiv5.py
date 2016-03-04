import os, sys
import word_display
import pygame
import random
import string

class MyOVBox(): # MyOVBox(OVBox):
#    def __init__(self):
#        OVBox.__init__(self)
            
    def initialize(self): # Called once when starting the scenario
        self.count = 0
        self.target = [0,0]
        self.label = 33024 + random.randint(0,11)
        self.textstring = ""
        self.textmode = 1
        self.keepWriting = 1 
        # Pygame
        #word_display.displaySetup()    
        return
            
    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        #print "fps:", clock.get_fps()
        self.count += 1
        self.count = self.count % 20
        if (self.count == 0):
            # Listen for rows/columns
            #rc_stim = self.getChunk(0)
            #if rc_stim:
            #    self.displayUpdate(rc_stim.identifier)
            self.label = random.randint(0,11) + 33024
            if (random.randint(0,9) == 9):
                # Listen for target
                #target_stim = self.getChunk(1)
                #if target_stim:
                #    print target_stim.identifier
                self.target[0] = random.randint(0,5)
                self.target[1] = random.randint(0,5)
        word_display.displayUpdate(self.target,self.keepWriting,self.textstring, self.textmode, self.label)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Check if key is one of possible inputs
                keyname = pygame.key.name(event.key)
                if(self.keepWriting):
                    if keyname in list(string.printable):
                        self.textstring = self.textstring + chr(ord(keyname) - 32*box.textmode)
                    elif keyname == 'space':
                        self.textstring = self.textstring + " "
                if keyname == 'backspace':
                    self.textstring = self.textstring[:-1]
                elif keyname == 'left ctrl':
                    self.textmode = 1 - self.textmode
                elif event.key == pygame.K_ESCAPE:
                    self.uninitialize()
        return
    
 
    def getChunk(self, inputNum):
        for chunkIndex in range( len(self.input[0]) ):
            chunk = self.input[inputNum].pop()
            if(type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop();
                    return stim
        return None
            
    def uninitialize(self): # Called once when stopping the scenario
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        return



box = MyOVBox()
running = True
#user32 = ctypes.windll.user32
#print "width", user32.GetSystemMetrics(0)/2 
#print "height", user32.GetSystemMetrics(1)/2 
clock = pygame.time.Clock()
box.initialize()
while(running):	
    box.process()
    #box.displayUpdate(33028)
    clock.tick(60)
    #print "fps:", clock.get_fps()
