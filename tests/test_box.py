from pylib.dark_magic.box.patch import patch_module, patch_module_ast
import tests.boxed_module
patch_module(tests.boxed_module)
import unittest
import ast
import astor
import inspect


class TestBox(unittest.TestCase):
  def test_assign(self):
    box = tests.boxed_module.Box(20) 
    value = tests.boxed_module.do_assignment(box)
    code = inspect.getsource(tests.boxed_module.do_assignment)
    a = astor.to_source(patch_module_ast(tests.boxed_module))
    self.assertEqual(value, 20)

if __name__ == "__main__":
  unittest.main()