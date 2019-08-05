from pylib.utils import require
import unittest
      
class TestUtils(unittest.TestCase):
  def test_require(self):

    @require(lambda var1, var2, named: var1 != 20)
    @require(lambda var1, var2, named: var2 != 20)
    @require(lambda var1, var2, named: named != "Joe")
    def simple_require(var1, var2, named="Joe"):
      return var1, var2, named

    self.assertFalse(simple_require(20, 0, "test"))
    self.assertFalse(simple_require(0, 20, "test"))
    self.assertFalse(simple_require(0, 0, named="Joe"))
    self.assertNotEqual(simple_require(0, 0, "test"), False)


if __name__ == "__main__":
  unittest.main()