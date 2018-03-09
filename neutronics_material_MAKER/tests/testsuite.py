
# these test cover the functionality of neutronics material maker

# to run type

# python -m pytest testsuite.py
# python3 -m pytest testsuite.py
# 
# coverage run testsuite.py
# py.test --cov=neutronics_material_maker testsuite.py 

#  pytest --cov=./neutronics_material_maker tests/testsuite.py 

# requires pytest (pip install pytest)

import unittest

from module_tests import Tester

def main():
    unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite())


if __name__ == '__main__':
    unittest.main()