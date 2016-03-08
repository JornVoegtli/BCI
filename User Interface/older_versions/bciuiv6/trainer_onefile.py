import os, sys
#import display
#import predictor
import random
import string
#import io # IO methods for non-OpenVibe
#sys.path.append(r"/home/junshern/OpenVibe/PythonBox") # Path to modules
import pygame
import ctypes
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
    
def predictText(string):
    words = string.split(' ')
    if len(words[-1]) > 0: 
        w1 = correct(words[-1])
        w2 = words[-1] + 'ing'
        w3 = words[-1] + 'ed'
    else:
        rick = "never gonna give" # you up
        [w1,w2,w3] = rick.split(' ')
    return [w1, w2, w3]

# Display
class Display(object):

    def __init__(self):
        pygame.init()
        ## Display setup
        # Linux
        infoObject = pygame.display.Info()
        self.width = int(infoObject.current_w)
        self.height = int(infoObject.current_h)
        # Windows
        #user32 = ctypes.windll.user32
        #width = user32.GetSystemMetrics(0) 
        #height = user32.GetSystemMetrics(1)
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE) #pygame.FULLSCREEN) #pygame.RESIZABLE) 
        self.bg_color = pygame.Color(15,15,15)
        self.screen.fill(self.bg_color)

        ## Font stuff
        self.smallFont = pygame.font.SysFont("monospace", self.width/50, True)
        self.smallFontW, self.smallFontH = self.smallFont.size('A')
        self.pFont = pygame.font.SysFont("monospace", self.width/30, True)
        self.bigFont = pygame.font.SysFont("monospace", self.width/24, True)

        ## SSVEP stuff 
        self.freq_count = [0,0,0] # List of counter variables for each frequency
        self.colorState = [1,1,1] # List of color toggle states 
        

    def drawP300RowCol(self, rowcol):
        color = pygame.Color(80,80,80)
        if rowcol < 6:
            pygame.draw.rect(self.screen, color, pygame.Rect(rowcol*self.width/6,self.height/2,self.width/6,self.height))
        elif rowcol < 12:
            pygame.draw.rect(self.screen, color, pygame.Rect(0, rowcol%6*self.height/12+self.height/2, self.width,self.height/12))

    def drawP300Target(self, target):
        i = target[0]
        j = target[1]
        pygame.draw.rect(self.screen, (60,180,160), pygame.Rect(i*self.width/6 ,j*self.height/12 + self.height/2,self.width/6,self.height/12))

    def drawP300Text(self, caps_on, rowcol):  
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

        if caps_on == 1:
            text = textUC
        else:
            text = textLC
            
        for j in range(0, len(text) ):
            for i in range(0, len(text[j]) ):
                if (i == rowcol) or (j == rowcol-6):
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

    def drawP300(self, rowcol, target, caps_on):
        pygame.draw.rect(self.screen, (20,20,20), pygame.Rect(0,self.height/2,self.width,self.height/2))
        self.drawP300RowCol(rowcol)
        self.drawP300Target(target)
        self.drawP300Text(caps_on, rowcol)

    def flashSSVEP(self, index, color, freq):
        self.freq_count[index] += 1
        if (self.colorState[index]):
            c = color
        else:
            c = pygame.Color(20,20,20)
        pygame.draw.rect(self.screen, c, pygame.Rect(index*self.width/3,0,self.width/3,self.height/12))

        if (60 % freq != 0): # For now, chosen frequency can only be a factor of 60Hz
            print "Invalid freq!"
            uninitialize()
        elif (self.freq_count[index] == 30/freq):
            self.freq_count[index] = 0
            self.colorState[index] = 1 - self.colorState[index] # Toggle

    def drawSSVEP(self, SSwords):
        ## Flash boxes
        self.flashSSVEP(0, (0,150,230), 5)
        self.flashSSVEP(1, (100,220,200), 10)
        self.flashSSVEP(2, (255,150,0), 15)

        ## Draw text
        for i in range(0, len(SSwords) ): # For each word
            # Adjust font size based on word length
            if (len(SSwords[i]) > 15) :
                SSwordssize = 30 + 2*(len(SSwords[i])-15)
            else :
                SSwordssize = 30    
            SSfont = pygame.font.SysFont("monospace", self.width/SSwordssize, True)
            # Draw
            r = SSfont.render(SSwords[i], 1, (255,255,255))
            w, h = SSfont.size(SSwords[i])
            xpos = i*self.width/3 + (self.width/3 - w) /2
            ypos = self.height/100
            self.screen.blit(r, (xpos,ypos))            

    def writeText(self, keepWriting, text):
        max_lines = 5 # number of lines that can be displayed at a time
        max_chars = self.width/self.smallFontW - 8 # number of characters that can fit on a line; 4 taken off each end for padding
        max_charsTotal = max_chars*5
        wordsToMaxChar = max_chars*5 - len(text) 
        lineHeight = ((self.height/2) - (self.height/12)) / max_lines
        lineNum = 4
        if(len(text) > max_charsTotal ) :
            keepWriting = 0
            if(wordsToMaxChar != 0):
                text = text[:wordsToMaxChar]
        else:
            keepWriting = 1
        cursor_x = (self.width-(max_chars*self.smallFontW))/2 - self.smallFontW
        cursor_y = self.height/2 - self.height/12 - 4*lineHeight + self.smallFontH/2 
        while (len(text) > 0 and lineNum >= 0):
            # Draw the text line by line, starting from last line at the bottom, then moving up
            i = (len(text)-1) / max_chars # the -1 is necessary to make sure the division always falls short and floors
            line = text[:max_chars]
            text = text[max_chars:]
            # Render character by character
            n = 0
            for c in line:
                r = self.smallFont.render(c, 1, (200,200,200))
                xpos = (self.width-(max_chars*self.smallFontW))/2 + n*self.smallFontW
                ypos = self.height/2 - self.height/12 - lineNum*lineHeight + self.smallFontH/2
                cursor_x = xpos
                cursor_y = ypos
                self.screen.blit(r, (xpos,ypos))
                n += 1
            lineNum -= 1
        # Draw cursor
        pygame.draw.rect(self.screen, (60,180,160), (cursor_x+self.smallFontW*1.2, cursor_y, 3, self.smallFontH))

    def displayUpdate(self):
        # Draw borders
        pygame.draw.rect(self.screen, (255,255,255), (0, 0, self.width, 4))
        pygame.draw.rect(self.screen, (255,255,255), (0, self.height/12, self.width, 4))

        pygame.display.update()
        self.screen.fill(self.bg_color)

    def finish(self):
        pygame.display.quit()
        pygame.quit()


