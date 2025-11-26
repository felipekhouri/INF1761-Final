
from OpenGL.GL import *
from PIL import Image
import numpy as np
import glm
from appearance import *

class Texture(Appearance):
  def __init__ (self, varname, filename, texel=None, width=1, height=1):
    self.varname = varname
    self.tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,self.tex)
    if filename:
      img = Image.open(filename)
      img = img.transpose(Image.FLIP_TOP_BOTTOM)
      data = np.array(img)
      width, height = img.size
      if (img.mode == 'RGB'):
        mode = GL_RGB
      elif (img.mode == 'RGBA'):
        mode = GL_RGBA
      else:
        raise RuntimeError("Unsupported image mode: " + img.mode)
      if (data.dtype == 'uint8'):
        dtype = GL_UNSIGNED_BYTE
      else:
        raise RuntimeError("Unsupported image component type: " + data.dtype)
      glTexImage2D(GL_TEXTURE_2D,0,mode,width,height,0,mode,dtype,data)
      glGenerateMipmap(GL_TEXTURE_2D)
    elif texel == None:
      glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,None)
    elif type(texel) == glm.vec3:
      array = np.array([texel[0]*255,texel[1]*255,texel[2]*255],dtype='uint8')
      glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,1,1,0,GL_RGB,GL_UNSIGNED_BYTE,array)
    elif type(texel) == glm.vec4:
      array = np.array([texel[0]*255,texel[1]*255,texel[2]*255,texel[3]*255],dtype='uint8')
      glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,1,1,0,GL_RGBA,GL_UNSIGNED_BYTE,array)
    else:
      raise RuntimeError("Invalid Texture parameters")
    self.width = width
    self.height = height

    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)	
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D,0)

  def GetTexId (self):
    return self.tex
  
  def GetWidth (self):
    return self.width

  def GetHeight (self):
    return self.height

  def Load (self, st):
    shd = st.GetShader()
    shd.ActiveTexture(self.varname)
    glBindTexture(GL_TEXTURE_2D,self.tex)

  def Unload (self, st):
    shd = st.GetShader()
    shd.DeactiveTexture()

