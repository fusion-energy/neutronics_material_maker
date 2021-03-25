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

      <iframe width="560" height="315" src="https://www.youtube.com/embed/V-VHLwRar9s" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


.. toctree::
   :maxdepth: 1

   
   material
   multimaterial
   example_material
   example_multimaterial
   example_library_usage


History
-------

The package was originally created by Jonathan Shimwell as a method of
reducing the effort required to the same materials accross different neutronics
codes. The current version can be considered a materials library and translator
between material types. The original version contained methods of mixing
materials and building materials from chemical equations. These aspects of the
code were moved to OpenMC in code contributions (e.g
`1 <https://github.com/openmc-dev/openmc/pull/1530>`_ and
`2 <https://github.com/openmc-dev/openmc/pull/1534>`_ )
which reduced the complexity and maintainance burden for the neutronics
material maker and brought on OpenMC as a major dependancy.


Prerequisites
-------------

To use the neutronics-material-maker tool you will need Python 3 and OpenMC
installed.

* `Python 3 <https://www.python.org/downloads/>`_
* `OpenMC <https://docs.openmc.org/en/stable/usersguide/install.html>`_



Installation
------------

The recommended method is to install from [Conda Forge](https://conda-forge.org)
which also installs all the dependancies including OpenMC.

.. code-block:: bash

   conda install neutronics_material_maker -c conda-forge


Alternativly the code can be easily installed using pip (which doesn't
currently include OpenMC)

.. code-block:: bash

   pip install neutronics_material_maker

You can clone the repository, and install using the setup.py if you would like
the development version.

.. code-block:: bash

   git clone https://github.com/ukaea/neutronics_material_maker.git
   cd neutronics_material_maker
   python setup.py install

Features
--------

There are two main user classes 
`Material() <https://neutronics-material-maker.readthedocs.io/en/latest/material.html>`_ 
and 
`MutliMaterial() <https://neutronics-material-maker.readthedocs.io/en/latest/multimaterial.html>`_ 
which are both fully documented.


Example Scripts
---------------

There are several examples in the relevant example webpages; `example Material usage <https://neutronics-material-maker.readthedocs.io/en/latest/example_material.html>`_ and `example MutliMaterial usage <https://neutronics-material-maker.readthedocs.io/en/latest/example_multimaterial.html>`_ .

Additionally there are more examples in the `OpenMC workshop <https://github.com/ukaea/openmc_workshop/tree/main/tasks/task_02_making_materials>`_ .


Source code
------------

The source code is permissively licensed open-source and available from the
`GitHub repository <https://github.com/ukaea/neutronics_material_maker>`_
