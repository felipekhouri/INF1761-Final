from OpenGL.GL import *
from appearance import *

class PolygonOffset (Appearance):
  def __init__ (self, factor = -1, units = -1):
    self.factor = factor
    self.units = units

  def Load (self, st):
    glPolygonOffset(self.factor,self.units)
    glEnable(GL_POLYGON_OFFSET_FILL)
    glEnable(GL_POLYGON_OFFSET_LINE)

  def Unload (self, st):
    glDisable(GL_POLYGON_OFFSET_LINE)
    glDisable(GL_POLYGON_OFFSET_FILL)
