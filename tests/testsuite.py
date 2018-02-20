
import unittest

from module_tests import Tester

def main():
    unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite())


if __name__ == '__main__':
    unittest.main()