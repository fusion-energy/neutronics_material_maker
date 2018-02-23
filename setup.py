
# install with this command
# sudo python setup.py install --force
# test with this command
# sudo python setup.py test


from setuptools import setup

with open('requirements.txt') as test_reqs_txt:
    requirements = [line for line in test_reqs_txt]


setup(name='neutronics_material_maker',
      version='0.1224',
      summary='Package for making material cards for neutronic codes such as Serpent',
      description='create isotopes, materials, chemical compounds, homogenised mixtures',
      url='https://github.com/ukaea/neutronics_material_maker',
      author='Jonathan Shimwell',
      author_email='jonathan.shimwell@ukaea.uk',
      license='Apache 2.0',
      packages=['neutronics_material_maker'],
      test_suite='neutronics_material_maker.tests.module_tests',
      zip_safe=False,
      install_requires=requirements,
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )

