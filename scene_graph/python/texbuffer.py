from OpenGL.GL import *
from appearance import *
import numpy as np

class TexBuffer(Appearance):
  def __init__ (self, varname, array):
    self.varname = varname
    self.buffer = glGenBuffers(1)
    self.tex = glGenTextures(1)
    self.SetData(array)

  def SetData (self, array):
    self.dtype = array.dtype
    self.shape = array.shape
    self.nbytes = array.nbytes
    if self.dtype == 'int32':
      if len(self.shape) == 1:
        self.format = GL_R32I
      elif self.shape[1] == 2:
        self.format = GL_RG32I
      elif self.shape[1] == 3:
        self.format = GL_RGB32I
      elif self.shape[1] == 4:
        self.format = GL_RGBA32I
      else:
        raise RuntimeError("Invalid shape for texture buffer")
    elif self.dtype == 'unt32':
      if len(self.shape) == 1:
        self.format = GL_R32UI
      elif self.shape[1] == 2:
        self.format = GL_RG32I
      elif self.shape[1] == 3:
        self.format = GL_RGB32UI
      elif self.shape[1] == 4:
        self.format = GL_RGBA32UI
      else:
        raise RuntimeError("Invalid shape for texture buffer")
    elif self.dtype == 'float32' or self.dtype == 'float64':
      if self.dtype == 'float64':
        array = np.array(array,dtype='float32')
      if len(self.shape) == 1:
        self.format = GL_R32F
      elif self.shape[1] == 2:
        self.format = GL_RG32F
      elif self.shape[1] == 3:
        self.format = GL_RGB32F
      elif self.shape[1] == 4:
        self.format = GL_RGBA32F
      else:
        raise RuntimeError("Invalid shape for texture buffer")
    else:
      raise RuntimeError("Invalid type for texture buffer:",self.dtype)
    glBindTexture(GL_TEXTURE_BUFFER,self.tex)
    glBindBuffer(GL_TEXTURE_BUFFER,self.buffer)
    glBufferData(GL_TEXTURE_BUFFER,self.nbytes,array,GL_DYNAMIC_DRAW)
    glTexBuffer(GL_TEXTURE_BUFFER,self.format,self.buffer)

  def GetTexId (self):
    return self.tex

  def Load (self, st):
    shd = st.GetShader()
    shd.ActiveTexture(self.varname)
    glBindTexture(GL_TEXTURE_BUFFER,self.tex)

  def Unload (self, st):
    shd = st.GetShader()
    shd.DeactiveTexture()

  def GetData (self):
    glBindBuffer(GL_TEXTURE_BUFFER, self.buffer)
    raw = glGetBufferSubData(GL_TEXTURE_BUFFER, 0, self.nbytes)  # returns bytes
    result = np.frombuffer(raw, dtype=np.float32, count=-1).copy()  # copy so it's owned by NumPy
    glBindBuffer(GL_TEXTURE_BUFFER, 0)
    return result
