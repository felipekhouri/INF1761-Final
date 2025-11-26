from luxor.interpolator import *

class LinearInterpolator (Interpolator):
  def __init__ (self, p0, p1):
    self.p0 = p0
    self.p1 = p1

  def Interpolate (self, t):
    return (1.0-t) * self.p0 + t * self.p1
