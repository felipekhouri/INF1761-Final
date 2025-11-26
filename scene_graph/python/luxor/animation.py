
class Animation:
  def __init__ (self, moves):
    self.curr = 0
    self.moves = moves.copy()

  # return true when its done
  def Advance (self, dt, reverse=False):
    if reverse:
      idx = (len(self.moves)-1) - self.curr 
    else:
      idx = self.curr
    if self.moves[idx].Advance(dt,reverse):
      self.curr += 1
      if self.curr == len(self.moves):
        self.curr = 0
        return True
    return False
