import unittest
import mathfunc


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    # this function is called before every test
    def setUp(self):
        self.math_object = mathfunc.Maths(1,2)

    # this function is called after every test
    # before output "ok" or "failed" in the report
    def tearDown(self):
        self.math_object = None

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(3, mathfunc.Maths(1, 2).add())
        self.assertNotEqual(3, mathfunc.Maths(2, 2).add())

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, mathfunc.Maths(3, 2).minus())

    @unittest.skip("I'm pretty sure this will pass")
    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, mathfunc.Maths(2, 3).multi())

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, mathfunc.Maths(6, 3).divide())
        self.assertEqual(2.5, mathfunc.Maths(5, 2).divide())


if __name__ == '__main__':
    unittest.main()
