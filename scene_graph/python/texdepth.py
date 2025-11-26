from OpenGL.GL import *
from appearance import *

class TexDepth (Appearance):
  def __init__ (self, varname, width, height):
    self.varname = varname
    self.width = width
    self.height = height
    self.tex = glGenTextures(1) 
    glBindTexture(GL_TEXTURE_2D,self.tex)
    glTexImage2D(GL_TEXTURE_2D,0,GL_DEPTH_COMPONENT,self.width,self.height,0,GL_DEPTH_COMPONENT,GL_FLOAT,None)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)	
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D,0)

  def GetTexId (self):
    return self.tex

  def SetCompareMode (self):
    glBindTexture(GL_TEXTURE_2D,self.tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL)
    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_REF_TO_TEXTURE)
    glBindTexture(GL_TEXTURE_2D,0)

  def Load (self, st):
    shd = st.GetShader()
    shd.ActiveTexture(self.varname)
    glBindTexture(GL_TEXTURE_2D,self.tex)

  def Unload (self, st):
    shd = st.GetShader()
    shd.DeactiveTexture()