class MyOVBox(OVBox): #MyOVBox(): # MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)

    def initialize(self): 
        # P300 variables
        self.clkdiv = 0
        self.rowcol = random.randint(0,11)
        self.P300_target = [0,0]
        self.caps_on = 0
        # SSVEP target
        self.SSVEP_target = random.randint(0,2)
        # Text variables
        self.textstring = ""
        self.keepWriting = 1 
        # Instantiate display object
        self.dp = Display()
        # IO Preparation
        self.initOutputs() # Set output stimulation headers
        self.inputList = [0,0] # Prepare for two inputs
        return
        
    def process(self): 
        #self.updateInputs()

        ## P300
        self.clkdiv += 1
        self.clkdiv = self.clkdiv % 20
        if (self.clkdiv == 0):
            ## Row/Column flashing randomly
            self.rowcol = random.randint(0,11)
            ## Change target randomly
            if (random.randint(0,9) == 9): # Don't change too often; probability of changing target is 0.1
                self.P300_target[0] = random.randint(0,5)
                self.P300_target[1] = random.randint(0,5)
        self.dp.drawP300(self.rowcol, self.P300_target, self.caps_on)
        # Send target row/col stimulation
        self.sendOutput(0, STIMSTART)
        self.sendOutput(0, STIMLABELBASE+self.P300_target[0])
        self.sendOutput(0, STIMLABELBASE+self.P300_target[1])
        self.sendOutput(0, STIMEND)
        # Send True answer if row/col contains target
        if (self.rowcol < 6) and (self.rowcol == self.P300_target[0]):
            self.sendOutput(1, OVTK_StimulationId_Target)
        elif (self.rowcol >= 6) and (self.rowcol-6 == self.P300_target[1]):
            self.sendOutput(1, OVTK_StimulationId_Target)
        # Send False answer if row/col does not contain target
        else:
            self.sendOutput(1, OVTK_StimulationId_NonTarget)


        ## SSVEP
        pred_words = predictText(self.textstring)
        self.dp.drawSSVEP(pred_words)
        self.SSVEP_target = 1
        # Produce stimulations at the outputs
