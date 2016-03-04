import word_predictor
import pygame
import ctypes
import random
import string

#def displaySetup():
    #Linux
    #infoObject = pygame.display.Info()
    #width = int(infoObject.current_w)
    #height = int(infoObject.current_h)
    #Windows
    
pygame.init()
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0) 
height = user32.GetSystemMetrics(1) 

screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN) #pygame.RESIZABLE) 
smallFont = pygame.font.SysFont("monospace", width/50, True)
smallFontW, smallFontH = smallFont.size('A')
pFont = pygame.font.SysFont("monospace", width/30, True)
bigFont = pygame.font.SysFont("monospace", width/24, True)

#SSVEP timers
timer = [0,0,0] # List of the timers L, M and R

#SSVEP color states
colorState = [1,1,1] # List of color toggle states for L, M and R

bg_color = pygame.Color(15,15,15)
screen.fill(bg_color)

def drawP300Text(textmode, label):  
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

    if textmode == 1:
        text = textUC
    else:
        text = textLC
        
    for j in range(0, len(text) ):
        for i in range(0, len(text[j]) ):
            if (i == label) or (j == label-6):
                r = bigFont.render(text[j][i], 1, (255,255,255))
                w, h = bigFont.size(text[j][i])
            else:
               # if (text == textLC and i == 5 and j == 2) : #make abc button highlight when lower case is chosen?
                   # r = pFont.render(text[j][i], 1, (0,0,255)) #it might screw the BCI system so leave out first
              #  else:
                r = pFont.render(text[j][i], 1, (200,200,200))
                w, h = pFont.size(text[j][i])

            xpos = i*width/6 + (width/6 - w) /2
            ypos = height/2 + j*height/12 + height/24 - h/2
            screen.blit(r, (xpos,ypos))

def drawP300Highlight( label):
    color = pygame.Color(80,80,80)
    if label < 6:
        pygame.draw.rect(screen, color, pygame.Rect(label*width/6,height/2,width/6,height))
    elif label < 12:
        pygame.draw.rect(screen, color, pygame.Rect(0, label%6*height/12+height/2, width,height/12))

def drawP300Target( target):
    i = target[0]
    j = target[1]
    pygame.draw.rect(screen, (60,180,160), pygame.Rect(i*width/6 ,j*height/12 + height/2,width/6,height/12))

def drawSSVEPHighlight( index, color, freq):
    timer[index] += 1
    if (colorState[index]):
        c = color
    else:
        c = pygame.Color(20,20,20)
    pygame.draw.rect(screen, c, pygame.Rect(index*width/3,0,width/3,height/12))

    if (60 % freq != 0): # For now, chosen frequency can only be a factor of 60Hz
        print "Invalid freq!"
        uninitialize()
    elif (timer[index] == 30/freq):
        timer[index] = 0
        colorState[index] = 1 - colorState[index] # Toggle

def drawSSVEPText( SStext):
    for i in range(0, len(SStext) ): # For each word
        # Adjust font size based on word length
        if (len(SStext[i]) > 15) :
            SStextsize = 30 + 2*(len(SStext[i])-15)
        else :
            SStextsize = 30    
        SSpFont = pygame.font.SysFont("monospace", width/SStextsize, True)
        # Draw
        r = SSpFont.render(SStext[i], 1, (255,255,255))
        w, h = SSpFont.size(SStext[i])
        xpos = i*width/3 + (width/3 - w) /2
        ypos = height/100
        #half screen
        #xpos = i*width/3 + (width/3 - w) /2
        #ypos = height/2 - height/24 - h/2
        screen.blit(r, (xpos,ypos))            

def predictText( string):
    words = string.split(' ')
    if len(words[-1]) > 0: 
        w1 = word_predictor.correct(words[-1])
        w2 = words[-1] + 'ing'
        w3 = words[-1] + 'ed'
    else:
        rick = "never gonna give" # you up
        [w1,w2,w3] = rick.split(' ')
    return [w1, w2, w3]


def writeText(keepWriting, text):

    max_lines = 5 # number of lines that can be displayed at a time
    max_chars = width/smallFontW - 8 # number of characters that can fit on a line; 4 taken off each end for padding
    max_charsTotal = max_chars*5
    wordsToMaxChar = max_chars*5 - len(text) 
    lineHeight = ((height/2) - (height/12)) / max_lines
    lineNum = 4
    if(len(text) > max_charsTotal ) :
        keepWriting = 0
        if(wordsToMaxChar != 0):
            text = text[:wordsToMaxChar]
    else:
        keepWriting = 1
    cursor_x = (width-(max_chars*smallFontW))/2 - smallFontW
    cursor_y = height/2 - height/12 - 4*lineHeight + smallFontH/2 
    while (len(text) > 0 and lineNum >= 0):
        # Draw the text line by line, starting from last line at the bottom, then moving up
        i = (len(text)-1) / max_chars # the -1 is necessary to make sure the division always falls short and floors
        line = text[:max_chars]
        text = text[max_chars:]
        # Render character by character
        n = 0
        for c in line:
            r = smallFont.render(c, 1, (200,200,200))
            xpos = (width-(max_chars*smallFontW))/2 + n*smallFontW
            ypos = height/2 - height/12 - lineNum*lineHeight + smallFontH/2
            cursor_x = xpos
            cursor_y = ypos
            screen.blit(r, (xpos,ypos))
            n += 1
        lineNum -= 1
    # Draw cursor
    pygame.draw.rect(screen, (60,180,160), (cursor_x+smallFontW*1.2, cursor_y, 3, smallFontH))

def displayUpdate(target, keepWriting ,textstring, textmode, label):
    screen.fill(bg_color)

    # P300
    label -= 33024 # Start from 0
    pygame.draw.rect(screen, (20,20,20), pygame.Rect(0,height/2,width,height/2))
    drawP300Highlight(label)
    drawP300Target(target)
    drawP300Text(textmode,label)
    
    # SSVEP 
    drawSSVEPHighlight(0, (0,150,230), 5)
    drawSSVEPHighlight(1, (100,220,200), 10)
    drawSSVEPHighlight(2, (255,150,0), 15)
    pred_words = predictText(textstring)
    drawSSVEPText(pred_words)

    # Draw borders
    pygame.draw.rect(screen, (255,255,255), (0, 0, width, 4))
    pygame.draw.rect(screen, (255,255,255), (0, 0+height/12, width, 4))
    # Text output
    writeText(keepWriting, textstring)

    pygame.display.update()