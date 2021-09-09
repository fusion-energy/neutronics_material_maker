Example Material.from_library() usage
=====================================

Usage - finding available materials
-----------------------------------

Each of the materials available is stored in an internal dictionary that can be
accessed using the AvailableMaterials() command.

.. code-block:: python

    import neutronics_material_maker as nmm
    all_materials = nmm.AvailableMaterials()
    print(all_materials.keys())


Usage - making materials from libraries
---------------------------------------

Here is an example that accesses a material from the internal collection called
eurofer which has about 60 isotopes and a density of 7.78g/cm3.

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat = nmm.Material.from_library(name='eurofer')

Once the object has been initiated the OpenMC or Serpent material card can be accessed.

.. code-block:: python

    my_mat.openmc_material
    my_mat.serpent_material

To access MCNP material it is necessary to also provide an id.

.. code-block:: python

    my_mat = nmm.Material.from_library(name='eurofer', material_id=1)
    my_mat.mcnp_material

To access the Fispact material it is necessary to also provide a volume.

.. code-block:: python

    my_mat = nmm.Material.from_library(name='eurofer', volume_in_cm3=10)
    my_mat.fispact_material

To access the Shift material it is necessary to also provide a temperature and
a material id

.. code-block:: python

    my_mat = nmm.Material.from_library(name='eurofer', temperature=293, material_id=1)
    my_mat.shift_material

Usage - customising materials from libraries
--------------------------------------------

Usage - hot pressurised  Material()
-----------------------------------

For several materials within the collection the temperature and the pressure
impacts the density of the material. The neutronics_material_maker adjusts the
density to take temperature (in C or K) and the pressure into account when
appropriate. Densities are calculated either by a material specific formula
(for example `FLiBe <https://github.com/fusion-energy/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/data/multiplier_and_breeder_materials.json>`_)
or using `CoolProps <https://pypi.org/project/CoolProp/>`_ (for example coolants such as H2O).

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat1 = nmm.Material.from_library('H2O', temperature=300, pressure=15e6)

    my_mat1.openmc_material

Temperature can be provided in degrees C or Kelvin.

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat1 = nmm.Material.from_library('H2O', temperature=573.15, pressure=15e6)

    my_mat1.openmc_material

The temperature is automatically sent to the openmc_material and
serpent_material cards. However if this causes difficulties for you (perhaps
due to not having cross sections at that temperature) this automatic propagate
of temperature information can be disabled by setting the 
temperature_to_neutronics_code to False.


Usage - enriched Material()
---------------------------

For several materials within the collection the density is adjusted when the
material is enriched. For breeder blankets in fusion it is common to enrich the
lithium 6 content.

Lithium ceramics used in fusion breeder blankets often contain enriched
lithium-6 content. This slight change in density is accounted for by the
neutronics_material_maker.

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat2 = nmm.Material.from_library('Li4SiO4', enrichment=60)

    my_mat2.openmc_material


The default enrichment target for 'Li4SiO4' is Li6 but this can be changed if required.

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat2 = nmm.Material.from_library('Li4SiO4', enrichment_target='Li7', enrichment=40)

    my_mat2.openmc_material


Usage - adding extra lines to a material card
---------------------------------------------

If you require additional lines at the end of the MCNP, Serpent, Fispact or
Shift materia card then the additional_end_lines argument can be used. This
will add specific line(s) to the end of a material card. Multiple lines can be
added by creating a list with multiple entries.

In this example and additional line can be added to allow the S(α,β) treatment
of water to be correctly modeled in MCNP. But this could also be used to add
comments to the material card or other text at the end of the material card
string.

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat2 = nmm.Material.from_library(
        name='H2O',
        material_id=24,
        temperature=573.15,
        pressure=15e6,
        additional_end_lines={'mcnp': ['      mt24 lwtr.01']}
    )

    print(my_mat2.mcnp_material)

The above code will return a MCNP material card string with the additional line
'      mt24 lwtr.01' at the end. Notice that spaces should also be set by the
user.

.. code-block:: bash

    c     H2O density 7.25553605e-01 g/cm3
    M24   001001  6.66562840e-01
            001002  1.03826667e-04
            008016  3.32540200e-01
            008017  1.26333333e-04
            008018  6.66800000e-04
            mt24 lwtr.01

It is also possible to specify this additional line in a JSON file and
then read in the file and export the material. The additional end lines can
also support different outputs for different codes and multiple lines being
appended to the material card as demonstrated in this video on the feature.

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/YLcMkQGOeJE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Usage - importing your own library from a file
----------------------------------------------

A correctly formated JSON file that contains materials defined in the same
format as the `exisiting materials <https://github.com/fusion-energy/neutronics_material_maker/tree/main/neutronics_material_maker/data>`_ can be added to the material library.

Assuming you have a JSON file saved as mat_lib.json with the following contents
then this can be added to the material library in the the following manner. 

::

    {
        "my_secret_material": {
            "density": 1.0,
            "percent_type":"ao",
            "density_unit": "g/cm3",
            "elements": {
                "H": 0.2,
                "C": 0.8
            },
        }
    }

This example file only contains one material but it could contain a list of
several materials.

You can import this file into the package using AddMaterialFromFile().

.. code-block:: python

    import neutronics_material_maker as nmm
    nmm.AddMaterialFromFile('mat_lib.json')
    my_new_material = nmm.Material.from_library(name='my_secret_material')

Another option is to use AddMaterialFromDir() to import a directory of JSON files.

Usage - exporting a material to a JSON file
-------------------------------------------

Materials can also be exported to a JSON file as demonstrated below. This JSON
file can then be read back in if required using the AddMaterialFromDir or
AddMaterialFromFile utility functions.

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat1 = nmm.Material.from_library(name='eurofer', material_id=1)
    my_mat2 = nmm.Material.from_library(name='Li4SiO4', material_id=1)

    nmm.SaveMaterialsToFile(
        filename='my_materials.json',
        materials=[my_mat1, my_mat2],
        format='json',
    )

The format can be changed to 'mcnp', 'serpent', 'shift' or 'fispact' to output
a list of nmm.Materials in those formats.
