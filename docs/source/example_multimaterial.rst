Example MultiMaterial() usage
=============================

Usage - mixing two materials to make a MultiMaterial
----------------------------------------------------

Making two materials and mixing them to create a MultiMaterial

::

   import neutronics-material-maker as nmm

   my_mat1 = nmm.Material('eurofer')
   my_mat2 = nmm.Material('tungsten')

   my_mat3 = nmm.MultiMaterial(
      material_tag='mixed_mat',
      materials=[my_mat1, my_mat2],
      fracs=[0.4, 0.6],
      percent_type='vo'
   )
