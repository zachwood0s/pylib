from pylib.dark_magic.box import auto_unbox
import boxed_module
import unittest
import ast
import inspect
import astor
import random
import timeit

auto_unbox(boxed_module)

"""
def patch_function(func):
    source = inspect.getsource(func) 
    module = inspect.getmodule(func)
    tree = ast.parse(source)
    patched_ast = patch_node_ast(tree)
    patched_code = compile(patched_ast, module.__file__, "exec")
    print(astor.to_source(patched_ast))
    exec(patched_code, module.__dict__)
    return func
"""

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

def count_patched(counter):
    a = b = c = counter
    return a, b, c

auto_unbox(count_patched)

class RandomVal:
    def __unbox__(self):
        return random.randint(0, 10)
        

def filter_(func):
    def filter_inner(seq):
        return filter(func, seq)
    return filter_inner

def map_(func):
    def map_inner(seq):
        return map(func, seq)
    return map_inner

def pipe(data, *funcs):
    for func in funcs:
        data = func(data)
    
    return data

def test_assign():
    box = Box(20) 
    value = boxed_module.do_assignment(box, 40)
    print(box.boxed_value)

    counter = Counter(0)
    counts = boxed_module.count(counter)
    print(counts)
    counts = count_patched(counter)
    print(counts)

    r = RandomVal()
    boxed_module.do_random(r)
    count(Counter(0))
    lst = [10, 12, 30]
    double = lambda x: x*2
    p = pipe(
        lst,
        map_(double),
        filter_(lambda x: x > 20),
        list
    )
    print(p)
    #print(inspect.getsource(inspect.getmodule(test_assign)))








    
if __name__ == "__main__":
    test_assign()
