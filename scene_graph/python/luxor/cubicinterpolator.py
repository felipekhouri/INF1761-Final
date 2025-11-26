from luxor.interpolator import *

class CubicInterpolator (Interpolator):
  def __init__ (self, p0, m0, p1, m1):
    self.p0 = p0
    self.m0 = m0
    self.p1 = p1
    self.m1 = m1

  def Interpolate (self, t):
    t2 = t*t
    t3 = t*t2
    return ((2*t3-3*t2+1) * self.p0 +
            (t3-2*t2+t) * self.m0 + 
            (-2*t3+3*t2) * self.p1 +
            (t3-t2) * self.m1
           )
