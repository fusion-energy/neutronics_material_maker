# **Neutronics material maker**

[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CircleCI](https://circleci.com/gh/ukaea/neutronics_material_maker/tree/openmc_version.svg?style=svg)](https://circleci.com/gh/ukaea/neutronics_material_maker/tree/openmc_version)

[![codecov](https://codecov.io/gh/Shimwell/neutronics_material_maker/branch/openmc_version/graph/badge.svg)](https://codecov.io/gh/ukaea/neutronics_material_maker)

[![PyPI version](https://badge.fury.io/py/neutronics_material_maker.svg)](https://badge.fury.io/py/neutronics_material_maker)

The aim of this project is to facilitate the creation of neutronics materials for use in OpenMC.

The hope is that by having this collection of materials it is easier to reuse materials across projects, use common source with less room for user error.

Materials for using in neutronics codes have two main aspects; a list of isotopes along with their abundance and the material density.

This code contains an internal collection of materials with their isotopes abundances and densities all from public references.

A small amount of python code is built upon existing material creation and mixing functions in OpenMC to allow the internal collection of materials to be created in OpenMC format. Therefore you will need to install [OpenMC](https://docs.openmc.org/en/latest/quickinstall.html) and Python to use this code.

The code can be easily installed using pip

```pip install neutronics_material_maker```

Here is an example that access a material from the internal collection called eurofer which has about 60 isotopes of various redundancies and a density of 7.78g/cm3.

```python

import neutronics_material_maker as nmm```
my_mat = nmm.Material('eurofer')```
my_mat.openmc_material
```

For several materials within the collection the temperature and the pressure impacts the density of the material. The neutronics_material_maker adjusts the density to take temperature and the pressure into account when appropriate. 

```python

import neutronics_material_maker as nmm
my_mat1 = nmm.Material('H2O', temperature_in_C=300, pressure_in_Pa=15e6)```
my_mat1.openmc_material
```

For several materials within the collection the desnity is adjusted when the material is enriched. For breeder blankets in fusion it is common to enrich the lithium 6 content.

```python

import neutronics_material_maker as nmm
my_mat2 = nmm.Material('Li4SiO4', enrichment=60)
my_mat2.openmc_material
```

Materials can also be mixed together using the MultiMaterial class. This accepts combinations of neutronics_material_maker.Materials or with openmc.Material objects.

```
my_mat3 = MultiMaterial(material_name='mixed_mat',
                        materials=[my_mat1, my_mat2],
                        fracs=[0.4, 0.6],
                        percent_type='vo')
```


Further examples can be found in the [UKAEA OpenMC workshop task 11](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_11)
