#!/usr/bin/env python

'''Demonstrates basic use of IncrementalTextLayout and Caret.

A simple widget-like system is created in this example supporting keyboard and
mouse focus.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )

class TextWidget(object):
    def __init__(self, text, x, y, width,height, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), 
                                dict(font_name = 'Arial', 
                                    font_size= 20, 
                                    color=(0, 0, 0, 255)),
                                )

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=True, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        #Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

    
