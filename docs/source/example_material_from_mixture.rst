Example Material.from_mixture() usage
=====================================

It is possible to mix two or more materials together to create a new mixed
material using the from_mixture method.

Usage - mixing two materials using Material.from_mixture
--------------------------------------------------------

Making two materials and mixing them to create a new material, the density
of the new material will be calculated from the mixture of the two materials.

This example mixes two materials with 40% of mat1 and 60% of mat2 by volume
fraction

.. code-block:: python

   import neutronics_material_maker as nmm

   mat1 = nmm.Material.from_library(name='eurofer')
   mat2 = nmm.Material.from_library(name='tungsten')

   mat3 = nmm.Material.from_mixture(
      name='mixed_eurofer_and_tungsten',
      materials=[mat1, mat2],
      fracs=[0.4, 0.6],
      percent_type='vo'
   )

This new material can then be exported to a file, perhaps as part of
a new material library and retrieve later

.. code-block:: python

   import json

   with open('my_mixed_material.json', 'w') as outfile:
      json.dump(mat3, outfile, indent=4)
