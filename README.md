
[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)
[![CircleCI](https://circleci.com/gh/fusion-energy/neutronics_material_maker/tree/main.svg?style=svg)](https://circleci.com/gh/fusion-energy/neutronics_material_maker/tree/main)
[![codecov](https://codecov.io/gh/fusion-energy/neutronics_material_maker/branch/main/graph/badge.svg)](https://codecov.io/gh/fusion-energy/neutronics_material_maker)
[![PyPI version](https://badge.fury.io/py/neutronics-material-maker.svg)](https://badge.fury.io/py/neutronics-material-maker)
[![Documentation Status](https://readthedocs.org/projects/neutronics-material-maker/badge/?version=latest)](https://neutronics-material-maker.readthedocs.io/en/latest/?badge=latest)
[![Code Quality Score](https://www.code-inspector.com/project/13383/score/svg)](https://frontend.code-inspector.com/public/project/13383/neutronics_material_maker/dashboard)
[![Code Grade](https://www.code-inspector.com/project/13383/status/svg)](https://frontend.code-inspector.com/public/project/13383/neutronics_material_maker/dashboard)


# **Neutronics Material Maker**

The aim of this project is to facilitate the creation of materials for use in
neutronics codes such as OpenMC, Serpent, MCNP and Fispact.

The hope is that by having this collection of materials it is easier to reuse
materials across projects, use a common source with less room for user error.

One nice aspect of this material maker is the ability to change the density of
a material based on isotope enrichment (e.g. inbuild lithium ceramics),
temperature and pressure.

:point_right: [Documentation](https://neutronics-material-maker.readthedocs.io/en/latest/)

:point_right: [Video presentation]()

## Installation

### Conda

To use the code you will need to have OpenMC installed
[OpenMC](https://docs.openmc.org/en/latest/quickinstall.html).

The recommended method is to install from
[Conda Forge](https://conda-forge.org) which also installs all the dependencies
including OpenMC.

```bash
conda create --name new_env python=3.8
conda activate new_env
conda install neutronics_material_maker -c conda-forge
```
### Pip
Alternatively the code can be easily installed using pip. This method doesn't
currently include OpenMC so that will have to be installed separately using
Conda or compiled.

```bash
pip install neutronics_material_maker
```

To include the optional capability of calculating the density of coolants
additional packages are needed (CoolProp). A slightly modified pip install
is required in this case.
```bash
pip install "neutronics_material_maker[density]"
```

## Features

Materials for using in neutronics codes have two main aspects; a list of
isotopes along with their abundance and the material density.

This code contains an internal collection of materials with their isotope
abundances and densities (sometimes temperature, pressure and enrichment
dependant), but you may also import your own materials collection.


## Usage - Finding Available Materials

Each of the materials available is stored in an internal dictionary that can be
accessed using the ```AvailableMaterials()``` command.

```python
import neutronics_material_maker as nmm
all_materials = nmm.AvailableMaterials()
print(all_materials.keys())
```

### Usage - Material()

```python
import neutronics_material_maker as nmm
my_mat = nmm.Material(
    name='my_custom_material',
    isotopes={'Li6':0.5, 'Li7':0.5},
    density=2.01,
    percent_type='ao',
    density_unit='g/cm3'
)
my_mat.openmc_material
```

## Usage - Material from library

Here is an example that accesses a material from the internal collection called
eurofer which has about 60 isotopes of a density of 7.78g/cm3.

```python
import neutronics_material_maker as nmm
my_mat = nmm.Material.from_library('eurofer')
my_mat.openmc_material
```


## Usage - Hot Pressurised Material

For several materials within the collection the temperature and the pressure impacts the density of the material. The neutronics_material_maker adjusts the density to take temperature and the pressure into account when appropriate. Densities are calculated either by a material specific formula (for example [FLiBe](https://github.com/fusion-energy/neutronics_material_maker/blob/main/neutronics_material_maker/data/multiplier_and_breeder_materials.json)) or using [CoolProps](https://pypi.org/project/CoolProp/) (for example [coolants](https://github.com/fusion-energy/neutronics_material_maker/blob/main/neutronics_material_maker/data/coolant_materials.json))

```python
import neutronics_material_maker as nmm
my_mat1 = nmm.Material.from_library(name='H2O', temperature=600, pressure=15e6)
my_mat1.openmc_material
```

For several materials within the collection the density is adjusted when the
material is enriched. For breeder blankets in fusion it is common to enrich the
lithium 6 content.


## Usage - Enriched Material

Lithium ceramics used in fusion breeder blankets often contain enriched
lithium-6 content. This slight change in density is accounted for by the
neutronics_material_maker.

```python
import neutronics_material_maker as nmm
my_mat2 = nmm.Material.from_library(name='Li4SiO4', enrichment=60)
my_mat2.openmc_material
```


## Usage - Material.from_mixture

Materials can also be mixed together using the from_mixture method. This
accepts a list of ```neutronics_material_maker.Materials``` or 
```openmc.Material``` objects along with the material fractions (fracs).

```python
import neutronics_material_maker as nmm
my_mat1 = nmm.Material.from_library(name='Li4SiO4', packing_fraction=0.64)
my_mat2 = nmm.Material.from_library(name='Be12Ti')
my_mat3 = nmm.Material.from_mixture(materials=[my_mat1, my_mat2],
                        fracs=[0.4, 0.6],
                        percent_type='vo')
my_mat3.openmc_material
```


## Usage - Importing Your Own Material Library

Assuming you have a JSON file saved as ```mat_lib.json``` containing materials
defined in the same format as the
[exisiting materials](https://github.com/fusion-energy/neutronics_material_maker/tree/main/neutronics_material_maker/data)
then you can import this file into the package using
```AddMaterialFromFile()```. Another option is to use ```AddMaterialFromDir()```
to import a directory of json files.

```python
import neutronics_material_maker as nmm
nmm.AddMaterialFromFile('mat_lib.json')
nmm.AvailableMaterials() # this will print the new larger list of materials
```

## Usage - Exporting To Different Neutronics Codes

You can export to OpenMC, Serpent, MCNP and Fispact with the appropiate
arguments.

```python
import neutronics_material_maker as nmm
my_mat = nmm.Materialfrom_library('tungsten')

# openmc
my_mat.openmc_material

# mcnp - required a material_id to be set
my_mat.material_id = 1
my_mat.mcnp_material

# serpent
my_mat.serpent_material

# fispact - requires volume to be specified
my_mat.volume_in_cm3 = 1 / my_mat.density
my_mat.fispact_material
```

## Further Examples

Further examples can be found in the
[neutronics workshop task 11](https://github.com/fusion-energy/openmc_workshop/tree/master/tasks/task_11)
and in the [Documentation](https://neutronics-material-maker.readthedocs.io/en/latest/)


# Acknowledgement

Inspired by software projects [Pyne](https://pyne.io/) and making use of
[OpenMC](https://docs.openmc.org/en/stable/) functionality and the
[JSON](https://www.json.org/json-en.html) file format and
[PNNL](https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-15870Rev1.pdf)
for many definitions.