#        self.sendOutput(2, self.SSVEP_target)

        ## Write text on screen
        self.updateTextInput()
        self.dp.writeText(self.keepWriting, self.textstring)
 
        ## Update the display
        self.dp.displayUpdate()
                
        return

    def updateTextInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Check if key is one of possible inputs
                keyname = pygame.key.name(event.key)
                if(self.keepWriting):
                    if keyname in list(string.printable):
                        self.textstring = self.textstring + chr(ord(keyname) - 32*box.caps_on)
                    elif keyname == 'space':
                        self.textstring = self.textstring + " "
                if keyname == 'backspace':
                    self.textstring = self.textstring[:-1]
                elif keyname == 'left ctrl':
                    self.caps_on = 1 - self.caps_on
                elif event.key == pygame.K_ESCAPE:
                    self.uninitialize()
        return
    
    def uninitialize(self): 
        self.closeOutputs()
        self.dp.finish()
        sys.exit()
        return


    ## I/O methods for OpenVibe 
    def updateInputs(self):
        # Read from each of our inputs
        for index in range(len(self.input)):
            tmp = self.getChunk(index)
            if (tmp != None): self.inputList[index] = tmp.identifier # Update the input in inputList if there is a new stimulation

    def getChunk(self, inputNum):
        for chunkIndex in range( len(self.input[inputNum]) ):
            chunk = self.input[inputNum].pop()
            if(type(chunk) == OVStimulationSet):
                for stimIdx in range(len(chunk)):
                    stim=chunk.pop();
                    return stim
        return None

    def initOutputs(self):
        print "Number of outputs:", len(self.output)
        for index in range(len(self.output)):
            # OV protocol requires an output stim header; dates are 0
            self.output[index].append(OVStimulationHeader(0., 0.))
        
    def sendOutput(self, index, stimLabel):
        # A stimulation set is a chunk which starts at current time and end time is the time step between two calls
        stimSet = OVStimulationSet(self.getCurrentTime(), self.getCurrentTime()+1./self.getClock())
        stimSet.append( OVStimulation(stimLabel, self.getCurrentTime(), 0.) )
        self.output[index].append(stimSet)

    def closeOutputs(self):
        for index in range(len(self.output)):
            # OV protocol requires an output stim end
            end = self.getCurrentTime()
            self.output[index].append(OVStimulationEnd(end, end))


# Some constants 
STIMSTART = 32780
STIMEND = 32779
STIMLABELBASE = 33024
# Comment out during OpenVibe use since already defined
OVTK_StimulationId_NonTarget = 33286
OVTK_StimulationId_Target = 33285

# Predictor
NWORDS = train(words(file('/home/junshern/OpenVibe/PythonBox/big.txt').read())) # Use full path or OV will complain
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# OV
box = MyOVBox()
"""clock = pygame.time.Clock()
box.initialize()
while (True):	
    box.process()
    #box.displayUpdate(33028)
    clock.tick(60)
    #print "fps:", clock.get_fps()
"""
