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
- [Making material cards](#making_material_cards)
- [Changing the nuclear library](#chainging_the_nuclear_library)
- [Examples](#examples)
- [Todo](#todo)


# <a name="design-goals"></a>Design Goals
The material composition impacts the transport of neutrons and photons through the material. Neutronics codes attempt to simulate the transport of particles through matter and therefore require the material composition. This software aims to ease the creation of customisable materials for use in neutronics codes. The motivation behind this software was the need to create material cards for Helium and H20 coolants at different temperatures and pressures and material cards for a selection of lithium ceramics with different Li6 enrichments.

# <a name="features"></a>Features
- Generate **isotopes**, **elements**, **materials**, **chemical compounds** and **homogenised mixtures**.
- Create your own custom materials and chemical compounds or select from the internal database.
- Optional parameters for your creations include:
    - specified densities (g/cm3 or atoms per barn cm)
    - homogenisation fraction (volume or mass)
    - void fraction
    - elements present (atom fraction or mass fraction)
    - options for enriched isotopes
    - temperature (in Kelvin)
    - pressure (in Pa)
- Retrieve the properties from your crations, available properties include:
    - mat cards for Serpent and MCNP
    - density
    - zaids
    - isotopes present
    - elements present
    - element mass / atom fractions
    - preferential ACE file or nuclear data library

# <a name="installation"></a>Installation

Neutronics material maker is available here on the git repository or via the python package index.

- Install the package using pip.
```sh
pip install neutronics_material_maker
```

- Alternatively install the package by cloning this git repository and install locally.
```sh
git clone https://github.com/ukaea/neutronics_material_maker.git
cd neutronics_material_maker
python setup.py install
```

Should you wish you can also run the test suite. To do this you will need pytest installed.
```sh
pip install pytest
python setup.py test
```

# <a name="getting-started"></a>Getting started

The software can be used to create: **Isotopes**, **Elements**, **Compounds**, **Materials** or **Homogenised_mixture**. Properties such as density or material card can be accessed after creation. For example see the  **<a name="https://github.com/ukaea/neutronics_material_maker/blob/master/neutronics_material_maker/examples.py ">eamples.py</a>** file in the git repository or continue with this readme.

After installation try importing the package:

```python
from neutronics_material_maker.nmm import *
```



# <a name="making-isotopes"></a>Making Isotopes

Isotopes form the basic building blocks of more complex objects (**Element**). An **Isotope** can be created by specifying the symbol and the atomic number:
```python
example_isotope = Isotope('Li',7)
```
Isotopes can also be created by specifying the proton number and the atomic number.
```python
example_isotope = Isotope(3,7)
```

Once an isotope is created its properties can be queried.
```python
example_isotope.symbol
>>> Li
example_isotope.atomic_number
>>> 7
example_isotope.protons
>>> 3
example_isotope.neutrons
>>> 4
example_isotope.natural_abundance
>>> 0.926
example_isotope.mass_amu
>>> 7.0160034366
```
It is also possible to overwrite the natural abundance of an isotope upon creation. This comes in useful when creating enriched **Compounds** or **Materials** which is demonstrated later.
```python
example_natural_isotope = Isotope('Li',7)
example_natural_isotope.abundance
>>> 0.9241
example_enriched_isotope = Isotope('Li',7,abundance=0.5)
example_enriched_isotope.abundance
>>> 0.5
```
# <a name="making-elements"></a>Making Elements

Elements form other building blocks of more complex objects (**Compounds** and **Materials**). Elements can be created by specifying the symbol and optional enrichment. A simple element construct can be achieved with:
```python
example_element = Element('Li')
```
The natural abundance of an **Element** is known and the **Isotope** objects are created accordingly. Elemental properties can then be queried. In some cases lists of **Isotope** objects are returned.

```python
example_element.molar_mass_g
>>> 6.94003660292
example_element.protons
>>> 3
example_element.isotopes
>>> [<__main__.Isotope object at 0x7f23ba50bfd0>, <__main__.Isotope object at 0x7f23ba50bed0>]
example_element.full_name
>>> Lithium
```

Elements can also be created with enriched Isotope abundances.

```python
example_element = Element('Li',enriched_isotopes=(Isotope('Li', 6, abundance=0.9), Isotope('Li', 7, abundance=0.1)))
```

# <a name="making-compounds"></a>Making Compounds

Chemical equations are referred to as a **Compound** by the software. Compounds can be any valid chemical formula such as H2O, CO2 or C8H10N4O2.  

Compounds can be created using the following command, when both the compound chemical formula and the density in grams per cm3 are specified. If the **chemical_equation** keyword is not provided then the **chemical_equation** is assummed to be the first non keyword arguement.
```python
example_compound = Compound('C12H22O11',density_g_per_cm3=1.59)
example_compound = Compound(chemical_equation='C12H22O11',density_g_per_cm3=1.59)
```



mat_Li4SiO4 = Compound('Li4SiO4',
                       volume_of_unit_cell_cm3=1.1543e-21,
                       atoms_per_unit_cell=14,
                       packing_fraction=0.6,
                       enriched_isotopes=[Isotope('Li',7,abundance=0.6),Isotope('Li',6,abundance=0.4)])


Several fusion relevant compounds along with their crystalline volume can be found in the  **<a name="https://github.com/ukaea/neutronics_material_maker/blob/master/neutronics_material_maker/examples.py ">eamples.py</a>** file. Compounds included are: *Li4SiO4, Li2SiO3, Li2ZrO3, Li2TiO3, Be, Ba5Pb3, Nd5Pb4, Zr5Pb3, Zr5Pb4, Pb84.2Li15.8.*
```python
mat_Li4SiO4 = Compound(chemical_equation = 'Li4SiO4',
                       volume_of_unit_cell_cm3 = 1.1543e-21,
                       atoms_per_unit_cell = 14)
mat_Li4SiO4.density_g_per_cm3
>>> 2.4136389927905504
```
A **Compound** can also be enriched much like isotopes can. To enrich an **compound** the user must pass the desired abundances for the required isotopes in the element. Here is an example for enriched Li4SiO4 with Li6 abundance set to 0.6 and Li7 abundance set to 0.4. You can see that **Isotope** objects are used for this procedure.
```python
mat_Li4SiO4_enriched = Compound(chemical_equation = 'Li4SiO4',
                                volume_of_unit_cell_cm3=1.1543e-21,
                                atoms_per_unit_cell=14,
                                enriched_isotopes=[Isotope('Li',7,abundance=0.4),
                                                   Isotope('Li',6,abundance=0.6)])
mat_Li4SiO4_enriched.density_g_per_cm3
>>> 2.3713790240133186                    
```
Other input options for creating a **Compound** include setting a **packing_fraction** . The density of the resulting **Compound** is multiplied by the input packing fraction. This property is included to allow pebble beds.
```python
solid_ceramic = Compound('Be12Ti',
                         volume_of_unit_cell_cm3= 0.22724e-21,
                         atoms_per_unit_cell=2)
pebble_bed_ceramic = Compound('Be12Ti',
                              volume_of_unit_cell_cm3= 0.22724e-21,
                              atoms_per_unit_cell=2,
                              packing_fraction=0.64)
```
The density of the Compounds can be found with the density_g_per_cm3 property. Here we can see that the density of the pebble bed is lower than the solid ceramic.
```python
solid_ceramic.density_g_per_cm3
>>>2.2801067618505506
pebble_bed_ceramic.density_g_per_cm3
>>>1.4592683275843523
```
Other input options for Compounds include **pressure_Pa** and **temperature_K** which are used when calculating the density of ideal gases and liquids. To make use of this feature the thermo package must be installed.
```sh
pip install thermo
```

The density of liquids and gases accounting for thermal expansion can then be found. To use the ideal gas equations the **state_of_matter** must be specified as 'gas'.

```python
He_compound = Compound('He',
                       pressure_Pa = 8.0E6,
                       temperature_K = 823.0,
                       state_of_matter='gas')
He_compound.density_g_per_cm3
>>> 0.004682671945463105
```

Other coolants can also accept different **pressure_Pa** and **temperature_K** values and the density changes accordingly. The **state_of_matter** must also be specified as 'liquid'. This example shows the resulting change in density for water at different temperatures and pressures.
```python
water_compound = Compound('H2O',
                          pressure_Pa = 3100000,
                          temperature_K = 473.15,
                          state_of_matter='liquid')
water_compound.density_g_per_cm3
>>> 0.8664202359381719
water_compound = Compound('H2O',
                          pressure_Pa = 101325,
                          temperature_K = 293,
                          state_of_matter='liquid')
water_compound.density_g_per_cm3
>>> 0.9990449108576049
```

Once a **Compound** has been created various properties can be extracted including material cards suitable for use in Serpent (default) simulations with the **material_card(code='serpent')** and MCNP **material_card(code='mcnp')** method.
```python
example_compound = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
example_compound.enriched_isotopes
>>> <__main__.Isotope object at 0x7f859e27dfd0>, <__main__.Isotope object at 0x7f859e28d2d0>
example_compound.density_g_per_cm3
>>> 2.4132772544935666
example_compound.description
>>> Li4SiO4__Li6_0.9_Li7_0.1
example_compound.isotopes_atom_fractions
>>> [0.39999999999999997, 0.044444444444444446, 0.10246999999999999, 0.005205555555555555, 0.0034355555555555554, 0.4433644444444444, 0.00016888888888888889, 0.0009111111111111111]
example_compound.volume_m3
>>> 8.245e-29
example_compound.molar_mass
>>> 116.526000953
example_compound.elements
>>> [<__main__.Element object at 0x7fea0f159350>, <__main__.Element object at 0x7fea0f159290>, <__main__.Element object at 0x7fea0f1590d0>]
example_compound.material_card(code='serpent')
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
One novel feature of the software is the variations of the density of **Compounds** with isotope enrichment, the density and atom fractions are based on the actual isotopes present within the cryslaine latic. Creating different Compounds for use in parameter studies is easy with a for loop. Here the enrichment of Li6 is changed from 0.25 to 0.5, 0.75 then 1.0 and the calculated density of the resulting Li4SiO4 and normalised atom fractions are printed out each iteration of the loop. The density decreases slowly as Li7 atoms are replaced with Li6. The **material_card(code='serpent')** also changes accordingly. These density and atom fractions can then be input into other Material makers for codes such as [OpenMC](https://openmc.readthedocs.io/en/stable/pythonapi/generated/openmc.Material.html#openmc.Material) or [Pyne](http://pyne.io/usersguide/material.html).

```python
for enrichment in [0, 0.25, 0.5, 0.75, 1.0]:
   example_compound = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, abundance=enrichment), Isotope('Li', 7, abundance=1.0-enrichment)))
   print('Li6 enrichment=',enrichment)
   example_compound.density_g_per_cm3
   example_compound.isotopes_atom_fractions
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

The above feature is the main motivation behind the software as it allows the user to perform massive parameter studies on various candidate neutron multiplier materials and lithium ceramics for use in fusion breeder blankets.

# <a name="making-materials"></a>Making Materials

A custom **Material** can be constructed by specifiying the material **material_card_name**, density and either the isotopes or elemental composition.

One or more element can be specified with the **element** keyword along with the **element_atom_fraction** or **element_mass_fraction**.

Alternativly one or more isotopes can be specified using the **isotopes** keyword along with the **isotope_atom_fractions** or **isotopes_mass_fractions** that make up the material.

The density can be specified as **density_g_per_cm3** or **atom_density_per_barn_per_cm**.

The following example makes a material called Steel which is 95% weight Iron and 5% weight Carbon, with a density of 7.8g per cm3.

```python
mat_Steel= Material(material_card_name='Steel',
                    density_g_per_cm3=7.93,
                    density_atoms_per_barn_per_cm=8.58294E-02,
                    elements=[Element('Fe'),
                              Element('C')],
                    element_mass_fractions=[0.95,
                                    0.05])
```

The following two examples show how to construct materials using **Isotopes** along with either **Isotpe_mass_fraction** or **Isotope_atom_fraction**.
```python
mat_using_isotope_mass_fractions = Material(material_card_name='enriched_lithum',
                                            density_g_per_cm3=2.0,
                                            isotopes=[Isotope('Li',7),
                                                      Isotope('Li',6)],
                                            isotope_atom_fractions=[0.5,
                                                                    0.5],
                                            )

mat_using_isotope_atom_fractions = Material(material_card_name='enriched_lithum',
                                            density_g_per_cm3=2.0,
                                            isotopes=[Isotope('Li',7),
                                                      Isotope('Li',6)],
                                            isotope_mass_fractions=[0.5,
                                                                    0.5],
                                            )
```


The software has a some example **Materials** in the **<a name="https://github.com/ukaea/neutronics_material_maker/blob/master/neutronics_material_maker/examples.py ">eamples.py</a>** file. The elemental composition and densities of **Bronze**, **Eurofer**, **SS-316LN-IG**, **DT-plasma**,  **CuCrZr**, **Glass-fibre**, **Epoxy**, **Glass-fibre** and **Tungten** are included. Here is an example of 50:50 DT-plasma constructed using enriched elements.

```python
example_mat1 = Material(material_card_name='DT-plasma',
                          density_atoms_per_barn_per_cm=1e20,
                          elements=[Element(symbol='H',
                                            enriched_isotopes=[Isotope('H',2,abundance=0.5),
                                                               Isotope('H',3,abundance=0.5)])
                                    ],
                         element_mass_fractions=[1.0]
                        )
example_mat1.material_card(code='serpent')
>>> mat DT_plasma 1e-20
>>>     1002.31c 0.5
>>>     1003.31c 0.5
```
The other materials available are considerably more detailed in their isotope description. To keep this user manual concise only Glass-fibre and DT_plasma have been demonstrated. One difference between Materials is the known density, the software has materials with density in **atom_density_per_barn_per_cm** which is useful for Materials such as DT-plasma or **density_g_per_cm3** which is useful for Materials such as Glass-fibre. Neutronics codes such as Serpent can accept both options so this is not a problem (density in g/cm3 has a **-** flag to indicate the units).
```python
mat_Glass_fibre = Material(material_card_name='Glass-fibre',
                    density_g_per_cm3=2.49,
                    elements=[Element('H'),
                              Element('O'),
                              Element(12),
                              Element(13),
                              Element(14)
                             ],
                    element_mass_fractions=[0.0000383948,
                                    0.6328110447,
                                    0.0499936947,
                                    0.1026861642,
                                    0.2144707015
                                    ])
example_mat2.density_g_per_cm3
>>> 2.49
example_mat2.material_card(code='serpent')
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

Materials and Compounds can be combined to form a **Homogenised_mixture**. Any number of Materials and Compounds can be combined but they must combine to give a volume fraction of 1.0. Here are some examples:

```python
mat_bronze = Material(material_card_name='Bronze',
                        density_g_per_cm3=8.8775,
                        elements=[Element('Cu'),
                                  Element('Sn') ],
                        element_mass_fractions=[0.95,
                                        0.05 ])
mat_bronze.density_g_per_cm3
>>> 8.8775
mat_water = Compound('H2O',density_g_per_cm3=0.926)
mat_water.density_g_per_cm3
>>> 0.926
mat_CuCrZr = Compound('CuCrZr',density_g_per_cm3=8.814)
mat_CuCrZr.density_g_per_cm3
>>> 8.814
```

The two Compounds and 1 Material can then be mixed with **volume_fraction** the following way. This Homogenised_mixture contains 20% volume Water, 30% volume CuCrZr and 50% Bronze.
```python
mat_mix = Homogenised_mixture(mixtures=[mat_water,
                                          mat_CuCrZr,
                                          mat_bronze],
                                volume_fractions=[0.20
                                                 0.30
                                                 0.5])
mat_mix.density_g_per_cm3
>>> 7.26815
```

The resulting material card comprises of the combined three material cards with modified atom fractions to account for the volume fraction of each component. The material name is also based on the combination of the three components along with their **volume_fractions**.

```python
mat_mix.material_card(code='serpent')
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
new_mat_mix = Homogenised_mixture([{'mix':mat_water,'mass_fraction':0.5},
                                         {'mix':mat_CuCrZr,'mass_fraction':0.5}])
new_mat_mix.density_g_per_cm3
>>> 1.6759268993839835
```

Void fractions can also be inserted into a **Homogenised_mixture**. In the example below, a new material is made from 50% volume fraction Nb3Sn and 50% void. The density of the Nb3Sn is specified as 8.91g per cm3 and a void is 0g per cm3. The resulting example material has a desnity of 4.455g per cm3 as expected.
```python
mat_Nb3Sn = Compound('Nb3Sn',density_g_per_cm3=8.91)
mat_void= Material(material_card_name='Void',
                     density_g_per_cm3=0,
                     elements=[ ],
                     element_mass_fractions=[  ]
                    )

example_mat =Homogenised_mixture(mixtures=[mat_Nb3Sn,mat_void],
                                   volume_fractions=[0.5,0.5])

example_mat.density_g_per_cm3
>>>4.455
```

**Homogenised_mixture** can also be **squashed** which combines duplicate isotopes. This setting is False by default but setting it to true can be achieved using the following command:
```
mat_mix.material_card(code='serpent',squashed=True)
```

The **material_card** for **Homogenised_mixture** can also be producing using isotope mass fractions instead of the default isotope atom fractions. Mass fractions can be achieved using **fractions** keyword:
```
mat_mix.material_card(fractions='isotope mass fractions')
```

# <a name="material_cards"></a>Making material cards

Isotopes, Elements, Materials and Compounds can all generate material cards for Serpent 2, MCNP and Fispact 2. Once your object has been created then use the **.material_card()** method along with optional arguments to get the material card.

Arguments can be passed to the **.material_card()** method or specified with the object upton creation. Permitted arguments are :
- material_card_name [string] used by Serpent,
- material_card_number [int] used by MCNP,
- material_card_comment [string]
- color [rgb tuple] used by Serpent,
- code ['serpent','mcnp','fispact'],
- fractions ['isotope atom fractions','isotope mass fractions'] used by MCNP and Serpent,
- temperature_K [float] used by Serpent
- volume_cm3 [float] required for Fispact outputs

```python
a=Material(density_g_per_cm3=7,
           isotopes=[Isotope('Sn',112),Isotope('Be',9)],
           isotope_atom_fractions=[0.5,0.5])
a.material_card(code='mcnp',material_card_number=5, material_card_comment='my material',fractions='isotope mass fractions')

c  
c  my material
c  density =7.0 g/cm3
c  density =0.06972548702136161 atoms per barn cm2
c  temperature =293.15 K
M5
   50112.31c   0.5                      $ Tin_112
   4009.31c    0.5                      $ Beryllium_9
```

# <a name="chainging_the_nuclear_library"></a>Changing the nuclear library

Serpent, MCNP material cards can contain a pointer to the desired nuclear cross section file. The pointer is optinal but if included it appears after the zaid entry in the material card. When importing neutronics_material_maker it attempts to import a default Serpent 2 xsdir file and find the preferential nuclear library evaluation for each isotope present in the xsdir. If no file is found or the particular isotope is not found then the optional nuclear library is left blank in material cards. The default path of the xsdir file is **/opt/serpent2/xsdir.serp**, however this can be changed using the **set_xsdir(filename)** function as demonstrated below.

```python
from neutronics_material_maker.examples import *
example_isotope = Isotope(3,6)
example_isotope.nuclear_library
>>> .31c
set_xsdir('xsdir_TENDL.serp')
example_isotope = Isotope(3,6)
>>> .10c
```


# <a name="examples"></a>Examples
Some example materials are available for importing

```python
from neutronics_material_maker.examples import *
```

The examples include Li4SiO4, Li2SiO3, Li2ZrO3, Li2TiO3, Be12Ti, Ba5Pb3, Nd5Pb4, Zr5Pb3, Lithium_Lead, Tungsten, Eurofer, SS316LN_IG, Bronze, Glass_fibre, Epoxy, CuCrZr, DT plasma and Void. The construction of these materials can be seen in the [examples.py](https://github.com/ukaea/neutronics_material_maker/blob/master/neutronics_material_maker/examples.py) file

# <a name="todo"></a>Todos
 - Write MORE Tests and improve code coverage
 - Add fispact writter to elements, isotopes, compounds and homogenised Materials
 - Add squash option to all material cards
 - Combine with engineering materials database
 - Address #todo comments in the code


# <a name="acknowledgements"></a>Acknowledgements

Isotope natural abundance and mass data from [Nist](https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses)
