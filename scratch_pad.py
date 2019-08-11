from pylib.dark_magic.box.patch import patch_module, patch_module_ast
import boxed_module
import unittest
import ast
import inspect
import astor
import random
import timeit

patch_module(boxed_module)

class Box:
  def __init__(self, value):
    self.boxed_value = value

  def __unbox__(self):
    return self.boxed_value + 1

  def __box__(self, new_val):
    self.boxed_value = new_val

class Counter:
    def __init__(self, value):
        self.value = value

    def __unbox__(self):
        temp = self.value
        self.value += 1
        return temp

    def __box__(self, new_val):
        self.value = new_val

def count(counter):
  a = counter.__unbox__()
  b = counter.__unbox__()
  counter.__box__(5)
  c = counter.__unbox__()
  d = counter.__unbox__()
  return a, b, c, d

class RandomVal:
    def __unbox__(self):
        return random.randint(0, 10)
        

def test_assign():
    box = Box(20) 
    value = boxed_module.do_assignment(box, 40)
    print(box.boxed_value)

    counter = Counter(0)
    counts = boxed_module.count(counter)

    print(counts)

    r = RandomVal()
    boxed_module.do_random(r)
    # print(timeit.timeit(lambda: boxed_module.count(Counter(0)), number=10000))
    # print(timeit.timeit(lambda: count(Counter(0)), number=10000))



class Fake(object):
    def __init__(self, value):
        try:
            self.boxed_value
        except:
            self.boxed_value = value
        else:
            print("do stuff")
    
if __name__ == "__main__":
    f = Fake(20)
    test_assign()
