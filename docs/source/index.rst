Neutronics Material Maker
=========================

The neutronics-material-maker python package allows rapid production of neutronics materials from a library

.. toctree::
   :maxdepth: 1

   
   material
   multimaterial
   example_material
   example_multimaterial


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

Usage - Materials
-----------------

Making a material from the inbuilt material database

::

   import neutronics-material-maker as nmm

   my_mat = nmm.Material('eurofer')

Once the object has been initiated the material card can be accessed

::

   my_mat_shape.openmc_material


Usage - MutliMaterial
---------------------

Making two materials and mixing them to create a MultiMaterial

::

   import neutronics-material-maker as nmm

   my_mat1 = nmm.Material('eurofer')
   my_mat2 = nmm.Material('tungsten')

   my_mat3 = MultiMaterial(material_name='mixed_mat',
                           materials=[my_mat1, my_mat2],
                           fracs=[0.4, 0.6],
                           percent_type='vo')



Example Scripts
---------------

There are several example scripts in the `examples folder <https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_11>`_ .
