Neutronics Material Maker
=========================

The neutronics-material-maker python package allows rapid production of neutronics materials from a library

Features have been added to address particular needs and the software is by no means a finished product. Contributions are welcome. CadQuery functions provide the majority the features, and incorporating additional capabilities is straight forward for developers with Python knowledge.

.. toctree::
   :maxdepth: 1

   
   material
   multimaterial
   example_material
   example_multimaterial


Prerequisites
-------------

To use the neutronics-material-maker tool you will need Python 3 installed.

* `Python 3 <https://www.python.org/downloads/>`_



Installation
------------

The quickest way to install the neutronics-material-maker is to use pip. In the terminal type...

::

   pip install neutronics-material-maker

Alternativly you can download the repository using the `download link <https://github.com/ukaea/neutronics_material_maker/archive/openmc_version.zip>`_ 
clone the repository using `git clone https://github.com/ukaea/neutronics_material_maker.git`.

::

Navigate to the neutronics_material_maker repository and within the terminal install the neutronics_material_maker package and the dependencies using pip3.

::

   pip install .

Alternatively you can install the neutronics_material_maker with following command.

::

   python setup.py install

Features
--------

Usage - Materials
-----------------

There are a collection of Python scripts in the example folder that demonstrate simple shape construction and visualisation. However here is a quick example of a RotateStraightShape.

After importing the class the user then sets the points. By default, points should be a list of (x,z) points. In this case the points are connected with straight lines.

::

   import neutronics-material-maker as nmm

   my_mat = nmm.Material('eurofer')

Once the object has been initiated the material card can be accessed

::

   my_mat_shape.openmc_material


Usage - MutliMaterial
---------------------

Parametric components are wrapped versions of the eight basic shapes where parameters drive the construction of the shape. There are numerous parametric components for a varity of different reactor components such as center columns, blankets, poloidal field coils. This example shows the construction of a plasma. Users could also construct a plasma by using a RotateSplineShape() combined with coordinates for the points. However a parametric component called Plasma can construct a plasma from more convenient parameters. Parametric components also inherit from the Shape object so they have access to the same methods like export_stp() and export_stl().

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

There are several example scripts in the `examples folder <https://github.com/ukaea/openmc_workshop/tree/master/tasks/task_11>`_ . A good one to start with is `make_CAD_from_points <https://github.com/ukaea/paramak/blob/develop/examples/make_CAD_from_points.py>`_ which makes simple examples of the different types of shapes (extrude, rotate) with different connection methods (splines, straight lines and circles).
