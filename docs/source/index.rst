Neutronics Material Maker
=========================

The aim of this project is to facilitate the creation of materials for use in
neutronics codes such as OpenMC, Serpent, MCNP, Shift and Fispact.

The hope is that by having this collection of materials it is easier to reuse
materials across projects and use a common source with less room for user
error.

The package allows for materials to be made from either an internal library of
materials or from your own material library.

Material densities can be made to account for temperature, pressure and
isotopic enrichment.

.. raw:: html

      <iframe width="560" height="315" src="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


.. toctree::
   :maxdepth: 1

   
   install
   material
   example_material
   example_material_from_library
   example_material_from_mixture


History
-------

The package was originally created by Jonathan Shimwell as a method of
reducing the effort required to the same materials across different neutronics
codes. The current version can be considered a materials library and translator
between material types. The original version contained methods of mixing
materials and building materials from chemical equations. These aspects of the
code were moved to OpenMC in code contributions (e.g
`1 <https://github.com/openmc-dev/openmc/pull/1530>`_ and
`2 <https://github.com/openmc-dev/openmc/pull/1534>`_ )
which reduced the complexity and maintenance burden for the neutronics
material maker and brought on OpenMC as a major dependency.

Features
--------

There is just one user class called
`Material() <https://neutronics-material-maker.readthedocs.io/en/latest/material.html>`_ 


Example Scripts
---------------

There are several examples in the relevant example webpages; `example Material usage <https://neutronics-material-maker.readthedocs.io/en/latest/example_material.html>`_ .

Additionally there are more examples in the `Neutronics workshop <https://github.com/fusion-energy/neutronics-workshop/tree/main/tasks/task_02_making_materials>`_ .


Source code
------------

The source code is permissively licensed open-source and available from the
`GitHub repository <https://github.com/fusion-energy/neutronics_material_maker>`_
