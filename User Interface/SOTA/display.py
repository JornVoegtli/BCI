from pyglet.gl import *
from pyglet import *
from pyglet.window import *
from controls import *
import user_input
from random import randint
import primitives

text = textUC # Defined in controls.py

class MyPyglet():
    def __init__(self):
        self.imageLoad = [pyglet.image.load('img/Vinay.jpg'), 
            pyglet.image.load('img/Sam.jpg'), 
            pyglet.image.load('img/Jorn.jpg'), 
            pyglet.image.load('img/Jun.jpg'), 
            pyglet.image.load('img/Nico.jpg'), 
            pyglet.image.load('img/javi.jpg')]
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

        # More flash settings
        if isCrazyKeyboardEnlargeColour:
            self.generateRandomColour()
            keyboardEnlargeFontColour = self.colourCrazy
        return

    def drawTarget(self, rowStim, colStim):
        if (isDrawTarget):
            rowNum = rowStim - OVTK_StimulationId_Label_01
            colNum = colStim - OVTK_StimulationId_Label_07
            x = colNum * width / 6
            y = (5-rowNum) * (keyboardPositionTop/5)
        primitives.drawRect(x, y, targetSize[0], targetSize[1], targetColour[0],targetColour[1],targetColour[2],targetColour[3])
        return

    def generateRandomColour(self,saturation=1,lightness=0.5):
        hue = randint(0,360)
        while hue > 120 and hue <290:
            hue = randint(0,360)

        chroma = 1 - abs(2*lightness-1)*saturation
        huePrime = hue/60
        intermediateValue = chroma*(1-abs(huePrime%2-1))
        red = 0
        blue = 0
        green = 0
        if huePrime < 1:
            red = chroma
            blue = intermediateValue
            green = 0
        elif huePrime < 2:
            red = intermediateValue
            blue = chroma
            green = 0
        elif huePrime < 3:
            red = 0
            blue = chroma
            green = intermediateValue
        elif huePrime < 4:
            red = 0
            blue = intermediateValue
            green = chroma
        elif huePrime < 5:
            red = intermediateValue
            blue = 0
            green = chroma
        elif huePrime < 6:
            red = chroma
            blue = 0
            green = intermediateValue
        m = lightness - 0.5*chroma
        red = (red+m)
        blue = (blue+m)
        green = (green+m)
        self.colourCrazyNormalized = (red,blue,green,1)
        self.colourCrazy = (int(red*255),int(blue*255),int(green*255),255)
        return 

    def startFlash(self, rowcol):
        # If column
        if (rowcol <= 5 and isDrawVertFlash):
            if (isEnlargeTextMode):
                c = rowcol
                for r in range(0, len(self.matrix)):
                    self.matrix[r][c].font_size = keyboardEnlargeFontSize
                    self.matrix[r][c].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
                    self.matrix[r][c].bold = True
            if (isHighlightTextMode):
                if(isCrazyHighlightTextMode):
                    self.generateRandomColour()
                    vertFlashColour = self.colourCrazyNormalized
                    self.generateRandomColour()
                    horizFlashColour = self.colourCrazyNormalized
                else:
                    vertFlashColour = vertFlashColourDefault
                    horizFlashColour = horizFlashColourDefault
                primitives.drawRect(rowcol*width/6, 0, vertFlashSize[0], vertFlashSize[1], vertFlashColour[0],vertFlashColour[1],vertFlashColour[2],vertFlashColour[3])
        # If row
        elif (rowcol <= 11 and isDrawHorizFlash):
            if (isEnlargeTextMode):
                r = rowcol%6
                for c in range(0, len(self.matrix[r])):
                    self.matrix[r][c].font_size = keyboardEnlargeFontSize
                    self.matrix[r][c].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
                    self.matrix[r][c].bold = True
            if (isHighlightTextMode):
                if(isCrazyHighlightTextMode):
                    self.generateRandomColour()
                    vertFlashColour = self.colourCrazyNormalized
                    self.generateRandomColour()
                    horizFlashColour = self.colourCrazyNormalized
                else:
                    vertFlashColour = vertFlashColourDefault
                    horizFlashColour = horizFlashColourDefault
                primitives.drawRect(0, rowcol%6*height/12, horizFlashSize[0], horizFlashSize[1], horizFlashColour[0], horizFlashColour[1], horizFlashColour[2], horizFlashColour[3])
        if(isDrawCircleMode):
            self.drawCircle(rowcol)
        if(isDrawImageMode):
            self.drawImage(rowcol)
        return

    def drawCircle(self, rowcol):
        if(isCrazyDrawCircleMode):
            self.generateRandomColour()
            circleColourVert = self.colourCrazyNormalized
            self.generateRandomColour()
            circleColourHoriz = self.colourCrazyNormalized
        else:
            circleColourHoriz = circleColourDefault
            circleColourVert = circleColourDefault
        if (rowcol < 6 and isDrawVertCircle):
            for j in range (0,6):
                ypos  = j*(keyboardPositionTop)/5 + circleRadius/4
                xpos  = rowcol*width/6 + circleRadius/4
                primitives.drawCircle(xpos,ypos,circleRadius,circleColourVert[0],circleColourVert[1],circleColourVert[2],circleColourVert[3])
        elif(rowcol < 12 and isDrawHorizCircle):
            for j in range (0,6):
                ypos  = rowcol%6*(keyboardPositionTop)/5 + circleRadius/4
                xpos  = j*width/6 + circleRadius/4
                primitives.drawCircle(xpos,ypos,circleRadius,circleColourHoriz[0],circleColourHoriz[1],circleColourHoriz[2],circleColourHoriz[3])        
        return

    def drawImage(self, rowcol):
        if(isDrawImageMode):
            if(rowcol<6 and isDrawVertImage):
                for j in range(0,6):
                    ypos  = j*(keyboardPositionTop)/5
                    xpos  = rowcol*width/6
                    self.imageLoad[randint(0,5)].blit(xpos,ypos,width=imageWidth,height=imageHeight)
            elif(rowcol < 12 and isDrawHorizCircle):
                for j in range (0,6):
                    ypos  = rowcol%6*(keyboardPositionTop)/5
                    xpos  = j*width/6
                    self.imageLoad[randint(0,5)].blit(xpos,ypos,width=imageWidth,height=imageHeight)
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
                self.matrix[r][c].bold = False
        # If row
        elif (rowcol <= 11 and isDrawHorizFlash):
            r = rowcol%6
            for c in range(0, len(self.matrix[r])):
                self.matrix[r][c].font_size = keyboardFontSize
                self.matrix[r][c].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
                self.matrix[r][c].bold = False
        return 

    def drawMatrix(self):
        # Draw keyboard matrix
        for r in range (0,len(self.matrix)):
            for c in range(0, len(self.matrix[r])):
                self.matrix[r][c].draw()
        
    def update(self):
        self.disp.batch.draw() 
        self.disp.win.flip()

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
        return 