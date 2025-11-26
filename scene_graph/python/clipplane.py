from OpenGL.GL import *
import glm
from appearance import Appearance

class ClipPlane(Appearance):
    def __init__ (self, name, a, b, c, d):
      self.name = name
      self.planes = [glm.vec4(a,b,c,d)]
      self.planecolor = "planecolor"
      self.color = glm.vec4(1,1,1,1)
    
    def AddPlane (self, a, b, c, d):
       self.planes.append(glm.vec4(a,b,c,d))

    def SetColor (self, name, r, g, b):
      self.planecolor = name
      self.color = glm.vec4(r,g,b,1)

    def Load (self, st):
      shd = st.GetShader()
      M = st.GetCurrentMatrix()  # model
      if shd.GetLightingSpace == "camera":
        M = st.GetCamera().GetViewMatrix() * M
      Mit = glm.transpose(glm.inverse(M))
      # transform planes
      planes = []
      for i, p in enumerate(self.planes):
        planes.append(Mit*p)
        glEnable(GL_CLIP_DISTANCE0 + i)
      shd.SetUniform(self.name,planes)
      shd.SetUniform(self.planecolor,self.color)
