from __future__ import division, print_function, unicode_literals
import os, sys
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import primitives
import user_input
import random
import string
import ctypes
#sys.path.append(r'C:\Users\AARON\Dropbox\EE2 BCI Project\User Interface\bciuiv7')

"""
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
"""

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
        # Pyglet
        self.win = window.Window(fullscreen = True)
        glClearColor(0, 0, 1, 1.0)
        glEnable(GL_BLEND)
        self.keys = key.KeyStateHandler()
        self.win.push_handlers(self.keys)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        user32 = ctypes.windll.user32
        self.width = user32.GetSystemMetrics(0)
        self.height = user32.GetSystemMetrics(1)
        self.words6 = pyglet.text.Label("A               B               C              D               E               \u2190",
            font_name='monospace',
            font_size=36,
            color=(255,255,255,255),
            x=0, y=5*self.height/12,
            anchor_x='left', anchor_y='bottom')
        self.words5 = pyglet.text.Label("F               G               H              I               J               ENTER",
            font_name='monospace',
            font_size=36,
            color=(255,255,255,255),
            x=0, y=4*self.height/12,
            anchor_x='left', anchor_y='bottom')
        self.words4 = pyglet.text.Label("K               L               M              N               O               abc",
            font_name='monospace',
            font_size=36,
            color=(255,255,255,255),
            x=0, y=3*self.height/12,
            anchor_x='left', anchor_y='bottom')
        self.words3 = pyglet.text.Label("P              Q              R             S              T              123",
            font_name='monospace',
            font_size=36,
            color=(255,255,255,255),
            x=0, y=2*self.height/12,
            anchor_x='left', anchor_y='bottom')        
        self.words2 = pyglet.text.Label("U              V              W             X              \u25B2              {&=",
            font_name='monospace',
            font_size=36,
            color=(255,255,255,255),
            x=0, y=self.height/12,
            anchor_x='left', anchor_y='bottom')
        self.words = pyglet.text.Label("Y              Z              SPACE             \u25C4              \u25BC              \u25BA", 
            font_name='monospace',
            font_size=36,
            color=(255,255,255,255),
            x=0, y=0,
            anchor_x='left', anchor_y='bottom')
        self.batch = pyglet.graphics.Batch()
        self.widget = user_input.TextWidget('', 0, int(7*self.height/12), int(self.width),int(5*self.height/12), self.batch)
        self.text = "This is a test line to test if the test moves to the next line. Test test test test test test test test test. The rabbit jumps over the moon to eat the pie that's in the stove but the stove is no where to be found because I got nothing to type and hats and peanut butter is not what i want to say but i dont know what im typing help me please"
        self.widget.caret.on_text(self.text)
        self.win.dispatch_events()
        self.win.flip()
        self.constant = 2
        self.num = self.constant
        self.write = False
        return
            
    def process(self): # Called on each box clock tick (this can be configured by right-clicking the box)
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

        if self.win.has_exit:
            self.win.close()
            sys.exit()

        else:
            self.label2 = random.randint(0,12)
            self.target0 = random.randint(0,5)
            self.target1 = random.randint(0,6)
            
            if(self.num < self.constant):
                self.num = self.num+1
            
            if(self.keys[key.A] and self.num == self.constant):
                self.text = " A"    
                self.num = 0
                self.write = True
            
            if(self.num == (self.constant-1) and self.write):    
                self.widget.caret.on_text(self.text)

            self.win.dispatch_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            #draw text
            self.batch.draw() 
            #highlight vertical
            if self.label2 < 6:
                primitives.drawRect(self.label2*self.width/6,0,self.width/6,7*self.height/12,1,1,0,1)
            #highlight horizontal
            elif self.label2 < 13:
                primitives.drawRect(0,self.label2%7*self.height/12,self.width,self.height/12,1,1,0,1)
            #highlight target    
            primitives.drawRect(self.target0*self.width/6,self.target1*self.height/12,self.width/6,self.height/12,0,1,0,1)
            #draw keyboard
            self.words6.draw()
            self.words5.draw()
            self.words4.draw()
            self.words3.draw()
            self.words2.draw()
            self.words.draw()
            self.win.flip()
            # Send outputs
            self.sendOutput(1, self.label)
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
        self.win.close()
        sys.exit()
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

OVTK_StimulationId_Target = 33285
OVTK_StimulationId_Label_00 = 33024
box = MyOVBox()
