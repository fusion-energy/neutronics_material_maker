Interal library usage and extension
===================================

Usage - finding available materials
-----------------------------------

Each of the materials available is stored in an internal dictionary that can be accessed using the AvailableMaterials() command.

::

    import neutronics_material_maker as nmm
    all_materials = nmm.AvailableMaterials()
    print(all_materials.keys())

Usage - importing your own library from a file
----------------------------------------------

Assuming you have a JSON file saved as mat_lib.json containing materials defined in the same format as the `exisiting <https://github.com/ukaea/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/data/>`_ materials. This example file only contains one material but it could contain several materials.


::

    {
        "polythylene": {
            "density": 1.0,
            "density_unit": "g/cm3",
            "elements": {
                "H": 0.2,
                "C": 0.8
            },
        }
    }

You can import this file into the package using AddMaterialFromFile().

::

    import neutronics_material_maker as nmm
    nmm.AddMaterialFromFile('mat_lib.json')
    my_new_material = nmm.Material('polythylene')

Another option is to use AddMaterialFromDir() to import a directory of json files
