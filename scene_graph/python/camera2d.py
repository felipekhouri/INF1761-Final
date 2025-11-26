import glm
from OpenGL.GL import *
from camera import *

class Camera2D (Camera):
  def __init__(self, xmin=-1, xmax=1, ymin=-1, ymax=1):
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax

  def GetProjMatrix (self):
    vp = glGetInteger(GL_VIEWPORT)
    w = vp[2]
    h = vp[3]
    dx = self.xmax - self.xmin
    dy = self.ymax - self.ymin
    if w/h > dx/dy:
      xc = (self.xmin + self.xmax) / 2
      xmin = xc - dx/2 * w/h
      xmax = xc + dx/2 * w/h 
      ymin = self.ymin
      ymax = self.ymax
    else:
      yc = (self.ymin + self.ymax) / 2
      ymin = yc - dy/2 * h/w
      ymax = yc + dy/2 * h/w
      xmin = self.xmin
      xmax = self.xmax
    return glm.ortho(xmin,xmax,ymin,ymax)

  def GetViewMatrix (self):
    return glm.mat4(1.0)