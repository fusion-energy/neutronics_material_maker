[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)
# Design goals
The material composion impacts the transport of neutrons and photons through the material and therefore neutronics codes require information on the material composition to accuratly model particle behaviour. This software aims to ease the creation of customisable materials for use in neutronics codes

# Features
- Generate isotopes, materials, chemical compounds, homgenised mixtures 
- Retrieve isotope compostions, isotopes fractions and density
- Customise your creation with optional isotope enrichment, packing fractions and more

# Installation

Neutronics material make is availabe here on the git repository or via the python package index
- install the package by cloning this git repository
```sh
$ git clone git@github.com:ukaea/neutronics_material_maker.git
```
- install the package using pip
```sh
$ pip install neutronics_material_maker
```

# Getting started

The software can be used to create isotopes, compounds, materials or homogenised mixtures. Properties such as density or material card can be accessed after creation. 

After installation users must import the package

```sh
$ import neutronics_material_maker
```

# Making isotopes

Isotope form the basic building blocks of more complex objects (elements). Isotope can be created by specifiy the symbol and the atomic number
```sh
$ example_isotope = Isotope('Li',7)
```
Isotope can be created by specifiy the proton number and the atomic number
```sh
$ example_isotope = Isotope(3,7)
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
It is also possible to overwrite the natural abundance of an isotope upon creation. This comes in usefull later when creating enriched compounds
```sh
$ example_isotope = Isotope('Li',7,0.5)
>>> Li
$ example_isotope.abundance
>>> 0.5
```
# Making elements

Elements form another building blocks of more complex objects (compounds). Elements can be created by specifiy the symbol and optional enrichment. A simple element construct can be achieved with ...
```sh
$ example_element = Element('Li')
```
The nautral abunadnace of Elements is known and the isotopes are created accordingly. Elemental properties can then be queried. In some cases lists of Isotope objects are returned

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

Elements can also be created with enriched abundances. All the natural isotopes within the element must be defined.

```sh
$ example_element = Element('Li',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
```

# Making compounds

Chemical equations are refered to as Compounds by the software. Compounds can be any valid chemical formula such as H2O, CO2 or C8H10N4O2.  

Compounds can be created using the following command when both the compound chemical forumla and the density in grams per cm3 are specified.
```sh
$ Compound('C12H22O11',1.59)
```
The software knows about the cystaline volume of some chemical formula and can create a compound using a small material database and the natural abundances of elements. Compounds that the software knows the cystaline volume or atoms per cm3 for are mainly fusion relevant materials Li4SiO4, Li2SiO3, Li2ZrO3, Li2TiO3, Be, Ba5Pb3, Nd5Pb4, Zr5Pb3, Zr5Pb4, Pb84.2Li15.8. For these compounds they can be create without the density argument.
```sh
$ Compound('Li4SiO4')
```
Compounds can also be enriched much like isotopes can. To enrich an compound one must pass the desired atom abundances for all the isotopes in the element. Here is an example for enriched Li2ZrO3 with Li6 abundance set to 0.9 and Li7 abundance set to 0.1. You can see that Isotope objects are used for this procedure.
```sh
Compound('Li2ZrO3',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
```
Other input options for creating compounds include setting a packing_fraction and theoretical_density which both perform the same operation. The density of the resulting compound is multiplied by the input packing fraction or theoretical density. Both are included to allow pebble beds which are made of pebbles that are not at 100% density.
```sh
$ solid_ceramic = Compound('Be12Ti')
$ pebble_bed_ceramic = Compound('Be12Ti',packing_fraction=0.64)
```
The density of the two compounds can be found with the density_g_per_cm3 property.
```sh
$ solid_ceramic.density_g_per_cm3
>>>2.2801067618505506
$ pebble_bed_ceramic.density_g_per_cm3
>>>1.4592683275843523
```
Other input options for Compunds include pressure_Pa and temperature_K which are used when calculating the density of ideal gases. This function only works for Helium at the moment but could be exspanded in the future.
```sh
$ He_compound = Compound('He', pressure_Pa = 8.0E6, temperature_K = 823.0)
$ He_compound.density_g_per_cm3_idea_gas
>>> 0.004682671945463105
```

Once a compound has been created various properties can be exstracted including material cards suitable for Serpent simulation and density. 
```sh
$ example_compound = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, 0.9), Isotope('Li', 7, 0.1)))
$ example_compound.enriched_isotopes
>>> <__main__.Isotope object at 0x7f859e27dfd0>, <__main__.Isotope object at 0x7f859e28d2d0>
$ example_compound.density_g_per_cm3
>>> 2.4132772544935666
$ example_isotope.description
>>> Li4SiO4__Li6_0.9_Li7_0.1
$ example_isotope.isotopes_mass_fractions
>>> [3.6, 0.4, 0.92223, 0.04685, 0.03092, 4.0]
$ example_isotope.volume_m3
>>> 8.245e-29
$ example_isotope.molar_mass
>>> 116.526000953
$ example_isotope.elements
>>> [<__main__.Element object at 0x7fea0f159350>, <__main__.Element object at 0x7fea0f159290>, <__main__.Element object at 0x7fea0f1590d0>]
$ example_isotopes.serpent_material_card_zaid
>>> mat Li4SiO4__Li6_0.9_Li7_0.1 -2.34682941932
>>>    3006.31c 3.6
>>>    3007.31c 0.4
>>>    14028.31c 0.92223
>>>    14029.31c 0.04685
>>>    14030.31c 0.03092
>>>    8016.31c 4.0
```
One novel feature of the software is that is varies the compound density and atom fractions based on the actual isotopes present within the cryslaine latic. Creating different compunds for use in parameter studies is easy with a for loop. Here the enrichment of Li6 is changed from 0.25 to 0.5, 0.75 then 1.0 and the calculated density of the resulting Li4SiO4 is returned each time. The density decreases slowwly as Li7 atoms are replaced with Li6. The serpent_material_card_zaid also changes accordingly.

```sh
for enrichment in [0.25,0.50,0.75,1.0]:
    example_compound = Compound('Li4SiO4',enriched_isotopes=(Isotope('Li', 6, enrichment), Isotope('Li', 7, 1.0-enrichment)))
    example_compound.density_g_per_cm3
