from OpenGL.GL import *
from shape import *
from grid import *

class Quad (Shape):
  def __init__ (self, nx = 1, ny = 1):
    grid = Grid(nx,ny)
    self.nind = grid.IndexCount()
    # create VAO
    self.vao  = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    # create coord and texcoord buffers
    id = glGenBuffers(2)
    coords = grid.GetCoords()
    glBindBuffer(GL_ARRAY_BUFFER,id[0])
    glBufferData(GL_ARRAY_BUFFER,coords.nbytes,coords,GL_STATIC_DRAW)
    glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,None)  # coord
    glEnableVertexAttribArray(0)  
    glVertexAttribPointer(3,2,GL_FLOAT,GL_FALSE,0,None)  # texcoord
    glEnableVertexAttribArray(3)  
    # create index buffer
    indices = grid.GetIndices()
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,id[1])
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

  def Draw (self, st):
    glBindVertexArray(self.vao)
    glVertexAttrib3f(1,0,0,1) # constant for all vertices
    glVertexAttrib3f(2,1,0,0) # constant for all vertices
    glDrawElements(GL_TRIANGLES,self.nind,GL_UNSIGNED_INT,None)
