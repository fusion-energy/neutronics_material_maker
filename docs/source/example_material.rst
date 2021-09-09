Example Material() usage
========================

While the internal data bases contain lots of standard materials it is often
necessary to build a custom material. These examples show users how to build
materials from user defined isotopes and elements.

Usage - make a your own materials
---------------------------------

Example making materials from elements

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat = nmm.Material(
        name="li_with_si",
        density=3.0,
        density_unit="g/cm3",
        percent_type="ao",
        elements={
                "Li": 4,
                "Si": 2
                }
        )


Example making materials from isotopes

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat = nmm.Material(
        name="enriched_li",
        density= 3.0,
        density_unit="g/cm3",
        percent_type="ao",
        isotopes={
            "Li6": 0.9,
            "Li7": 0.1
        }
    )

Example making materials from isotopes defined by zaid

.. code-block:: python

    import neutronics_material_maker as nmm

    my_mat = nmm.Material(
        name="enriched_li",
        density=3.0,
        density_unit="g/cm3",
        percent_type="ao",
        isotopes={
            "3006": 0.9,
            "3007": 0.1
        }
    )

It is also possible to make your own materials directly from a dictionary by
making use of the python syntax to expand a dictionary **

.. code-block:: python

    import neutronics_material_maker as nmm
    
    my_dict = {
        "name": "li_with_si",
        "elements": {
                        "Li": 4,
                        "Si": 2
                    },
        "density": 3.1,
        "density_unit": "g/cm3",
        "percent_type": "ao",
    }

    my_mat = nmm.Material(**my_dict)
