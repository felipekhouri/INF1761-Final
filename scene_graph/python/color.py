import glm
from appearance import Appearance

class Color(Appearance):
    def __init__ (self, r, g, b, a=1):
      self.color = glm.vec4(r,g,b,a)

    def Load (self, st):
      shd = st.GetShader()
      shd.SetUniform("color",self.color)
