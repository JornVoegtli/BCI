from __future__ import division, print_function, unicode_literals
import pyglet
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import primitives
import ctypes
import word_display 
import random

if __name__=="__main__":
	#set window
    win = window.Window()
    win.set_fullscreen(True)
    
    #color background
    glClearColor(0.05882, 0.05882, 0.05882, 1.0)
    
    #set openGL stuff
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    #key event handlers
    keys = key.KeyStateHandler()
    win.push_handlers(keys)
  
  	#get window parameters
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0) 
    height = user32.GetSystemMetrics(1) 

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        primitives.drawRect(0,height/2,width,height/2,20,20,20,1)
        primitives.drawRect(0,0,width,4,255,255,255,1)
        primitives.drawRect(0,0+height/12,width,4,255,255,255,1)
        win.flip()