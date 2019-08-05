

class Box:
  def __init__(self):
    self.assigned = None

  def __assign__(self, var):
    self.assigned = True
  
def do_assignment(box):
  a = box
  return a