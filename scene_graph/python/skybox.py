from OpenGL.GL import * 
from shape import *
import glm
import numpy as np

class SkyBox (Shape):
  def __init__ (self):
    coords = np.array([
      -1.0,  1.0, -1.0,
      -1.0, -1.0, -1.0,
      1.0, -1.0, -1.0,
      1.0, -1.0, -1.0,
      1.0,  1.0, -1.0,
      -1.0,  1.0, -1.0,

      -1.0, -1.0,  1.0,
      -1.0, -1.0, -1.0,
      -1.0,  1.0, -1.0,
      -1.0,  1.0, -1.0,
      -1.0,  1.0,  1.0,
      -1.0, -1.0,  1.0,

      1.0, -1.0, -1.0,
      1.0, -1.0,  1.0,
      1.0,  1.0,  1.0,
      1.0,  1.0,  1.0,
      1.0,  1.0, -1.0,
      1.0, -1.0, -1.0,

      -1.0, -1.0,  1.0,
      -1.0,  1.0,  1.0,
      1.0,  1.0,  1.0,
      1.0,  1.0,  1.0,
      1.0, -1.0,  1.0,
      -1.0, -1.0,  1.0,

      -1.0,  1.0, -1.0,
      1.0,  1.0, -1.0,
      1.0,  1.0,  1.0,
      1.0,  1.0,  1.0,
      -1.0,  1.0,  1.0,
      -1.0,  1.0, -1.0,

      -1.0, -1.0, -1.0,
      -1.0, -1.0,  1.0,
      1.0, -1.0, -1.0,
      1.0, -1.0, -1.0,
      -1.0, -1.0,  1.0,
      1.0, -1.0,  1.0
    ], dtype='float32')
    
    # create VAO
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)
    # create coord and normal buffer
    id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,id)
    glBufferData(GL_ARRAY_BUFFER,coords.nbytes,coords,GL_STATIC_DRAW)
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,None)
    glEnableVertexAttribArray(0) 


  def Draw (self, st):
  # draw at camera position
    camera = st.GetCamera()
    origin = glm.vec4(0,0,0,1)
    peye = glm.vec3(glm.inverse(camera.GetViewMatrix()) * origin)
    M = glm.translate(glm.mat4(1),peye)
    st.PushMatrix()
    st.LoadMatrix(M)
    st.LoadMatrices()    # update loaded matrices
    glDepthMask(GL_FALSE)
    glBindVertexArray(self.vao)
    glDrawArrays(GL_TRIANGLES,0,36)
    glDepthMask(GL_TRUE)
    st.PopMatrix()
