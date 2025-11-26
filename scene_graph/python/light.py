import glm
from OpenGL.GL import *

class Light:
    def __init__ (self, x, y, z, w=1, space="world"): 
      self.amb = glm.vec4(0.2,0.2,0.2,1.0)
      self.dif = glm.vec4(0.8,0.8,0.8,1.0)
      self.spe = glm.vec4(1.0,1.0,1.0,1.0)
      self.pos = glm.vec4(x,y,z,w)
      self.space = space
      self.reference = None

    def SetAmbient (self, r, g, b):
      self.amb[0] = r
      self.amb[1] = g
      self.amb[2] = b

    def SetDiffuse (self, r, g, b):
      self.dif[0] = r
      self.dif[1] = g
      self.dif[2] = b

    def SetSpecular (self, r, g, b):
      self.spe[0] = r
      self.spe[1] = g
      self.spe[2] = b

    def SetPosition (self, x, y, z, w):
      self.pos[0] = x
      self.pos[1] = y
      self.pos[2] = z
      self.pos[3] = w

    def SetReference (self, reference):
      self.reference = reference

    def GetReference (self):
      return self.reference

    def Load (self, st):
      shd = st.GetShader()
      shd.SetUniform("lamb",self.amb)
      shd.SetUniform("ldif",self.dif)
      shd.SetUniform("lspe",self.spe)
      # Set position in lighting space
      mat = glm.mat4(1.0)
      if self.space == "world" and shd.GetLightingSpace() == "camera":
        mat = st.GetCamera().GetViewMatrix()
      elif self.space == "camera" and shd.GetLightingSpace() == "world":
        mat = glm.inverse(st.GetCamera().GetViewMatrix())
      if self.GetReference():
        mat = mat * self.GetReference().GetModelMatrix()
      pos = mat * self.pos  # to lighting space
      shd.SetUniform("lpos",pos)
