Example MultiMaterial() usage
=============================

Usage - mixing two materials to make a MultiMaterial
----------------------------------------------------

Making two materials and mixing them to create a MultiMaterial, the density
of the new material will be calculated from the mixture of the two materials.

This example mixes two materials with 40% of mat1 and 60% of mat2 by volume
fraction

.. code-block:: python

   import neutronics_material_maker as nmm

   mat1 = nmm.Material('eurofer')
   mat2 = nmm.Material('tungsten')

   mat3 = nmm.MultiMaterial(
      material_tag='mixed_mat',
      materials=[mat1, mat2],
      fracs=[0.4, 0.6],
      percent_type='vo'
   )
