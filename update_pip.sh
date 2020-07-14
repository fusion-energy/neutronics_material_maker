
#install required packages
pip3 install bump
pip3 install setuptools
pip3 install twine

#clean up old versions
rm -r .eggs
rm -r dist
rm -r neutronics_material_maker.egg-info/

# increase version umber in setup.py
bump

# create distribution
python setup.py sdist

#upload to pypi
twine upload dist/* --verbose
