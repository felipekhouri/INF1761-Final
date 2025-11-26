import glm

class Camera:
  def GetProjMatrix (self):
    return glm.mat4(1)

  def GetViewMatrix (self):
    return glm.mat4(1)

  def Load (self, st):
    pass