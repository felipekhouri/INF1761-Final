from OpenGL.GL import *
from shape import Shape
import numpy as np
import math

class Square (Shape):
  def __init__ (self):
    coord = [[-1.0,-1.0],[1.0,-1.0],[1.0,1.0],[-1.0,1.0]]
    texcoord = [[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0]]
    bcoord = np.array(coord,dtype='float32')
    btexcoord = np.array(texcoord,dtype='float32')
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    id = glGenBuffers(2)
    glBindBuffer(GL_ARRAY_BUFFER,id[0])
    glBufferData(GL_ARRAY_BUFFER,bcoord.nbytes,bcoord,GL_STATIC_DRAW)
    glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER,id[1])
    glBufferData(GL_ARRAY_BUFFER,btexcoord.nbytes,btexcoord,GL_STATIC_DRAW)
    glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(1)

  def Draw (self, st):
    glBindVertexArray(self.vao)
    glDrawArrays(GL_TRIANGLE_FAN,0,4)