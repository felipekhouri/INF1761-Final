
class Scene:
  def __init__ (self, root):
    self.root = root
    self.engines = []

  def GetRoot (self):
    return self.root

  def AddEngine (self, engine):
    self.engines.append(engine)

  def Update (self, dt):
    for e in self.engines:
      e.Update(dt)

  def Render (self, camera):
    from state import State
    st = State(camera)
    self.root.Render(st)
