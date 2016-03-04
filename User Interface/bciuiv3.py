import pygame
import ctypes
import random
import os, sys
import string
import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


class MyOVBox(): # MyOVBox(OVBox):
#    def __init__(self):
#        OVBox.__init__(self)
            
    def initialize(self): # Called once when starting the scenario
        self.count = 0
        self.target = [0,0]
        self.label = 33024 + random.randint(0,11)
        self.textstring = ""
        self.textmode = 1

        # Pygame
        pygame.init()	
        self.displaySetup()    
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
        self.displayUpdate(self.label)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Check if key is one of possible inputs
                keyname = pygame.key.name(event.key)
                if keyname in list(string.printable):
                    self.textstring = self.textstring + chr(ord(keyname) - 32*box.textmode)
                elif keyname == 'space':
                    self.textstring = self.textstring + " "
                elif keyname == 'backspace':
                    self.textstring = self.textstring[:-1]
                elif keyname == 'left ctrl':
                    self.textmode = 1 - self.textmode
                elif event.key == pygame.K_ESCAPE:
                    self.uninitialize()
        return
    
    def displaySetup(self):
        # Linux
        infoObject = pygame.display.Info()
        self.width = int(infoObject.current_w)
        self.height = int(infoObject.current_h)
        # Windows
        #user32 = ctypes.windll.user32
        #self.width = user32.GetSystemMetrics(0) - 100
        #self.height = user32.GetSystemMetrics(1)/2 - 100

        self.screen = pygame.display.set_mode((self.width,self.height), pygame.FULLSCREEN) #pygame.RESIZABLE)
        self.smallFont = pygame.font.SysFont("monospace", self.width/50, True)
        self.smallFontW, self.smallFontH = self.smallFont.size('A')
        self.pFont = pygame.font.SysFont("monospace", self.width/30, True)
        self.bigFont = pygame.font.SysFont("monospace", self.width/24, True)

        #SSVEP timers
        self.timer = [0,0,0] # List of the timers L, M and R
        self.timerL = 0

        #SSVEP color states
        self.colorState = [1,1,1] # List of color toggle states for L, M and R
        self.colorStateL = True

        self.bg_color = pygame.Color(15,15,15)
        self.screen.fill(self.bg_color)

    def drawP300Text(self, label):  
        
        textUC = [ ['A','B','C','D','E',u"\u2190"], 
                ['F','G','H','I','J','ENTER'], 
                ['K','L','M','N','O','abc'], 
                ['P','Q','R','S','T','123'], 
                ['U','V','W','X',u"\u25B2",'{&='], 
                ['Y','Z','SPACE',u"\u25C4",u"\u25BC", u"\u25BA"] ]

        textLC = [ ['a','b','c','d','e',u"\u2190"], 
                ['f','g','h','i','j','ENTER'], 
                ['k','l','m','n','o','ABC'], 
                ['p','q','r','s','t','123'], 
                ['u','v','w','x',u"\u25B2",'{&='], 
                ['y','z','SPACE',u"\u25C4",u"\u25BC", u"\u25BA"] ]

        if self.textmode == 1:
            text = textUC
        else:
            text = textLC
            
        for j in range(0, len(text) ):
            for i in range(0, len(text[j]) ):
                if (i == label) or (j == label-6):
                    r = self.bigFont.render(text[j][i], 1, (255,255,255))
                    w, h = self.bigFont.size(text[j][i])
                else:
                   # if (text == textLC and i == 5 and j == 2) : #make abc button highlight when lower case is chosen?
                       # r = self.pFont.render(text[j][i], 1, (0,0,255)) #it might screw the BCI system so leave out first
                  #  else:
                    r = self.pFont.render(text[j][i], 1, (200,200,200))
                    w, h = self.pFont.size(text[j][i])

                xpos = i*self.width/6 + (self.width/6 - w) /2
                ypos = self.height/2 + j*self.height/12 + self.height/24 - h/2
                self.screen.blit(r, (xpos,ypos))

    def drawP300Highlight(self, label):
        color = pygame.Color(80,80,80)
        if label < 6:
            pygame.draw.rect(self.screen, color, pygame.Rect(label*self.width/6,self.height/2,self.width/6,self.height))
        elif label < 12:
            pygame.draw.rect(self.screen, color, pygame.Rect(0, label%6*self.height/12+self.height/2, self.width,self.height/12))

    def drawP300Target(self, target):
        i = target[0]
        j = target[1]
        pygame.draw.rect(self.screen, (60,180,160), pygame.Rect(i*self.width/6 ,j*self.height/12 + self.height/2,self.width/6,self.height/12))

    def drawSSVEPHighlight(self, index, color, freq):
        self.timer[index] += 1
        if (self.colorState[index]):
            c = color
        else:
            c = pygame.Color(20,20,20)
        pygame.draw.rect(self.screen, c, pygame.Rect(index*self.width/3,self.height/2-self.height/12,self.width/3,self.height/12))

        if (60 % freq != 0): # For now, chosen frequency can only be a factor of 60Hz
            print "Invalid freq!"
            self.uninitialize()
        elif (self.timer[index] == 30/freq):
            self.timer[index] = 0
            self.colorState[index] = 1 - self.colorState[index] # Toggle

    def drawSSVEPText(self, SStext):
        for i in range(0, len(SStext) ): # For each word
            # Adjust font size based on word length
            if (len(SStext[i]) > 15) :
                SStextsize = 30 + 2*(len(SStext[i])-15)
            else :
                SStextsize = 30    
            SSpFont = pygame.font.SysFont("monospace", self.width/SStextsize, True)
            # Draw
            r = SSpFont.render(SStext[i], 1, (255,255,255))
            w, h = SSpFont.size(SStext[i])
            xpos = i*self.width/3 + (self.width/3 - w) /2
            ypos = self.height/2 - self.height/24 - h/2
            self.screen.blit(r, (xpos,ypos))            

    def predictText(self, string):
        words = string.split(' ')
        if len(words[-1]) > 0: 
            w1 = correct(words[-1])
            w2 = words[-1] + 'ing'
            w3 = words[-1] + 'ed'
        else:
            rick = "never gonna give" # you up
            [w1,w2,w3] = rick.split(' ')
        return [w1, w2, w3]

    def writeText(self, text):
        max_lines = 5 # number of lines that can be displayed at a time
        max_chars = self.width/self.smallFontW - 8 # number of characters that can fit on a line; 4 taken off each end for padding
        
        lineHeight = ((self.height/2) - (self.height/12)) / max_lines

        lineNum = 1
        cursor_x = (self.width-(max_chars*self.smallFontW))/2 - self.smallFontW
        cursor_y = self.height/2 - self.height/12 - lineHeight + self.smallFontH/2 
        while (len(text) > 0 and lineNum <= max_lines):
            # Draw the text line by line, starting from last line at the bottom, then moving up
            i = (len(text)-1) / max_chars # the -1 is necessary to make sure the division always falls short and floors
            line = text[i*max_chars:]
            text = text[:i*max_chars] 

            # Render character by character
            n = 0
            for c in line:
                r = self.smallFont.render(c, 1, (200,200,200))
                xpos = (self.width-(max_chars*self.smallFontW))/2 + n*self.smallFontW
                ypos = self.height/2 - self.height/12 - lineNum*lineHeight + self.smallFontH/2
                if lineNum == 1:
                    cursor_x = xpos
                    cursor_y = ypos
                self.screen.blit(r, (xpos,ypos))
                n += 1
            lineNum += 1
        # Draw cursor
        pygame.draw.rect(self.screen, (60,180,160), (cursor_x+self.smallFontW*1.2, cursor_y, 3, self.smallFontH))

    def displayUpdate(self, label):
        self.screen.fill(self.bg_color)

        # P300
        label -= 33024 # Start from 0
        pygame.draw.rect(self.screen, (20,20,20), pygame.Rect(0,self.height/2,self.width,self.height/2))
        self.drawP300Highlight(label)
        self.drawP300Target(self.target)
        self.drawP300Text(label)
        
        # SSVEP 
        self.drawSSVEPHighlight(0, (0,150,230), 5)
        self.drawSSVEPHighlight(1, (100,220,200), 10)
        self.drawSSVEPHighlight(2, (255,150,0), 15)
        pred_words = self.predictText(self.textstring)
        self.drawSSVEPText(pred_words)

        # Draw borders
        pygame.draw.rect(self.screen, (255,255,255), (0, self.height/2, self.width, 4))
        pygame.draw.rect(self.screen, (255,255,255), (0, self.height/2-self.height/12, self.width, 4))
        # Text output
        self.writeText(self.textstring)

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
        sys.exit()
        return

# Autocorrect
NWORDS = train(words(file('big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

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
