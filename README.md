
[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)
[![CircleCI](https://circleci.com/gh/ukaea/neutronics_material_maker/tree/openmc_version.svg?style=svg)](https://circleci.com/gh/ukaea/neutronics_material_maker/tree/openmc_version)
[![codecov](https://codecov.io/gh/ukaea/neutronics_material_maker/branch/openmc_version/graph/badge.svg)](https://codecov.io/gh/ukaea/neutronics_material_maker)
[![PyPI version](https://badge.fury.io/py/neutronics-material-maker.svg)](https://badge.fury.io/py/neutronics-material-maker)
[![Documentation Status](https://readthedocs.org/projects/neutronics-material-maker/badge/?version=latest)](https://neutronics-material-maker.readthedocs.io/en/latest/?badge=latest)

# **Neutronics material maker**

The aim of this project is to facilitate the creation of materials for use in neutronics codes such as OpenMC, Serpent, MCNP and Fispact.

The hope is that by having this collection of materials it is easier to reuse materials across projects, use a common source with less room for user error.

:point_right: [Documentation](https://neutronics-material-maker.readthedocs.io/en/latest/)

## Installation

To use the code you will need to have OpenMC installed [OpenMC](https://docs.openmc.org/en/latest/quickinstall.html) 

The code can be easily installed using pip

```
pip install neutronics_material_maker
```

## Features

Materials for using in neutronics codes have two main aspects; a list of isotopes along with their abundance and the material density.

This code contains an internal collection of materials with their isotopes abundances and densities (sometimes temperature, pressure and enrichment dependant), but you may also import your own materials collection.

## Usage - finding available materials

Each of the materials available is stored in an internal dictionary that can be accessed using the ```AvailableMaterials()``` command.

```python
import neutronics_material_maker as nmm
all_materials = nmm.AvailableMaterials()
print(all_materials.keys())
```

## Usage - basic Material

Here is an example that access a material from the internal collection called eurofer which has about 60 isotopes of and a density of 7.78g/cm3.

```python
import neutronics_material_maker as nmm
my_mat = nmm.Material('eurofer')
my_mat.openmc_material
```

## Usage - hot pressurised Material

For several materials within the collection the temperature and the pressure impacts the density of the material. The neutronics_material_maker adjusts the density to take temperature and the pressure into account when appropriate. Densities are caluclated either by an material specific formula (for example [FLiBe](https://github.com/ukaea/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/data/multiplier_and_breeder_materials.json)) or using [CoolProps](https://pypi.org/project/CoolProp/) (for example [coolants](https://github.com/ukaea/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/data/coolant_materials.json))

```python
import neutronics_material_maker as nmm
my_mat1 = nmm.Material('H2O', temperature_in_C=300, pressure_in_Pa=15e6)
my_mat1.openmc_material
```

For several materials within the collection the density is adjusted when the material is enriched. For breeder blankets in fusion it is common to enrich the lithium 6 content.

## Usage - enriched Material

Lithium ceramics used in fusion breeder blankets often contain enriched lithium-6 content. This slightly change in density is accounted for by the neutronics_material_maker

```python
import neutronics_material_maker as nmm
my_mat2 = nmm.Material('Li4SiO4', enrichment=60)
my_mat2.openmc_material
```


## Usage - MultiMaterial (mixed Materials))

Materials can also be mixed together using the MultiMaterial class. This accepts a list of neutronics_material_maker.Materials or openmc.Material objects along with the material fractions (fracs).

```python
import neutronics_material_maker as nmm
my_mat1 = nmm.Material('Li4SiO4', enrichment=60)
my_mat2 = nmm.Material('Be12Ti')
my_mat3 = MultiMaterial(materials=[my_mat1, my_mat2],
                        fracs=[0.4, 0.6],
                        percent_type='vo')
my_mat3.openmc_material
```

## Usage - importing your own material library

Assuming you have a JSON file saved as ```mat_lib.json``` containing materials defined in the same format as the [exisiting materials](https://github.com/ukaea/neutronics_material_maker/tree/openmc_version/neutronics_material_maker/data) then you can import this file into the package using ```AddMaterialFromFile()```. Another option is to use ```AddMaterialFromDir()``` to import a directory of json files

```python
import neutronics_material_maker as nmm
nmm.AddMaterialFromFile('mat_lib.json')
nmm.AvailableMaterials() # this will print the new larger list of materials
```

## Usage - exporting to different neutronics codes

You can export to OpenMC, Serpent, MCNP and Fispact with the appropiate arguments

```python
import neutronics_material_maker as nmm
my_mat = nmm.Material('tungsten')
my_mat.openmc_material()
my_mat.mcnp_material(id=1, zaid_suffix='.31c)
my_mat.serpent_material(zaid_suffix='.31c))
my_mat.fispact_material(volume=100)
```

## Further examples

Further examples can be found in the [UKAEA OpenMC workshop task 11](https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_11) and in the [Documentation](https://neutronics-material-maker.readthedocs.io/en/latest/)
