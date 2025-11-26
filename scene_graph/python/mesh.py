from OpenGL.GL import *
from shape import Shape
import numpy as np

class Mesh (Shape):
  def __init__ (self, filename):
    coords = []
    normals = []
    indices = []
    with open(filename) as f:
      for line in f:
        elems = line.split()
        if elems[0] == "V":
          coords.append(float(elems[1]))
          coords.append(float(elems[2]))
          coords.append(float(elems[3]))
        elif elems[0] == "N":
          normals.append(float(elems[1]))
          normals.append(float(elems[2]))
          normals.append(float(elems[3]))
        elif elems[0] == "T":
          indices.append(int(elems[1]))
          indices.append(int(elems[2]))
          indices.append(int(elems[3]))
    vcoords = np.array(coords,dtype='float32')
    vnormals = np.array(normals,dtype='float32')
    vindices = np.array(indices,dtype='uint32')
    # create VAO
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    ids = glGenBuffers(3)
    # create coord and normal buffers
    glBindBuffer(GL_ARRAY_BUFFER,ids[0])
    glBufferData(GL_ARRAY_BUFFER,vcoords.nbytes,vcoords,GL_STATIC_DRAW)
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(0) 
    glBindBuffer(GL_ARRAY_BUFFER,ids[1])
    glBufferData(GL_ARRAY_BUFFER,vnormals.nbytes,vnormals,GL_STATIC_DRAW)
    glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(1) 
    # create index buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ids[2])
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,vindices.nbytes,vindices,GL_STATIC_DRAW)
    self.nind = len(indices)

  def Draw (self, st):
    glBindVertexArray(self.vao)
    glDrawElements(GL_TRIANGLES,self.nind,GL_UNSIGNED_INT,None)