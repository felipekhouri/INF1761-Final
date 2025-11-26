from OpenGL.GL import *
from shape import Shape
import numpy as np
import math

class Triangle (Shape):
  def __init__ (self):
    coord = [[-1,0],[1,0],[0,1]]
    bcoord = np.array(coord,dtype='float32')
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,id)
    glBufferData(GL_ARRAY_BUFFER,bcoord.nbytes,bcoord,GL_STATIC_DRAW)
    glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(0) 
    glVertexAttribPointer(3,2,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(3) 

  def Draw (self, st):
    glBindVertexArray(self.vao)
    glVertexAttrib3f(1,0,0,1) # constant for all vertices
    glVertexAttrib3f(2,1,0,0) # constant for all vertices
    glDrawArrays(GL_TRIANGLES,0,3)