from __future__ import division, print_function, unicode_literals
import pyglet
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
from pyglet import clock
import ctypes
import primitives
import random
import user_input

constant = 10;
win = window.Window(fullscreen = True)
glClearColor(1, 1, 1, 1.0)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)
keys = key.KeyStateHandler()
win.push_handlers(keys)
batch = pyglet.graphics.Batch()
widget = user_input.TextWidget('', 200, 100, width - 210, batch)
a = primitives.Arc(150,150,radius=100,color=(1.,0.,0.,1.),sweep=90,style=GLU_FILL)
text_cursor = win.get_system_mouse_cursor('text')
text = "hi"
widget.caret.on_text(text)
pyglet.clock.set_fps_limit(60)
num = constant;
write = False
while not win.has_exit:
    clock.tick()
    if(num < constant):
        num = num+1
    win.dispatch_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if(keys[key.A] and num == constant):
        text = "A"    
        num = 0
        write = True
    
    if(num == (constant-1) and write):    
        widget.caret.on_text(text)    

    a.render()
    a.rotation+=1       
    batch.draw()
   
    
    win.flip()