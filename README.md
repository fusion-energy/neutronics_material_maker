[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)
[![Build Status](https://travis-ci.org/ukaea/neutronics_material_maker.svg?branch=master)](https://travis-ci.org/ukaea/neutronics_material_maker)
# Design goals
The material composition impacts the transport of neutrons and photons through the material. Neutronics codes attempt to simulate the transport of particles through matter and therefore require the material composition. This software aims to ease the creation of customisable materials for use in neutronics codes

# Features
- Generate isotopes, materials, **chemical compounds** and homogenised mixtures
- Retrieve isotope compositions, isotopes fractions and material density and **material cards for Serpent**
- Customise your creations with optional **isotope enrichment**, packing fractions and specified densities

# Installation

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

# Getting started

The software can be used to create isotopes, elements, compounds, materials or homogenised mixtures. Properties such as density or material card can be accessed after creation.

After installation users must import the package

```sh
$ import neutronics_material_maker as nmm
```

# Making Isotopes

Isotope form the basic building blocks of more complex objects (elements). Isotope can be created by specifying the symbol and the atomic number
```sh
$ example_isotope = nmm.Isotope('Li',7)
```
Isotope can be created by specifying the proton number and the atomic number
```sh
$ example_isotope = nmm.Isotope(3,7)
```

Once an isotope is created it's properties can be queried.
```sh
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
$ example_isotope.description
>>> {'abundance': 0.9241, 'atomic_number ': 7, 'mass_amu': 7.0160034366, 'protons': 3, 'neutrons': 4, 'isotope ': 'Li'}
```
It is also possible to overwrite the natural abundance of an isotope upon creation. This comes in useful when creating enriched compounds.
```sh
$ example_natural_isotope = nmm.Isotope('Li',7)
$ example_natural_isotope.abundance
>>> 0.9241
$ example_enriched_isotope = nmm.Isotope('Li',7,0.5)
$ example_enriched_isotope.abundance
>>> 0.5
```
# Making Elements

Elements form another building blocks of more complex objects (compounds). Elements can be created by specifying the symbol and optional enrichment. A simple element construct can be achieved with ...
```sh
$ example_element = nmm.Element('Li')
```
The natural abundance of Elements is known and the isotopes are created accordingly. Elemental properties can then be queried. In some cases lists of Isotope objects are returned

```sh
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

```sh
$ example_element = nmm.Element('Li',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
```

# Making Compounds

Chemical equations are referred to as Compounds by the software. Compounds can be any valid chemical formula such as H2O, CO2 or C8H10N4O2.  

Compounds can be created using the following command when both the compound chemical formula and the density in grams per cm3 are specified.
```sh
$ example_compound = nmm.Compound('C12H22O11',density_g_per_cm3=1.59)
```
The software knows about the crystalline volume of some chemical formula (using a small internal material database) and can create some compound without the density_g_per_cm3 argument. Compounds that the software knows the crystalline volume or atoms per cm3 for are mainly fusion relevant materials Li4SiO4, Li2SiO3, Li2ZrO3, Li2TiO3, Be, Ba5Pb3, Nd5Pb4, Zr5Pb3, Zr5Pb4, Pb84.2Li15.8. For these compounds they can be create without the density argument. 
```sh
$ example_compound = nmm.Compound('Li4SiO4')
$ example_compound.density_g_per_cm3
>>> 2.4136389927905504
```
Compounds can also be enriched much like isotopes can. To enrich an compound one must pass the desired abundances for the required isotopes in the element. Here is an example for enriched Li2ZrO3 with Li6 abundance set to 0.9 and Li7 abundance set to 0.1. You can see that Isotope objects are used for this procedure.
```sh
nmm.Compound('Li2ZrO3',enriched_isotopes=(nmm.Isotope('Li', 6, 0.9), nmm.Isotope('Li', 7, 0.1)))
```
Other input options for creating Compounds include setting a **packing_fraction** and **theoretical_density** which both perform the same operation. The density of the resulting compound is multiplied by the input packing fraction or theoretical density. Both are included to allow pebble beds to be created which are made of pebbles that are not at 100% density.
```sh
$ solid_ceramic = nmm.Compound('Be12Ti')
$ pebble_bed_ceramic = nmm.Compound('Be12Ti',packing_fraction=0.64)
```
The density of the two Compounds can be found with the density_g_per_cm3 property.
```sh
$ solid_ceramic.density_g_per_cm3
>>>2.2801067618505506
$ pebble_bed_ceramic.density_g_per_cm3
>>>1.4592683275843523
```
Other input options for Compounds include **pressure_Pa** and **temperature_K** which are used when calculating the density of ideal gases. This function only works for Helium at the moment but could be expanded in the future.
```sh
$ He_compound = nmm.Compound('He', pressure_Pa = 8.0E6, temperature_K = 823.0)
$ He_compound.density_g_per_cm3_idea_gas
>>> 0.004682671945463105
```

Once a compound has been created various properties can be extracted including material cards suitable for use in Serpent II simulations.
```sh
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
One novel feature of the software is the variations of Compound density and atom fractions based on the actual isotopes present within the cryslaine latic. Creating different Compounds for use in parameter studies is easy with a for loop. Here the enrichment of Li6 is changed from 0.25 to 0.5, 0.75 then 1.0 and the calculated density of the resulting Li4SiO4 is returned each time. The density decreases slowly as Li7 atoms are replaced with Li6. The **serpent_material_card** also changes accordingly. These density an atom fractions can then be input into other Material makers for codes such as [OpenMC](https://openmc.readthedocs.io/en/stable/pythonapi/generated/openmc.Material.html#openmc.Material) or [Pyne](http://pyne.io/usersguide/material.html)

```sh
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

The above feature is the main motivation behind the software as it allows me to perform massive parameter studies on various candidate neutron multiplier materials and lithium ceramics for use in fusion breeder blankets

# Making Materials

Custom materials can be constructed by specifiying the material **description**, density and elements that make up the material along with their **mass_faction** or **atom_fraction** . The density can be specified as **density_g_per_cm3** or **atom_density_per_barn_per_cm**. The following example makes a material called Steel which as 95% weight Iron and 5% weight Carbon.

```sh
m5 = nmm.Material('Steel',
                   density_g_per_cm3=7.8,
                   elements_and_fractions=[{'element':nmm.Element('Fe'),'mass_fraction':0.95},
                                           {'element':nmm.Element('C') ,'mass_fraction':0.05}])
```

The software has a small internal database and knows the elemental composition and densities of some materials. The list of Materials can easily be expanded but currently includes **Bronze**, **Eurofer**, **SS-316LN-IG**, **DT-plasma**,  **CuCrZr_with_impurities**, **Glass-fibre** and **Epoxy**.

```sh
$ example_mat1 = nmm.Material('DT_plasma')
$ example_mat1.atom_density_per_barn_per_cm
>>> 1e-20
$ example_mat1.serpent_material_card
>>> mat DT_plasma 1e-20
>>>     1002.31c 0.5
>>>     1003.31c 0.5
```
The other materials available are considerably more detailed in their isotope description. To keep this user manual concise only Glass-fibre and DT_plasma have been demonstrated. One difference between Materials is the known density, the software has materials with density in **atom_density_per_barn_per_cm** which is useful for Materials such as DT-plasma or **density_g_per_cm3** which is useful for Materials such as Glass-fibre. Neutronics codes such as Serpent can accept both options so this is not a problem (density in g/cm3 has a **-** flag to indicate the units).
```sh
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

# Making Homogenised_mixtures

Materials and Compounds can be combined to form a Homogenised_mixture. Any number of Materials and Compounds can be combined but they must combine to give a volume fraction of 1.0. Here are some examples ...

```sh
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
```sh
$ mat_mix = nmm.Homogenised_mixture([{'mix':mat_water,'volume_fraction':0.20},
                                     {'mix':mat_CuCrZr,'volume_fraction':0.30},
                                     {'mix':mat_bronze,'volume_fraction':0.5}])
$ mat_mix.density_g_per_cm3
>>> 7.26815
```

The resulting material card comprises of the combined three material cards with modified atom fractions to account for the volume fraction of each component. The material name is also based on the combination of the three components along with their **volume_fractions**.

```sh
$ mat_mix.serpent_material_card
>>> mat H2O_vf_0.2_CuCrZr_vf_0.3_Bronze_vf_0.5_  -7.26815
>>>     1001.31c 0.13331800000000002
>>>     1002.31c 1.5333333333333334e-05
>>>     8016.31c 0.06650466666666666
>>>     8017.31c 2.5333333333333334e-05
>>>     8018.31c 0.00013666666666666666
>>>     29063.31c 0.06914999999999999
>>>     29065.31c 0.03085
>>>     24050.31c 0.004345
>>>     24052.31c 0.08378899999999999
>>>     24053.31c 0.009500999999999999
>>>     24054.31c 0.0023649999999999995
>>>     40090.31c 0.051449999999999996
>>>     40091.31c 0.011219999999999999
>>>     40092.31c 0.017150000000000002
>>>     40094.31c 0.01738
>>>     40096.31c 0.0027999999999999995
>>>     29063.31c 0.3284625
>>>     29065.31c 0.1465375
>>>     50112.31c 0.0002425
>>>     50114.31c 0.000165
>>>     50115.31c 8.5e-05
>>>     50116.31c 0.003635
>>>     50117.31c 0.0019199999999999998
>>>     50118.31c 0.0060550000000000005
>>>     50119.31c 0.0021475
>>>     50120.31c 0.008145
>>>     50122.31c 0.0011575000000000001
>>>     50124.31c 0.0014475
```

Homogenised_mixture can also be formed from Compounds and Materials based on **mass_fraction**. The two Compounds and 1 Material are mixed with **mass_fraction** in the following way. This Homogenised_mixture contains 20% mass Water and 30% mass CuCrZr.
```sh
$ new_mat_mix = nmm.Homogenised_mixture([{'mix':mat_water,'mass_fraction':0.50},
                                         {'mix':mat_CuCrZr,'mass_fraction':0.50}])
$ new_mat_mix.density_g_per_cm3
>>> 1.6759268993839835
```

### Todos
 - Write MORE Tests and improve code coverage
 - Improve gas Compounds and Materials
 - Add some more Materials to the collection
 - Combine with engineering materials database
 - Make a GUI
 - address #todo comments in the code

### Acknowledgements

Isotope natural abundance and mass data from [Nist](https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses)
