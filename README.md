# **Neutronics material maker user manual**

[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)
[![Build Status](https://travis-ci.org/ukaea/neutronics_material_maker.svg?branch=master)](https://travis-ci.org/ukaea/neutronics_material_maker)

- [Design goals](#design-goals)
- [Features](#features)
- [Installation](#installation)
- [Getting started](#getting-started)
- [Making Isotopes](#making-isotopes)
- [Making Elements](#making-elements)
- [Making Compounds](#making-compounds)
- [Making Materials](#making-materials)
- [Making Homogenised_mixtures](#making-homogenised_mixtures)
- [Todo](#todo)


# <a name="design-goals"></a>Design Goals
The material composition impacts the transport of neutrons and photons through the material. Neutronics codes attempt to simulate the transport of particles through matter and therefore require the material composition. This software aims to ease the creation of customisable materials for use in neutronics codes. The motivation behind this software was the need to create material cards for Helium and H20 coolants at different temperatures and pressures and material cards for a selection of lithium ceramics with different Li6 enrichments.

# <a name="features"></a>Features
- Generate **isotopes**, **elements**, **materials**, **chemical compounds** and **homogenised mixtures**.
- Create your own custom materials and chemical compounds or select from the internal database.
- Optional parameters for your creations include:
    - packing fractions,
    - theoretical density fraction,
    - specified densities,
    - homogenisation fraction (volume or mass),
    - void fraction ,
    - elements present (atom fraction or mass fraction)
    - options for enriched isotopes
    - temperature (in Kelvin)
    - pressure (in Pa)
- Retrieve the properties from your crations, available properties include:
    - mat cards for Serpent
    - density
    - zaids
    - isotopes present
    - elements present
    - element mass / atom fractions

# <a name="installation"></a>Installation

Neutronics material maker is available here on the git repository or via the python package index

- install the package using pip
```sh
$ pip install neutronics_material_maker
```

- Alternatively install the package by cloning this git repository and install locally
```sh
$ git clone git@github.com:ukaea/neutronics_material_maker.git
$ cd neutronics_material_maker
$ python setup.py install
```

Should you wish you can also run the test suite. To do this you will need pytest installed.
```sh
$ pip install pytest
$ python setup.py test
```

# <a name="getting-started"></a>Getting started

The software can be used to create isotopes, elements, compounds, materials or homogenised mixtures. Properties such as density or material card can be accessed after creation.

After installation users must import the package

```python
$ import neutronics_material_maker as nmm
```

# <a name="making-isotopes"></a>Making Isotopes

Isotopes form the basic building blocks of more complex objects (**Element**). An **Isotope** can be created by specifying the symbol and the atomic number
```python
$ example_isotope = nmm.Isotope('Li',7)
```
Isotope can also be created by specifying the proton number and the atomic number
```python
$ example_isotope = nmm.Isotope(3,7)
```

Once an isotope is created it's properties can be queried.
```python
$ example_isotope.symbol
>>> Li
$ example_isotope.atomic_number
>>> 7
$ example_isotope.protons
>>> 3
$ example_isotope.neutrons
>>> 4
$ example_isotope.natural_abundance
>>> 0.926
$ example_isotope.mass_amu
>>> 7.0160034366
$ example_isotope.description
>>> {'abundance': 0.9241, 'atomic_number ': 7, 'mass_amu': 7.0160034366, 'protons': 3, 'neutrons': 4, 'isotope ': 'Li'}
```
It is also possible to overwrite the natural abundance of an isotope upon creation. This comes in useful when creating enriched **Compounds** or **Materials** which is demonstrated later.
```python
$ example_natural_isotope = nmm.Isotope('Li',7)
$ example_natural_isotope.abundance
>>> 0.9241
$ example_enriched_isotope = nmm.Isotope('Li',7,0.5)
$ example_enriched_isotope.abundance
>>> 0.5
```
# <a name="making-elements"></a>Making Elements

Elements form another building blocks of more complex objects (**Compounds** and **Materials**). Elements can be created by specifying the symbol and optional enrichment. A simple element construct can be achieved with ...
```python
$ example_element = nmm.Element('Li')
```
The natural abundance of an **Element** is known and the **Isotope** objects are created accordingly. Elemental properties can then be queried. In some cases lists of **Isotope** objects are returned

```python
$ example_element.natural_isotopes_in_elements
>>>[<__main__.Isotope object at 0x7f23ba50bed0>, <__main__.Isotope object at 0x7f23ba50bf50>]
$ example_element.molar_mass_g
>>> 6.94003660292
$ example_element.protons
>>> 3
$ example_element.isotopes
>>> [<__main__.Isotope object at 0x7f23ba50bfd0>, <__main__.Isotope object at 0x7f23ba50bed0>]
$ example_element.full_name
>>> Lithium
```

Elements can also be created with enriched Isotope abundances.

```python
$ example_element = nmm.Element('Li',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
```

# <a name="making-compounds"></a>Making Compounds

Chemical equations are referred to as Compounds by the software. Compounds can be any valid chemical formula such as H2O, CO2 or C8H10N4O2.  

Compounds can be created using the following command when both the compound chemical formula and the density in grams per cm3 are specified.
```python
$ example_compound = nmm.Compound('C12H22O11',density_g_per_cm3=1.59)
```
The software knows about the crystalline volume of some chemical formula (using a small internal material database) and can therefore create some compound without the density_g_per_cm3 argument. Compounds that the software knows the crystalline unit volume or atoms per cm3 for are mainly fusion relevant materials *Li4SiO4, Li2SiO3, Li2ZrO3, Li2TiO3, Be, Ba5Pb3, Nd5Pb4, Zr5Pb3, Zr5Pb4, Pb84.2Li15.8.* For these compounds they can be create without the density argument.
```python
$ example_compound = nmm.Compound('Li4SiO4')
$ example_compound.density_g_per_cm3
>>> 2.4136389927905504
```
A **Compound** can also be enriched much like isotopes can. To enrich an **compound** the user must pass the desired abundances for the required isotopes in the element. Here is an example for enriched Li2ZrO3 with Li6 abundance set to 0.9 and Li7 abundance set to 0.1. You can see that **Isotope** objects are used for this procedure.
```python
nmm.Compound('Li2ZrO3',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
```
Other input options for creating a **Compound** include setting a **packing_fraction** and **theoretical_density** which both perform the same operation. The density of the resulting **Compound** is multiplied by the input packing fraction or theoretical density. Both are included to allow pebble beds to be created which are made of pebbles that are not at 100% density.
```python
$ solid_ceramic = nmm.Compound('Be12Ti')
$ pebble_bed_ceramic = nmm.Compound('Be12Ti',packing_fraction=0.64)
```
The density of the Compounds can be found with the density_g_per_cm3 property. Here we can see that the density of the pebble bed is lower than the solid ceramic.
```python
$ solid_ceramic.density_g_per_cm3
>>>2.2801067618505506
$ pebble_bed_ceramic.density_g_per_cm3
>>>1.4592683275843523
```
Other input options for Compounds include **pressure_Pa** and **temperature_K** which are used when calculating the density of ideal gases and liquids. To make use of this feature the thermo package must be installed.
```sh
pip install thermo
```

The density of liquids and gases accounting for thermal expansion can then be found. To use the ideal gas equations the **state_of_matter** must be specified as 'gas'.

```python
$ He_compound = nmm.Compound('He', pressure_Pa = 8.0E6, temperature_K = 823.0, state_of_matter='gas')
$ He_compound.density_g_per_cm3
>>> 0.004682671945463105
```

Other coolants can also accept different **pressure_Pa** and **temperature_K** values and the density changes accordingly. The **state_of_matter** must also be specified as 'liquid'. This example shows the resulting change in density for water at different temperatures and pressures.
```python
$ water_compound = nmm.Compound('H2O', pressure_Pa = 3100000, temperature_K = 473.15, state_of_matter='liquid')
$ water_compound.density_g_per_cm3
>>> 0.8664202359381719
$ water_compound = nmm.Compound('H2O', pressure_Pa = 101325, temperature_K = 293, state_of_matter='liquid')
$ water_compound.density_g_per_cm3
>>> 0.9990449108576049
```

Once a **Compound** has been created various properties can be extracted including material cards suitable for use in Serpent II simulations (**serpent_material_card**).
```python
$ example_compound = nmm.Compound('Li4SiO4',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
$ example_compound.enriched_isotopes
>>> <__main__.Isotope object at 0x7f859e27dfd0>, <__main__.Isotope object at 0x7f859e28d2d0>
$ example_compound.density_g_per_cm3
>>> 2.4132772544935666
$ example_compound.description
>>> Li4SiO4__Li6_0.9_Li7_0.1
$ example_compound.isotopes_atom_fractions
>>> [0.39999999999999997, 0.044444444444444446, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
$ example_compound.volume_m3
>>> 8.245e-29
$ example_compound.molar_mass
>>> 116.526000953
$ example_compound.elements
>>> [<__main__.Element object at 0x7fea0f159350>, <__main__.Element object at 0x7fea0f159290>, <__main__.Element object at 0x7fea0f1590d0>]
$ example_compound.serpent_material_card
>>> mat Li4SiO4__Li6_0.9_Li7_0.1 -2.34719115762
>>>    3006.31c 0.4
>>>    3007.31c 0.0444444444444
>>>    14028.31c 0.10247
>>>    14029.31c 0.00520555555556
>>>    14030.31c 0.00343555555556
>>>    8016.31c 0.443364444444
>>>    8017.31c 0.000168888888889
>>>    8018.31c 0.000911111111111
```
One novel feature of the software is the variations of the **Compound** object is that the density and atom fractions are based on the actual isotopes present within the cryslaine latic. Creating different Compounds for use in parameter studies is easy with a for loop. Here the enrichment of Li6 is changed from 0.25 to 0.5, 0.75 then 1.0 and the calculated density of the resulting Li4SiO4 and normalised atom fractions are printed out each iteration of the loop. The density decreases slowly as Li7 atoms are replaced with Li6. The **serpent_material_card** also changes accordingly. These density an atom fractions can then be input into other Material makers for codes such as [OpenMC](https://openmc.readthedocs.io/en/stable/pythonapi/generated/openmc.Material.html#openmc.Material) or [Pyne](http://pyne.io/usersguide/material.html)

```python
$ for enrichment in [0, 0.25, 0.5, 0.75, 1.0]:
$    example_compound = nmm.Compound('Li4SiO4',enriched_isotopes=(nmm.Isotope('Li', 6, enrichment), nmm.Isotope('Li', 7, 1.0-enrichment)))
$    print('Li6 enrichment=',enrichment)
$    example_compound.density_g_per_cm3
$    example_compound.isotopes_atom_fractions
>>> Li6 enrichment= 0
>>> 2.419758869855734
>>> [0.0, 0.4444444444444444, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
>>> Li6 enrichment= 0.25
>>> 2.399601172012573
>>> [0.1111111111111111, 0.3333333333333333, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
>>> Li6 enrichment= 0.5
>>> 2.379443474169413
>>> [0.2222222222222222, 0.2222222222222222, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
>>> Li6 enrichment= 0.75
>>> 2.359285776326253
>>> [0.3333333333333333, 0.1111111111111111, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
>>> Li6 enrichment= 1.0
>>> 2.3391280784830926
>>> [0.4444444444444444, 0.0, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
```

The above feature is the main motivation behind the software as it allows me to perform massive parameter studies on various candidate neutron multiplier materials and lithium ceramics for use in fusion breeder blankets.

# <a name="making-materials"></a>Making Materials

A custom **Material** can be constructed by specifiying the material **description**, density and one or more **Element** in the **elements_and_fractions** parameter that make up the material. The density can be specified as **density_g_per_cm3** or **atom_density_per_barn_per_cm**. The **Elements** need to be specified with either a **mass_faction** or an **atom_fraction**. The following example makes a material called Steel which as 95% weight Iron and 5% weight Carbon with a density of 7.8g per cm3.

```python
m5 = nmm.Material(description='Steel',
                  density_g_per_cm3=7.8,
                  elements_and_fractions=[{'element':nmm.Element('Fe'),'mass_fraction':0.95},
                                          {'element':nmm.Element('C') ,'mass_fraction':0.05}])
```

The software has a small internal database and knows the elemental composition and densities of some materials. The list of Materials can easily be expanded but currently includes **Bronze**, **Eurofer**, **SS-316LN-IG**, **DT-plasma**,  **CuCrZr**, **Glass-fibre**, **Epoxy**, **Glass-fibre** and **Tungten**. Here is an example of DT-plasma.

```python
$ example_mat1 = nmm.Material('DT_plasma')
$ example_mat1.atom_density_per_barn_per_cm
>>> 1e-20
$ example_mat1.serpent_material_card
>>> mat DT_plasma 1e-20
>>>     1002.31c 0.5
>>>     1003.31c 0.5
```
The other materials available are considerably more detailed in their isotope description. To keep this user manual concise only Glass-fibre and DT_plasma have been demonstrated. One difference between Materials is the known density, the software has materials with density in **atom_density_per_barn_per_cm** which is useful for Materials such as DT-plasma or **density_g_per_cm3** which is useful for Materials such as Glass-fibre. Neutronics codes such as Serpent can accept both options so this is not a problem (density in g/cm3 has a **-** flag to indicate the units).
```python
$ example_mat2 = nmm.Material('Glass-fibre')
$ example_mat2.density_g_per_cm3
>>> 2.49
$ example_mat2.serpent_material_card
>>> mat Glass-fibre -2.49
>>>     1001.31c 3.8390384598e-05
>>>     1002.31c 4.415402e-09
>>>     8016.31c 0.631273313861
>>>     8017.31c 0.000240468196986
>>>     8018.31c 0.00129726264164
>>>     12024.31c 0.0394900194435
>>>     12025.31c 0.00499936947
>>>     12026.31c 0.00550430578647
>>>     13027.31c 0.1026861642
>>>     14028.31c 0.197791315044
>>>     14029.31c 0.0100479523653
>>>     14030.31c 0.00663143409038
```



# <a name="making-homogenised_mixtures"></a>Making Homogenised_mixtures

Materials and Compounds can be combined to form a **Homogenised_mixture**. Any number of Materials and Compounds can be combined but they must combine to give a volume fraction of 1.0. Here are some examples ...

```python
$ mat_bronze = nmm.Material('Bronze')
$ mat_bronze.density_g_per_cm3
>>> 8.8775
$ mat_water = nmm.Compound('H2O',density_g_per_cm3=0.926)
$ mat_water.density_g_per_cm3
>>> 0.926
$ mat_CuCrZr = nmm.Compound('CuCrZr',density_g_per_cm3=8.814)
$ mat_CuCrZr.density_g_per_cm3
>>> 8.814
```

The two Compounds and 1 Material can then be mixed with **volume_fraction** the following way. This Homogenised_mixture contains 20% volume Water, 30% volume CuCrZr and 50% Bronze.
```python
$ mat_mix = nmm.Homogenised_mixture([{'mix':mat_water,'volume_fraction':0.20},
                                     {'mix':mat_CuCrZr,'volume_fraction':0.30},
                                     {'mix':mat_bronze,'volume_fraction':0.5}])
$ mat_mix.density_g_per_cm3
>>> 7.26815
```

The resulting material card comprises of the combined three material cards with modified atom fractions to account for the volume fraction of each component. The material name is also based on the combination of the three components along with their **volume_fractions**.

```python
$ mat_mix.serpent_material_card
>>> mat H2O_vf_0.2_CuCrZr_vf_0.3_Bronze_vf_0.5  -7.26815
>>> %   
>>> %   H2O with a density of 0.926gcm-3
>>> %   volume fraction of 0.2
>>> %   mass fraction of 0.0254810371277
>>>     1001.31c 0.161622473319
>>>     1002.31c 1.85887221347e-05
>>>     8016.31c 0.0806241371301
>>>     8017.31c 3.07118017878e-05
>>>     8018.31c 0.000165682088592
>>> %   
>>> %   CuCrZr with a density of 8.814gcm-3
>>> %   volume fraction of 0.3
>>> %   mass fraction of 0.363806470697
>>>     29063.31c 0.0695231818437
>>>     29065.31c 0.0310164882122
>>>     24050.31c 0.00436844866393
>>>     24052.31c 0.0842411841431
>>>     24053.31c 0.00955227405201
>>>     24054.31c 0.00237776319682
>>>     40090.31c 0.0517276602438
>>>     40091.31c 0.0112805509803
>>>     40092.31c 0.0172425534146
>>>     40094.31c 0.0174737946557
>>>     40096.31c 0.00281511076157
>>> %   
>>> %   Bronze with a density of 8.8775gcm-3
>>> %   volume fraction of 0.5
>>> %   mass fraction of 0.610712492175
>>>     29063.31c 0.345745900177
>>>     29065.31c 0.154248170939
>>>     50112.31c 0.000255260131043
>>>     50114.31c 0.000173682151019
>>>     50115.31c 8.94726232523e-05
>>>     50116.31c 0.00382627041791
>>>     50117.31c 0.0020210286664
>>>     50118.31c 0.00637360863285
>>>     50119.31c 0.00226049951099
>>>     50120.31c 0.00857358254576
>>>     50122.31c 0.00121840660488
>>>     50124.31c 0.00152366614303
```

Homogenised_mixture can also be formed from Compounds and Materials based on **mass_fraction**. The two Compounds and 1 Material are mixed with **mass_fraction** in the following way. This Homogenised_mixture contains 20% mass Water and 30% mass CuCrZr.
```python
$ new_mat_mix = nmm.Homogenised_mixture([{'mix':mat_water,'mass_fraction':0.5},
                                         {'mix':mat_CuCrZr,'mass_fraction':0.5}])
$ new_mat_mix.density_g_per_cm3
>>> 1.6759268993839835
```

Void fractions can also be inserted into a **Homogenised_mixture**. In the example below a new materials is made from 50% volume fraction Nb3Sn and 50% void. The density of the Nb3Sn is specified as 8.91g per cm3 and a void is 0g per cm3. The resulting example material has a desnity of 4.455g per cm3 as expected.
```python
$ mat_Nb3Sn = nmm.Compound('Nb3Sn',density_g_per_cm3=8.91)
$ mat_void = nmm.Material('Void')

$ example_mat =nmm.Homogenised_mixture([{'mix':mat_Nb3Sn, 'volume_fraction':0.5},
                                        {'mix':mat_void, 'volume_fraction':0.5}])

$ example_mat.density_g_per_cm3
>>>4.455
```

# <a name="todo"></a>Todos
 - Write MORE Tests and improve code coverage
 - Improve Materials (allow material made of isotopes aswell as elements)
 - Add some more Materials to the collection
 - Combine with engineering materials database
 - Make a GUI
 - Address #todo comments in the code
 - demonstrate unit conversion features for pressure (in bars or Pa) and temperature (in degC or Kelvin)

# <a name="acknowledgements"></a>Acknowledgements

Isotope natural abundance and mass data from [Nist](https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses)
