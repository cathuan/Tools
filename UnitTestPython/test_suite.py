import unittest
import test_mathfunc
from test_mathfunc import TestMathFunc


def create_and_run_test_suite():
    suite = unittest.TestSuite()

    tests = [TestMathFunc("test_add"), TestMathFunc("test_minus"), TestMathFunc("test_divide")]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def load_all_test_in_module_and_run():

    suite = unittest.TestLoader().loadTestsFromModule(test_mathfunc)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    load_all_test_in_module_and_run()
