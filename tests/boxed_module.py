


class Box:
  def __init__(self, value):
    self.boxed_value = value

  def __unbox__(self):
    return self.boxed_value

  def __box__(self, new_val):
    self.boxed_value = new_val
  
def do_assignment(box, new_val):
  a = box
  box = new_val
  return a