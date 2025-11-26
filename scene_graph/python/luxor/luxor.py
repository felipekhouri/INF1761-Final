from node import *
from mesh import *
from material import *
from transform import *
from luxor.luxorengine import *

class Luxor:
  def __init__ (self):
    base_a = Mesh("../../luxor/base_a.msh")
    base_b = Mesh("../../luxor/base_b.msh")
    haste1 = Mesh("../../luxor/haste1.msh")
    haste2 = Mesh("../../luxor/haste2.msh")
    haste3_a = Mesh("../../luxor/haste3_a.msh")
    haste3_b = Mesh("../../luxor/haste3_b.msh")
    cupula_a = Mesh("../../luxor/cupula_a.msh")
    cupula_b = Mesh("../../luxor/cupula_b.msh")
    lampada = Mesh("../../luxor/lampada.msh")
    red = Material(1.0,0.0,0.0)
    white = Material(1.0,1.0,1.0)
    white.SetAmbient(1.0,1.0,1.0)
    trf_all = Transform()
    trf_base = Transform()
    trf_haste1 = Transform()
    trf_haste2 = Transform()
    trf_haste3 = Transform()
    trf_cupula = Transform()
    trf_lampada = Transform()
    trf_haste1.Translate(0.0,4.0,0.0)
    trf_haste2.Translate(0.0,17.15,0.0)
    trf_haste3.Translate(0.0,16.78,0.0)
    trf_cupula.Translate(0.0,18.12,0.0)
    trf_lampada.Translate(0.0,8.4,9.0)
    self.light_node = Node(None,trf_lampada,[white],[lampada])
    self.node = Node(None,trf_all,[red],
                     nodes = [
                               Node(None,trf_base,shps=[base_a,base_b],nodes=[
                                 Node(None,trf_haste1,shps=[haste1],nodes=[
                                   Node(None,trf_haste2,shps=[haste2],nodes=[
                                     Node(None,trf_haste3,shps=[haste3_a,haste3_b],nodes=[
                                       Node(None,trf_cupula,shps=[cupula_a,cupula_b],nodes=[
                                         self.light_node
                                       ])
                                     ])
                                   ])
                                 ])
                               ])
                             ]
                    )
    self.engine = LuxorEngine(trf_all,trf_base,trf_haste1,trf_haste2,trf_haste3,trf_cupula,trf_lampada)

  def GetNode (self):
    return self.node

  def GetLightNode (self):
    return self.light_node

  def GetEngine (self):
    return self.engine