>>> 2.39923943372
>>> 2.37908173587
>>> 2.35892403803
>>> 2.33876634019
```

# Making materials

Materials are a sets of particular isotopes and densities that the software knows about. This can easily be exspanded but current includes Tungsten, Eurofer, Homogenous_Magnet, DT_plasma, SS-316L-IG.

```sh
$ plasma_mat = Material('DT_plasma')
$ plasma_mat.atom_density_per_barn_per_cm
>>> 1e-20
$ plasma_mat.serpent_material_card_zaid
>>> mat DT_plasma 1e-20
>>>     1002.31c 0.5
>>>     1003.31c 0.5
```
The other materials available are considerably more detailed in their isotope description. So only Tungsten and DT_plasma have been shown here.
```sh
$ mat_Tungsten = Material('Tungsten')
$ mat_Tungsten.atom_density_per_barn_per_cm
>>> 19.298
$ mat_Tungsten.serpent_material_card_zaid
>>> mat Tungsten -19.298
>>>     74182.31c 0.016733
>>>     74183.31c 0.0090295
>>>     74184.31c 0.019322
>>>     74186.31c 0.017933
```

# Making homogenised mixtures

Materials and Compounds can be combined to form a Homogenised_mixture. Any number of Materials and Compounds can be combined but they must combine to give a volume fraction of 1.0. Here are some examples ...

```sh
$ mat_steel = Compound('SS-316L-IG')
$ mat_steel.density_g_per_cm3
>>> 7.93
$ mat_water = Compound('H2O',density_g_per_cm3=0.926)
$ mat_water.density_g_per_cm3
>>> 0.926
$ mat_CuCrZr = Compound('CuCrZr',density_g_per_cm3=8.814)
$ mat_CuCrZr.density_g_per_cm3
>>> 8.814
```

The two Compounds and 1 Material can then be mixed with volume fractions the following way
```sh
$ mat_mix = Homogenised_mixture([(mat_water, 0.25), (mat_CuCrZr, 0.25), (mat_steel,0.5)])
$ mat_mix.density_g_per_cm3
>>> 6.4
```

The resulting material card comprises of the combined three material cards with modified atom fractions to account for the volume fraction of each component. The material name is also based on the combination of the three components along with their volume fractions.
```sh
$ mat_mix.serpent_material_card_zaid
>>> mat H2O_vf_0.25_CuCrZr_vf_0.25_SS-316L-IG_vf_0.5_  -6.4
>>>   1001.31c 0.4999425
>>>   1002.31c 5.75e-05
>>>   8016.31c 0.25
>>>   29063.31c 0.172875
>>>   29065.31c 0.077125
>>>   24050.31c 0.0108625
>>>   24052.31c 0.2094725
>>>   24053.31c 0.0237525
>>>   24054.31c 0.0059125
>>>   40090.31c 0.128625
>>>   40091.31c 0.02805
>>>   40092.31c 0.042875
>>>   40094.31c 0.04345
>>>   40096.31c 0.007
>>>   26054.31c 0.001645905
>>>   26056.31c 0.02491445
>>>   26057.31c 0.00056529
>>>   26058.31c 7.39325e-05
>>>   6012.31c 5.96385e-05
>>>   25055.31c 0.000868265
>>>   14028.31c 0.000393248
>>>   14029.31c 1.927965e-05
>>>   14030.31c 1.228565e-05
>>>   15031.31c 1.925585e-05
>>>   16032.03c 7.08335e-06
>>>   16033.03c 5.499e-08
>>>   16034.03c 3.012745e-07
>>>   16036.03c 1.326515e-09
>>>   24050.31c 0.0003734875
>>>   24052.31c 0.0069253
>>>   24053.31c 0.00077046
>>>   24054.31c 0.000188232
>>>   28058.31c 0.003503205
>>>   28060.31c 0.00130445
>>>   28061.31c 5.5774e-05
>>>   28062.31c 0.0001749635
>>>   28064.31c 4.316555e-05
>>>   42092.31c 0.0001039905
>>>   42094.31c 6.344e-05
>>>   42095.31c 0.0001080355
>>>   42096.31c 0.000112014
>>>   42097.31c 6.34715e-05
>>>   42098.31c 0.0001587375
>>>   42100.31c 6.2083e-05
>>>   7014.31c 0.000135939
>>>   7015.31c 4.686305e-07
>>>   5010.31c 4.75157e-07
>>>   5011.31c 1.738695e-06
>>>   29063.31c 7.8647e-05
>>>   29065.31c 3.397545e-05
>>>   27059.31c 2.023495e-05
>>>   41093.31c 2.567445e-06
>>>   22046.31c 4.28233e-06
>>>   22047.31c 3.779715e-06
>>>   22048.31c 3.667145e-05
>>>   22049.31c 2.63624e-06
>>>   22050.31c 2.47368e-06
>>>   73181.31c 1.319185e-06
```

### Todos
 - Write MORE Tests
 - Improve gas Compounds and Materials
 - Add some more Materials to the collection
 - Upload tested source code
 - Combine with engineering materials database
 - Make a GUI
 
### Acknowledgements

Isotope natural abundance and mass data from [Nist](https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses)
