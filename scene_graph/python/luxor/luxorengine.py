from engine import *
from luxor.linearinterpolator import *
from luxor.cubicinterpolator import *
from luxor.animation import *
from luxor.movement import *
import glm

class LuxorEngine (Engine): 

  def __init__ (self, trf_all, trf_base, trf_haste1, trf_haste2, trf_haste3, trf_cupula, trf_lampada):
    self.reverse = False
    self.head_angle = 0.0
    self.status = "up"
    self.curr_anim = None 
    self.trf_all = trf_all
    self.trf_base = trf_base
    self.trf_haste1 = trf_haste1
    self.trf_haste2 = trf_haste2
    self.trf_haste3 = trf_haste3
    self.trf_cupula = trf_cupula
    self.trf_lampada = trf_lampada
    self.CreateStandDownAnimation()
    self.CreateJumpForwardAnimation()

  def CreateStandDownAnimation (self):
    move = Movement(0.5)
    move.AddRotation(self.trf_haste1,
                     LinearInterpolator(glm.vec3(0.0,0.0,0.0),
                                        glm.vec3(-30.0,0.0,0.0)
                                       )
                   )
    move.AddRotation(self.trf_haste2,
                      LinearInterpolator(glm.vec3(0.0,0.0,0.0),
                                         glm.vec3(120.0,0.0,0.0)
                                        )
                    )
    move.AddRotation(self.trf_haste3,
                      LinearInterpolator(glm.vec3(0.0,0.0,0.0),
                                         glm.vec3(-120.0,0.0,0.0)
                                        )
                    )
    move.AddRotation(self.trf_cupula,
                      LinearInterpolator(glm.vec3(0.0,0.0,0.0),
                                         glm.vec3(30.0,0.0,0.0)
                                        )
                    )
    self.stand_down_anim = Animation([move])

  def CreateJumpForwardAnimation (self):
    # first move: take position to jump
    move1 = Movement(0.3)
    move1.AddRotation(self.trf_haste1, 
                      LinearInterpolator(glm.vec3(-30.0,0.0,0.0),
                                         glm.vec3(-40.0,0.0,0.0)
                                        )
                      )
    move1.AddRotation(self.trf_haste2, 
                      LinearInterpolator(glm.vec3(120.0,0.0,0.0),
                                         glm.vec3(150.0,0.0,0.0)
                                        )
                    )
    move1.AddRotation(self.trf_haste3, 
                      LinearInterpolator(glm.vec3(-120.0,0.0,0.0),
                                         glm.vec3(-145.0,0.0,0.0)
                                        )
                    )
    move1.AddRotation(self.trf_cupula, 
                      LinearInterpolator(glm.vec3(30.0,0.0,0.0),
                                         glm.vec3(60.0,0.0,0.0)
                                        )
                    )
    # second move: jump to the top
    move2 = Movement(0.5)
    move2.AddTranslation(self.trf_all, 
                          CubicInterpolator(glm.vec3(0.0,0.0,0.0),
                                            glm.vec3(0.0,1.0,1.0),
                                            glm.vec3(0.0,30.0,50.0),
                                            glm.vec3(0.0,0.0,100.0)
                                           )
                          )
    move2.AddRotation(self.trf_base, 
                      LinearInterpolator(glm.vec3(0.0,0.0,0.0),
                                         glm.vec3(-30.0,0.0,0.0)
                                        )
                      )
    move2.AddRotation(self.trf_haste1, 
                      LinearInterpolator(glm.vec3(-40.0,0.0,0.0),
                                         glm.vec3(10.0,0.0,0.0)
                                        )
                      )
    move2.AddRotation(self.trf_haste2, 
                      LinearInterpolator(glm.vec3(150.0,0.0,0.0),
                                         glm.vec3(50.0,0.0,0.0)
                                        )
                    )
    move2.AddRotation(self.trf_haste3, 
                      LinearInterpolator(glm.vec3(-145.0,0.0,0.0),
                                         glm.vec3(-50.0,0.0,0.0)
                                        )
                    )
    move2.AddRotation(self.trf_cupula, 
                      LinearInterpolator(glm.vec3(60.0,0.0,0.0),
                                         glm.vec3(65.0,0.0,0.0)
                                        )
                    )
    # third move: from top to landing
    move3 = Movement(0.5)
    move3.AddTranslation(self.trf_all, 
                          CubicInterpolator(glm.vec3(0.0,30.0,50.0),
                                            glm.vec3(0.0,0.0,100.0),
                                            glm.vec3(0.0,0.0,90.0),
                                            glm.vec3(0.0,-1.0,1.0)
                                           )
                          )
    move3.AddRotation(self.trf_base, 
                      LinearInterpolator(glm.vec3(-30.0,0.0,0.0),
                                         glm.vec3(0.0,0.0,0.0)
                                        )
                      )
    move3.AddRotation(self.trf_haste1, 
                      LinearInterpolator(glm.vec3(10.0,0.0,0.0),
                                         glm.vec3(-60.0,0.0,0.0)
                                        )
                      )
    move3.AddRotation(self.trf_haste2, 
                      LinearInterpolator(glm.vec3(50.0,0.0,0.0),
                                         glm.vec3(160.0,0.0,0.0)
                                        )
                    )
    move3.AddRotation(self.trf_haste3, 
                      LinearInterpolator(glm.vec3(-50.0,0.0,0.0),
                                         glm.vec3(-165.0,0.0,0.0)
                                        )
                    )
    move3.AddRotation(self.trf_cupula, 
                      LinearInterpolator(glm.vec3(65.0,0.0,0.0),
                                         glm.vec3(60.0,0.0,0.0)
                                        )
                    )
    # forth move: from landing to resting
    move4 = Movement(0.3)
    move4.AddRotation(self.trf_haste1, 
                      LinearInterpolator(glm.vec3(-60.0,0.0,0.0),
                                         glm.vec3(-30.0,0.0,0.0)
                                        )
                      )
    move4.AddRotation(self.trf_haste2, 
                      LinearInterpolator(glm.vec3(160.0,0.0,0.0),
                                         glm.vec3(120.0,0.0,0.0)
                                        )
                    )
    move4.AddRotation(self.trf_haste3, 
                      LinearInterpolator(glm.vec3(-165.0,0.0,0.0),
                                         glm.vec3(-120.0,0.0,0.0)
                                        )
                    )
    move4.AddRotation(self.trf_cupula, 
                      LinearInterpolator(glm.vec3(60.0,0.0,0.0),
                                         glm.vec3(30.0,0.0,0.0)
                                        )
                    )
    self.jump_forward_anim = Animation([move1,move2,move3,move4])

  def StandUp (self):
    if self.curr_anim or self.status != "down":
      return False
    self.curr_anim = self.stand_down_anim
    self.reverse = True
    self.status = "up"   # next status
    return True

  def StandDown (self):
    if self.curr_anim or self.status != "up":
      return False
    self.curr_anim = self.stand_down_anim
    self.reverse = False
    self.status = "down"     # next status
    return True

  def JumpForward (self):
    if self.curr_anim or self.status != "down":
      return False
    self.curr_anim = self.jump_forward_anim
    self.reverse = False
    self.status = "down"   # next status
    return True

  def JumpBackward (self):
    if self.curr_anim or self.status != "down":
      return False
    self.curr_anim = self.jump_forward_anim
    self.reverse = True
    self.status = "down"   # next status
    return True

  def TurnHead (self, angle):
    self.trf_cupula.Rotate(angle,0.0,1.0,0.0)
    self.head_angle += angle

  def Update (self, dt):
    if (self.curr_anim):
      if (self.curr_anim.Advance(dt,self.reverse)):
        self.curr_anim = None
