Neutronics Material Maker
=========================

The aim of this project is to facilitate the creation of materials for use in neutronics codes such as OpenMC, Serpent, MCNP and Fispact.

The hope is that by having this collection of materials it is easier to reuse materials across projects, use a common source with less room for user error.

The package allows for materials to be made from either an internal library of materials or from your own material library.

Material densities can be made to account for temperature, pressure isotopic enrichment.


.. toctree::
   :maxdepth: 1

   
   material
   multimaterial
   example_material
   example_multimaterial
   example_library_usage


Prerequisites
-------------

To use the neutronics-material-maker tool you will need Python 3 and OpenMC installed.

* `Python 3 <https://www.python.org/downloads/>`_
* `OpenMC <https://docs.openmc.org/en/stable/usersguide/install.html>`_



Installation
------------

The quickest way to install the neutronics-material-maker is to use pip. In the terminal type...

::

   pip install neutronics-material-maker

Alternativly you can clone the repository, and install using the setup.py 

::

   git clone https://github.com/ukaea/neutronics_material_maker.git
   cd neutronics_material_maker
   python setup.py install

Features
--------

There are two main user classes `Material() <https://neutronics-material-maker.readthedocs.io/en/latest/material.html>`_ and `MutliMaterial() <https://neutronics-material-maker.readthedocs.io/en/latest/multimaterial.html>`_ which are both fully documented.


Example Scripts
---------------

There are several examples in the relevent example webpages `example Material usage <https://neutronics-material-maker.readthedocs.io/en/latest/example_material.html>`_ and `example MutliMaterial usage <https://neutronics-material-maker.readthedocs.io/en/latest/example_multimaterial.html>`_

Additionally there are more examples in the `OpenMC workshop <https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_11>`_ .
