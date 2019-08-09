from pylib.dark_magic.box.patch import patch_module, patch_module_ast
import tests.boxed_module
import unittest
import ast
import inspect
import astor

#patch_module(tests.boxed_module)


class TestBox(unittest.TestCase):
  def test_assign(self):
    box = tests.boxed_module.Box(20) 
    value = tests.boxed_module.do_assignment(box, 40)
    s = inspect.getsource(tests.boxed_module.do_assignment)
    #print s
    self.assertEqual(value, 20)
    self.assertEqual(40, box.boxed_value)

if __name__ == "__main__":
  unittest.main()