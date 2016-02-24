import os, sys
import pyglet
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import ctypes
import primitives
import random
import string
sys.path.append(r'C:\Users\Jun Shern\Dropbox\EE2 BCI Project\User Interface\bciuiv7')

class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
            
    def initialize(self): # Called once when starting the scenario
        self.count = 0
        self.target = [0,0]
        self.label = 33024 + random.randint(0,11)
        self.textstring = ""
        self.textmode = 1
        self.keepWriting = 1 
        # Pygame
        win = window.Window()
        glClearColor(.8, .8, .8, 1.0)
        glEnable(GL_BLEND)
        keys = key.KeyStateHandler()
        win.push_handlers(keys)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        p = primitives.Pixel(10,10)
        c = primitives.Circle(200,100,width=100,color=(0.,.9,0.,1.))
        a = primitives.Arc(150,150,radius=100,color=(1.,0.,0.,1.),sweep=90,style=GLU_FILL)
        P = primitives.Polygon([(0, 0), (50, 200), (80, 200),(60,100),(100,5)],color=(.3,0.2,0.5,.7))
        l = primitives.Line((10,299),(100,299),stroke=2,color=(0,0.,1.,1.))
        label = pyglet.text.Label("Hello, world!", 
            font_name='Times New Roman',
            font_size=36,
            color=(0,0,0,255),
            x=win.width//2, y=win.height//2,
            anchor_x='center', anchor_y='center')
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

        win.dispatch_events()
        col = (255,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        c.color = col
        if(keys[key.A]):
            c.render()
        p.render()
        a.render()
        a.rotation+=1
        P.render()
        l.render()
        label.draw()
        win.flip()
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
#user32 = ctypes.windll.user32
#print "width", user32.GetSystemMetrics(0)/2 
#print "height", user32.GetSystemMetrics(1)/2 
