from pylib.dark_magic.box.patch import patch_module
import tests.boxed_module
import unittest
patch_module(tests.boxed_module)


class TestBox(unittest.TestCase):
  def test_assign(self):
    box = tests.boxed_module.Box() 
    self.assertIsNone(box.assigned)
    tests.boxed_module.do_assignment(box)
    self.assertIsNotNone(box.assigned)

if __name__ == "__main__":
  unittest.main()