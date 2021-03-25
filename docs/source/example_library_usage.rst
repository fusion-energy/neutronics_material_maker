Interal library searching, extension and exporting
==================================================

Usage - finding available materials
-----------------------------------

Each of the materials available is stored in an internal dictionary that can be
accessed using the AvailableMaterials() command.

.. code-block:: python

    import neutronics_material_maker as nmm
    all_materials = nmm.AvailableMaterials()
    print(all_materials.keys())

Usage - importing your own library from a file
----------------------------------------------

A correctly formated JSON file that contains materials defined in the same
format as the `exisiting materials <https://github.com/ukaea/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/data/>`_ can be added to the material library.

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
    my_new_material = nmm.Material('polythylene')

Another option is to use AddMaterialFromDir() to import a directory of JSON files.

Usage - exporting a material to a JSON file
-------------------------------------------

Materials can also be exported to a JSON file as demonstrated below

.. code-block:: python

    import json

    import neutronics_material_maker as nmm

    my_mat1 = nmm.Material('eurofer')
    my_mat2 = nmm.Material('Li4SiO4')

    with open('my_materials.json', 'w') as outfile:
        json.dump([my_mat1, my_mat2], outfile, indent=4)

