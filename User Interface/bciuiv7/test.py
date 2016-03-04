from __future__ import division, print_function, unicode_literals
import pyglet
from pyglet.gl import *
from pyglet import *
from pyglet.window import *
import pyglet.primitives



if __name__=="__main__":
    import random
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
    while not win.has_exit:
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
