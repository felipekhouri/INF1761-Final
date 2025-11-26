from transform import *
import glm

class Movement:

  def __init__ (self, T):
    self.t = 0
    self.T = T
    self.trl_trf = []
    self.rot_trf = []
    self.trl_interp = []
    self.rot_interp = []

  def AddTranslation (self, trf, interp):
    self.trl_trf.append(trf)
    self.trl_interp.append(interp)

  def AddRotation (self, trf, interp):
    self.rot_trf.append(trf)
    self.rot_interp.append(interp)

  def Advance (self, dt, reverse):
    t = self.t + dt
    if (t > self.T):
      t = self.T
    if reverse:
      t0 = (self.T-self.t)/self.T
      t1 = (self.T-t)/self.T
    else:
      t0 = self.t / self.T
      t1 = t / self.T
    # perform translations
    for i in range(0,len(self.trl_trf)):
      v0 = self.trl_interp[i].Interpolate(t0)
      v1 = self.trl_interp[i].Interpolate(t1)
      self.trl_trf[i].Translate(v1[0]-v0[0],v1[1]-v0[1],v1[2]-v0[2])
    # perform rotations 
    for i in range(0,len(self.rot_trf)):
      v0 = self.rot_interp[i].Interpolate(t0)
      v1 = self.rot_interp[i].Interpolate(t1)
      self.rot_trf[i].Rotate(v1[0]-v0[0],1.0,0.0,0.0)
      self.rot_trf[i].Rotate(v1[1]-v0[1],0.0,1.0,0.0)
      self.rot_trf[i].Rotate(v1[2]-v0[2],0.0,0.0,1.0)
    if t >= self.T:  # check if movement ended
      self.t = 0.0   # reset internal clock
      return True   # signalize the movement ended after this advance
    else:
      self.t = t
      return False  # signalize the movement continues
