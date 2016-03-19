import pygame
import ctypes
import random
import os, sys
# -*- coding: utf-8 -*-
# coding: utf-8
class MyOVBox():
		
    def initialize(self): # Called once when starting the scenario
        self.count = 0
        self.target = [0,0]

        #SSVEP timers
        self.timerL = 0
        self.timerM = 0
        self.timerR = 0

        #SSVEP color states
        self.colorStateL = True
        self.colorStateM = True
        self.colorStateR = True

        # Pygame
        pygame.init()	
        self.displaySetup()    
        return
            
    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
        self.count = self.count % 10
        self.count += 1
	# Listen for rows/columns
        rc_stim = self.getChunk(0)
        if rc_stim:
            self.displayUpdate(rc_stim.identifier)
		# Listen for target
		#target_stim = self.getChunk(1)
        #if target_stim:
        #    print target_stim.identifier
        return
    
    def displaySetup(self):
        user32 = ctypes.windll.user32
        self.width = user32.GetSystemMetrics(0)-100 #img.get_rect().size[0] #
        self.height = user32.GetSystemMetrics(1)-100 #img.get_rect().size[1] + 60*num_devices 
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE) #pygame.FULLSCREEN
        self.pFont = pygame.font.SysFont("monospace", self.width/30, True)
        self.bigFont = pygame.font.SysFont("monospace", self.width/24, True)

        self.bg_color = pygame.Color(15,15,15)
        self.screen.fill(self.bg_color)
	
	
		
    def drawHighlight(self, label):
        color = pygame.Color(80,80,80)
        if label < 6:
            pygame.draw.rect(self.screen, color, pygame.Rect(label*self.width/6,self.height/2,self.width/6,self.height))
        elif label < 12:
            pygame.draw.rect(self.screen, color, pygame.Rect(0,label%6*self.height/6 + self.height/2,self.width,self.height/12))
    
    def drawSSVEPHighlightL(self):
        self.timerL += 1
        if (self.colorStateL):
            color = pygame.Color(255,0,0)
        else:
            color = pygame.Color(39,40,34)

        if(self.timerL == 3):  #F = 10 Hz
            self.timerL = 0
            if(self.colorStateL):
                self.colorStateL = False
            else:
                self.colorStateL = True

        pygame.draw.rect(self.screen, color, pygame.Rect(0,0,self.width/3,self.height/12))
       
        

    def drawSSVEPHighlightM(self):
        self.timerM += 1
        if (self.colorStateM):
            color = pygame.Color(0,255,0)
        else:
            color = pygame.Color(39,40,34)

        if(self.timerM == 2):  #F = 15Hz
            self.timerM = 0
            if(self.colorStateM):
                self.colorStateM = False
            else:
                self.colorStateM = True

        pygame.draw.rect(self.screen, color, pygame.Rect(self.width/3,0,self.width/3,self.height/12))


    def drawSSVEPHighlightR(self):
        self.timerR += 1
        if (self.colorStateR):
            color = pygame.Color(0,0,255)
        else:
            color = pygame.Color(39,40,34)

        if(self.timerR == 1):  #F = 30Hz
            self.timerR = 0
            if(self.colorStateR):
                self.colorStateR = False
            else:
                self.colorStateR = True

        pygame.draw.rect(self.screen, color, pygame.Rect(2*self.width/3,0,self.width/3,self.height/12))

    def drawTarget(self, target):
        i = target[0]
        j = target[1]
        pygame.draw.rect(self.screen, (60,180,160), pygame.Rect(i*self.width/6 ,j*self.height/12 + self.height/2,self.width/6,self.height/12))

    def drawSSVEPText(self):
        SStext = ['Actually','B','C']
        
        for i in range(0, len(SStext) ):
            r = self.pFont.render(SStext[i], 1, (255,255,255))
            w, h = self.pFont.size(SStext[i])
            xpos = i*self.width/3 + (self.width/3 - w) /2
            ypos = self.height/100
            self.screen.blit(r, (xpos,ypos))            
		
    def drawText(self, label):  
        # u"\u2191" up arrow u"\u25B2"
        # u"\u2192" right arrow u"\u25B6"
        # u"\u2190" left arrow u"\u25C0"
        # u"\u2193" down arrow u"\u25BC"
        # u"\u21E6" backspace u"\u2190"
        # u"\u21A9" enter
        text = [ ['A','B','C','D','E','F'], 
                ['G','H','I','J','K','L'], 
                ['M','N','O','P','Q','R'], 
                ['S','T','U','V','W','X'], 
                ['Y','Z','0','1','2','3'], 
                ['4','5','6','7','8', u"\u2191"] ]

        for j in range(0, len(text) ):
            for i in range(0, len(text[j]) ):
                if (i == label) or (j == label-6):
                    r = self.bigFont.render(text[j][i], 1, (255,255,255))
                    w, h = self.bigFont.size(text[j][i])
                else:
                    r = self.pFont.render(text[j][i], 1, (200,200,200))
                    w, h = self.pFont.size(text[j][i])

                xpos = self.width/12 + i*self.width/6
                ypos = self.height/2 + j*self.height/12
                self.screen.blit(r, (xpos,ypos))

    def displayUpdate(self, label):
        label -= 33024 # Start from 0
        self.screen.fill((39,40,34))
        pygame.draw.rect(self.screen, (20,20,20), pygame.Rect(self.width/12,self.height/2,self.width,self.height/2))
        
        self.drawHighlight(label)
        self.drawSSVEPHighlightL()
        self.drawSSVEPHighlightM()
        self.drawSSVEPHighlightR()
        self.target[0] = 0
        self.target[1] = 0
        self.drawTarget(self.target)
        self.drawText(label)
        self.drawSSVEPText()
        pygame.display.update()
        
        

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
        return
		
box = MyOVBox()
running = True
#user32 = ctypes.windll.user32
#print "width", user32.GetSystemMetrics(0)/2 
#print "height", user32.GetSystemMetrics(1)/2 
clock = pygame.time.Clock()
box.initialize()
box.displaySetup()
while(running):	
    box.displayUpdate(33024)
    clock.tick(60)
    #print "fps:", clock.get_fps()

    for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False