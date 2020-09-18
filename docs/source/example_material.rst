Example Material() usage
========================

Usage - basic Material()
------------------------

Here is an example that accesses a material from the internal collection called eurofer which has about 60 isotopes and a density of 7.78g/cm3.

::

   import neutronics-material-maker as nmm

   my_mat = nmm.Material('eurofer')

Once the object has been initiated the OpenMC or Serpent material card can be accessed.

::

   my_mat_shape.openmc_material
   my_mat_shape.serpent_material

To access MCNP material it is necessary to also provide an id.

::

   my_mat = nmm.Material('eurofer', id=1)
   my_mat_shape.mcnp_material

To access the Fispact material it is necessary to also provide a volume.

::

   my_mat = nmm.Material('eurofer', volume_in_cm3=10)
   my_mat_shape.fispact_material




Usage - hot pressurised  Material()
-----------------------------------

For several materials within the collection the temperature and the pressure impacts the density of the material. The neutronics_material_maker adjusts the density to take temperature (in C or K) and the pressure into account when appropriate. Densities are calculated either by a material specific formula (for example `FLiBe <https://github.com/ukaea/neutronics_material_maker/blob/openmc_version/neutronics_material_maker/data/multiplier_and_breeder_materials.json>`_) or using `CoolProps <https://pypi.org/project/CoolProp/>`_ (for example coolants such as H2O).

::

    import neutronics_material_maker as nmm

    my_mat1 = nmm.Material('H2O', temperature_in_C=300, pressure_in_Pa=15e6)

    my_mat1.openmc_material

Temperature can be provided in degrees C or Kelvin.

::

    import neutronics_material_maker as nmm

    my_mat1 = nmm.Material('H2O', temperature_in_K=573.15, pressure_in_Pa=15e6)

    my_mat1.openmc_material



Usage - enriched Material()
---------------------------

For several materials within the collection the density is adjusted when the material is enriched. For breeder blankets in fusion it is common to enrich the lithium 6 content.

Lithium ceramics used in fusion breeder blankets often contain enriched lithium-6 content. This slight change in density is accounted for by the neutronics_material_maker.

::

    import neutronics_material_maker as nmm

    my_mat2 = nmm.Material('Li4SiO4', enrichment=60)

    my_mat2.openmc_material

The default enrichment target for 'Li4SiO4' is Li6 but this can be changed if required.

::

    import neutronics_material_maker as nmm

    my_mat2 = nmm.Material('Li4SiO4', enrichment_target='Li7', enrichment=40)

    my_mat2.openmc_material



Usage - make a your own materials
---------------------------------

Example making materials from elements

::
    import neutronics_material_maker as nmm

    my_mat = nmm.Material(material_name="li_with_si",
                          density= 3.0,
                          density_unit= "g/cm3",
                          percent_type= "ao",
                          elements={
                                "Li":4,
                                "Si":2
                            }
    )

Example making materials from isotopes

::
    import neutronics_material_maker as nmm

    my_mat = nmm.Material(material_name="enriched_li",
                          density= 3.0,
                          density_unit= "g/cm3",
                          percent_type= "ao",
                          isotopes={
                                "Li6":0.9,
                                "Li7":0.1
                            }
    )

Example making materials from isotopes defined by zaid

::
    import neutronics_material_maker as nmm

    my_mat = nmm.Material(material_name="enriched_li",
                          density= 3.0,
                          density_unit= "g/cm3",
                          percent_type= "ao",
                          isotopes={
                                "3006":0.9,
                                "3007":0.1
                            }
    )

It is also possible to make your own materials directly from a dictionary by making use of the python syntax **

::
    import neutronics_material_maker as nmm
    
    my_dict = { "material_name": "li_with_si",
                "elements": {
                                "Li":4,
                                "Si":2
                            },
                "density": 3.0,
                "density_unit": "g/cm3",
                "percent_type": "ao",
                }

    my_mat = nmm.Material(**my_dict)
