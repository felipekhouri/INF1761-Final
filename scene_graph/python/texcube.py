from OpenGL.GL import *
from PIL import Image
import numpy as np

from appearance import *

class TexCube(Appearance):
  def __init__ (self, varname, filename):
    self.varname = varname
    img = Image.open(filename)
    #img = img.transpose(Image.FLIP_TOP_BOTTOM)
    data = np.array(img)
    width, height = img.size
    if img.mode == 'RGB':
      mode = GL_RGB
    elif img.mode == 'RGBA':
      mode = GL_RGBA
    else:
      raise RuntimeError("Unsupported image mode: " + img.mode)
    print(img.mode)
    if (data.dtype == 'uint8'):
      dtype = GL_UNSIGNED_BYTE
    else:
      raise RuntimeError("Unsupported image component type: " + data.dtype)
    self.tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP,self.tex)
    # subimages' dimension
    w = width / 4
    h = height / 3
    x = [2*w,  0,  w,  w,  w,3*w]
    y = [  h,  h,2*h,  0,  h,  h]
    face = [
      GL_TEXTURE_CUBE_MAP_POSITIVE_X,  # right
      GL_TEXTURE_CUBE_MAP_NEGATIVE_X,  # left
      GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,  # bottom
      GL_TEXTURE_CUBE_MAP_POSITIVE_Y,  # top
      GL_TEXTURE_CUBE_MAP_POSITIVE_Z,  # front
      GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,  # back
    ]
    for i in range(0,6):
      subimg = img.crop((x[i],y[i],x[i]+w,y[i]+h))
      glTexImage2D(face[i],0,GL_RGB,w,h,0,mode,dtype,np.array(subimg))

    glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)	
    glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)	
    glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_WRAP_R,GL_CLAMP_TO_EDGE)	

  def GetTexId (self):
    return self.tex

  def Load (self, st):
    shd = st.GetShader()
    shd.ActiveTexture(self.varname)
    glBindTexture(GL_TEXTURE_CUBE_MAP,self.tex)


  def Unload (self, st):
    shd = st.GetShader()
    shd.DeactiveTexture()
