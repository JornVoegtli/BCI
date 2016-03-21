from pyglet.gl import *
from pyglet import *
from pyglet.window import *
from controls import *
import user_input
from random import randint
import primitives
import word_predictor

text = textUC # Defined in controls.py

class MyPyglet():
    def __init__(self):
        self.imageLoad = [pyglet.image.load('img/Vinay.jpg'), 
                        pyglet.image.load('img/Sam.jpg'), 
                        pyglet.image.load('img/Jorn.jpg'), 
                        pyglet.image.load('img/Jun.jpg'), 
                        pyglet.image.load('img/Nico.jpg'), 
                        pyglet.image.load('img/javi.jpg'),
                        pyglet.image.load('img/cat.jpg'),
                        pyglet.image.load('img/cat2.jpg'),
                        pyglet.image.load('img/cat3.jpg'),
                        pyglet.image.load('img/cat4.jpg'),
                        pyglet.image.load('img/cat5.jpg'),
                        pyglet.image.load('img/cat6.jpg')]
        self.logo = pyglet.image.load('img/neurospell.png')
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
        self.current_text = "" 
        # Set up user keyboard matrices
        # Uppercase
        matrixUC = []
        for j in range(0, len(textUC) ):
            row = []
            for i in range(0, len(textUC[j]) ):
                line = textUC[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5) 
                xpos = i*width/6 + width/40
                temp = pyglet.text.Label(line, 
                    font_name='Courier New',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
                row.append(temp)
            matrixUC.append(row)
        # Lowercase
        matrixLC = []
        for j in range(0, len(textLC) ):
            row = []
            for i in range(0, len(textLC[j]) ):
                line = textLC[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5)
                xpos = i*width/6 + width/40
                temp = pyglet.text.Label(line, 
                    font_name='Courier New',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
                row.append(temp)
            matrixLC.append(row)
        # Numbers
        matrixNum = []
        for j in range(0, len(textNum) ):
            row = []
            for i in range(0, len(textNum[j]) ):
                line = textNum[j][i]
                ypos = keyboardPositionTop - (j)*(keyboardPositionTop/5)
                xpos = i*width/6 + width/40
                temp = pyglet.text.Label(line, 
                    font_name='Courier New',
                    font_size=keyboardFontSize,
                    color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                    x=xpos, y=ypos,
                    anchor_x='left', anchor_y='bottom')
                row.append(temp)
            matrixNum.append(row)
        # Make matrix lists
        self.matrices = [matrixUC, matrixLC, matrixNum]
        self.text = [textUC, textLC, textNum]
        # Choose initial matrix
        self.matIndex = matIndex
        # Do first text prediction
        self.updatePredictiveText()

        #set up window rendering
        self.win.dispatch_events()
        #self.drawMatrix()
        self.win.flip()
        return

    def drawTarget(self, rowStim, colStim):
        if (isDrawTarget):
            rowNum = rowStim - OVTK_StimulationId_Label_01
            colNum = colStim - OVTK_StimulationId_Label_07
            x = colNum * width / 6
            y = (5-rowNum) * (keyboardPositionTop/5)
        primitives.drawRect(x, y, targetSize[0], targetSize[1], targetColour[0],targetColour[1],targetColour[2],targetColour[3])
        return

    def drawSelection(self, rowStim, colStim, selectedStr):
        if (isDrawTarget):
            rowNum = rowStim - OVTK_StimulationId_Label_01
            colNum = colStim - OVTK_StimulationId_Label_07
            x = colNum * width / 6
            y = (5-rowNum) * (keyboardPositionTop/5)
        primitives.drawRect(x, y, targetSize[0], targetSize[1], targetColour[0],targetColour[1],targetColour[2],targetColour[3])

        # Make whole screen flash suddenly 
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
        selectText = pyglet.text.Label(selectedStr, 
                font_name='Courier New',
                font_size=selectTextFontSize,
                color=(selectTextFontColour[0],selectTextFontColour[1],selectTextFontColour[2],selectTextFontColour[3]),
                x=width/2, y=height/2,
                anchor_x='left', anchor_y='bottom')
        selectText.draw()
        glClearColor(backgroundColour[0], backgroundColour[1], backgroundColour[2], backgroundColour[3])
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
        if(isDrawCrazyFlashMode):
            randNum = randint(1,4)
            #if randNum == 0:
            #   self.drawHighlightText(rowcol)
            if randNum == 1:
                if (isEnlargeTextMode):
                    self.drawEnlargeText(rowcol,)
                else:
                    self.startFlash(rowcol) # Recursion!
            elif randNum == 2:
                if (isDrawCircleMode):
                    self.drawCircleFlash(rowcol)
                else:
                    self.startFlash(rowcol) # Recursion!
            elif randNum == 3:
                if (isDrawTriMode):
                    self.drawTriFlash(rowcol)
                else:
                    self.startFlash(rowcol) # Recursion!
            elif randNum == 4:
                if (isDrawImageMode):
                    self.drawImage(rowcol)
                else:
                    self.startFlash(rowcol) # Recursion!
        else:
            if(isEnlargeTextMode):
                self.drawEnlargeText(rowcol)
            if(isHighlightTextMode):
                self.drawHighlightText(rowcol)
            if(isDrawCircleMode):
                self.drawCircleFlash(rowcol)
            if(isDrawImageMode):
                self.drawImage(rowcol)
            if(isDrawTriMode):
                self.drawTriFlash(rowcol)
        return

    def drawHighlightText(self,rowcol):
        if(isCrazyHighlightTextMode):
            self.generateRandomColour()
            vertFlashColour = self.colourCrazyNormalized
            self.generateRandomColour()
            horizFlashColour = self.colourCrazyNormalized
        else:
            vertFlashColour = vertFlashColourDefault
            horizFlashColour = horizFlashColourDefault
        if (isHighlightTextMode):
            if (rowcol <= 5 and isDrawVertFlash):
                primitives.drawRect(rowcol*width/6, 0, vertFlashSize[0], vertFlashSize[1], vertFlashColour[0],vertFlashColour[1],vertFlashColour[2],vertFlashColour[3])
            elif (rowcol <= 11 and isDrawHorizFlash):
                if (isHighlightTextMode):
                    primitives.drawRect(0, rowcol%6*keyboardPositionTop/5, horizFlashSize[0], horizFlashSize[1], horizFlashColour[0], horizFlashColour[1], horizFlashColour[2], horizFlashColour[3])
        return

    def drawEnlargeText(self,rowcol):  
        if isCrazyKeyboardEnlargeColour:
            self.generateRandomColour()
            keyboardEnlargeFontColour = self.colourCrazy
        else:
            keyboardEnlargeFontColour = keyboardEnlargeFontColourDefault 
        if (rowcol <= 5 and isDrawVertEnlarge): 
            c = rowcol
            for r in range(0, len(self.matrices[matIndex])):
                self.matrices[matIndex][r][c].font_size = keyboardEnlargeFontSize
                self.matrices[matIndex][r][c].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
                self.matrices[matIndex][r][c].bold = True
        elif (rowcol <= 11 and isDrawHorizEnlarge): 
            r = 5-rowcol%6
            for c in range(0, len(self.matrices[matIndex][r])):
                self.matrices[matIndex][r][c].font_size = keyboardEnlargeFontSize
                self.matrices[matIndex][r][c].color = (keyboardEnlargeFontColour[0],keyboardEnlargeFontColour[1],keyboardEnlargeFontColour[2],keyboardEnlargeFontColour[3])
                self.matrices[matIndex][r][c].bold = True
        self.drawMatrix()
        return

    def drawTriFlash(self,rowcol):
        if(isCrazyDrawTriMode):
            self.generateRandomColour()
            triColourVert = self.colourCrazyNormalized
            self.generateRandomColour()
            triColourHoriz = self.colourCrazyNormalized
        else:
            triColourHoriz = triColourDefault
            triColourVert = triColourDefault
        if (rowcol < 6 and isDrawVertTri):
            for j in range (0,6):
                ypos  = j*(keyboardPositionTop)/5
                xpos  = rowcol*width/6 
                primitives.drawTri(xpos,ypos,triWidth,triHeight,triColourVert[0],triColourVert[1],triColourVert[2],triColourVert[3])
        elif(rowcol < 12 and isDrawHorizTri):
            for j in range (0,6):
                ypos  = rowcol%6*(keyboardPositionTop)/5
                xpos  = j*width/6
                primitives.drawTri(xpos,ypos,triWidth,triHeight,triColourHoriz[0],triColourHoriz[1],triColourHoriz[2],triColourHoriz[3])                
        return

    def drawCircleFlash(self, rowcol):
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
        if(rowcol<6 and isDrawVertImage):
            for j in range(0,6):
                ypos  = j*(keyboardPositionTop)/5
                xpos  = rowcol*width/6
                self.imageLoad[randint(0,len(self.imageLoad)-1)].blit(xpos,ypos,width=imageWidth,height=imageHeight)
        elif(rowcol < 12 and isDrawHorizImage):
            for j in range (0,6):
                ypos  = rowcol%6*(keyboardPositionTop)/5
                xpos  = j*width/6
                self.imageLoad[randint(0,len(self.imageLoad)-1)].blit(xpos,ypos,width=imageWidth,height=imageHeight)
        return

    def stopFlash(self, rowcol):
        if (isEnlargeTextMode == False and isDrawCrazyFlashMode == False): 
            return # No need to stopFlash if text is not enlarged

        # If column
        if (rowcol <= 5 and isDrawVertEnlarge):
            c = rowcol
            for r in range(0, len(self.matrices[matIndex])):
                self.matrices[matIndex][r][c].font_size = keyboardFontSize
                self.matrices[matIndex][r][c].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
                self.matrices[matIndex][r][c].bold = False
        # If row
        elif (rowcol <= 11 and isDrawHorizEnlarge):
            r = 5-rowcol%6
            for c in range(0, len(self.matrices[matIndex][r])):
                self.matrices[matIndex][r][c].font_size = keyboardFontSize
                self.matrices[matIndex][r][c].color = (keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3])
                self.matrices[matIndex][r][c].bold = False
        self.drawMatrix()
        return 

    def drawMatrix(self): # For online
        for r in range (0,len(self.matrices[self.matIndex])):
            for c in range(0, len(self.matrices[self.matIndex][r])):
                self.matrices[self.matIndex][r][c].draw()

    def updatePredictiveText(self):
        ## Predictive text
        word = ((self.current_text).split(" "))[-1] # Get only last word
        if (len(word)>5): 
            word = word[0:5] # Limit the length of the word to predict so it won't slow things down
        corrected_text = word_predictor.correct(word)

        ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
        xpos  = 0*width/6 + width/40
        temp0 = pyglet.text.Label(corrected_text[0], 
                font_name='Courier New',
                font_size=keyboardFontSize,
                color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                x=xpos, y=ypos,
                anchor_x='left', anchor_y='bottom')
       
        ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
        xpos  = 1*width/6 + width/40
        temp1 = pyglet.text.Label(corrected_text[1], 
                font_name='Courier New',
                font_size=keyboardFontSize,
                color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                x=xpos, y=ypos,
                anchor_x='left', anchor_y='bottom')
        
        ypos = keyboardPositionTop - (0)*(keyboardPositionTop/5)
        xpos  = 2*width/6 + width/40
        temp2 = pyglet.text.Label(corrected_text[2], 
                font_name='Courier New',
                font_size=keyboardFontSize,
                color=(keyboardFontColour[0],keyboardFontColour[1],keyboardFontColour[2],keyboardFontColour[3]),
                x=xpos, y=ypos,
                anchor_x='left', anchor_y='bottom')

        for i in range(len(self.matrices)): # Need to update for all matrices
            self.matrices[i][0][0] = temp0
            self.matrices[i][0][1] = temp1
            self.matrices[i][0][2] = temp2
            self.text[i][0][0] = corrected_text[0]
            self.text[i][0][1] = corrected_text[1]
            self.text[i][0][2] = corrected_text[2]
        return

    def getSelectedText(self, selection):
        selection[0] -= 33025
        selection[1] -= 33031
        return self.text[self.matIndex][selection[0]][selection[1]]

    def makeSelection(self, selection, selectionStr):
        self.text_input = selectionStr
        # Normal text
        if (selection[1] <= 4) : # Not rightmost column 
            if (self.text_input == "SPACE"): 
                self.text_input = " "
            print("Text selection:", self.text_input)
            if(selection[0] == 0 and selection[1] < 2):
                self.current_text = self.current_text + self.text_input
                self.widget.caret.on_text(self.text_input)  
            else:
                word = ((self.current_text).split(" "))[-1]
                for i in range (0,len(word)):
                    self.widget.caret.on_text_motion(MOTION_BACKSPACE)
                self.current_text = self.current_text[0,len(self.current_text)-len(word)] + self.text_input
                self.widget.caret.on_text(self.text_input)
            self.updatePredictiveText()
        # Backspace
        elif (self.text_input == u"\u2190"): 
            self.current_text = self.current_text.pop()
            self.widget.caret.on_text_motion(MOTION_BACKSPACE)
        elif (self.text_input == u"\u2190"): 
            print("Pressed ENTER")
        elif (self.text_input == "ABC"):
            self.matIndex = 0
        elif (self.text_input == "abc"): 
            self.matIndex = 1
        elif (self.text_input == "123"):
            self.matIndex = 2
        return

    def drawTextBox(self):
        self.batch.draw()
        return

    def update(self):
        self.win.flip()
        return

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Set up background
        return

    def loadingScreen(self):
        glClearColor(0.1,0.1,0.1,1)
        self.clear()
        #self.drawMatrix()
        w = self.logo.width/10
        h = self.logo.height/10
        self.logo.blit(width/2-w/2,height/2-h/2,width=w,height=h)
        glClearColor(backgroundColour[0], backgroundColour[1], backgroundColour[2], backgroundColour[3])
        return