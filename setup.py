
# install with this command
# sudo python setup.py install --force
# test with this command
# sudo python setup.py test
# export PYTHONPATH=/media/jshim/Data/neutronics_material_maker/
# pytest

from setuptools import setup

#with open('requirements.txt') as test_reqs_txt:
#    requirements = [line for line in test_reqs_txt]


setup(name='neutronics_material_maker',
      version='0.1233',
      summary='Package for making material cards for neutronic codes such as Serpent',
      description='Create isotopes, elements, materials, chemical compounds and homogenised mixtures for use in neutronics codes',
      url='https://github.com/ukaea/neutronics_material_maker',
      author='Jonathan Shimwell',
      author_email='jonathan.shimwell@ukaea.uk',
      license='Apache 2.0',
      packages=['neutronics_material_maker'],
      test_suite='tests.module_tests',
      zip_safe=True,
      package_data={'':['requirements.txt', 'README.md','README.md.html', 'LICENSE']},
      #install_requires=requirements,
      #setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )

