
# these test cover the functionality of neutronics material maker

# to run type

# python -m pytest tests/testsuite.py
# python3 -m pytest tests/testsuite.py
# 
# coverage run tests/testsuite.py
# py.test --cov=neutronics_material_maker testsuite.py 

#  pytest --cov=./neutronics_material_maker tests/testsuite.py 

# requires pytest (pip install pytest)

import unittest

from tests.module_tests import Isotope_tests
from tests.module_tests import Element_tests
from tests.module_tests import Material_tests
from tests.module_tests import Compound_tests
from tests.module_tests import Homogenised_mixture_tests

def main():
    unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite())


if __name__ == '__main__':
    unittest.main()