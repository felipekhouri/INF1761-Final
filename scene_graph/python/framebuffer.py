from OpenGL.GL import *
import numpy as np

class Framebuffer:
  def __init__ (self, depth=None, colors=None):
    self.depth = depth         # depth texture buffer
    self.colors = colors or [] # color texture buffers
    self.fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER,self.fbo)
    if self.depth:
      glFramebufferTexture(GL_FRAMEBUFFER,GL_DEPTH_ATTACHMENT,self.depth.GetTexId(),0)
    for i,tex in enumerate(self.colors):
      glFramebufferTexture(GL_FRAMEBUFFER,GL_COLOR_ATTACHMENT0+i,tex.GetTexId(),0)
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
      raise RuntimeError("Framebuffer not complete")
    glBindFramebuffer(GL_FRAMEBUFFER,0)

  def GetDepthTexture (self):
    return self.depth

  def GetColorTextures (self):
    return self.colors

  def Bind (self):
    glBindFramebuffer(GL_FRAMEBUFFER,self.fbo)
    if not self.colors:
      glDrawBuffer(GL_NONE)
    else:
      buffers = []
      for i in range(0,len(self.colors)):
        buffers.append(GL_COLOR_ATTACHMENT0+i)
      glDrawBuffers(self.colors.size(),np.array(buffers,dtype="uint8"))

  def Unbind (self):
    glBindFramebuffer(GL_FRAMEBUFFER,0)
    glDrawBuffer(GL_BACK)
