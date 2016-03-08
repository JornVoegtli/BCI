from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import random

class OVBox():
    def initialize(self):
        self.win = window.Window()
        #self.keys = key.KeyStateHandler()
        #elf.win.push_handlers(self.keys)
        return

    def process(self):
        self.win.dispatch_events()
        #self.win.push_handlers(pyglet.window.event.WindowEventLogger())
        #dt = pyglet.clock.tick() 
        print "Processing"
#        if (self.keys[key.A]):
#            self.unitialize()
        #self.win.clear() 
        #self.win.draw() 
        #self.win.flip() 
        if self.win.has_exit:
            self.unitialize()
        return

    def unitialize(self):
        self.win.close()
        sys.exit()
        return

box = OVBox()
box.initialize()
print "Hello"
while True:
    box.process()