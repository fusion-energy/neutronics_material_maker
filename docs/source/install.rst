
Installation
============


Prerequisites
-------------

To use the neutronics-material-maker package you will need Python 3 installed
using Miniconda or Anaconda


* `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_
* `Anaconda <https://www.anaconda.com/>`_

Once you have Anaconda or Miniconda installed then proceed with the OS specific
steps.

Install (conda)
---------------

This is the recommended method.

Create a new environment (Python 3.6, 3.7 or 3.8 are supported).

.. code-block:: bash

   conda create --name new_env python=3.8


Then activate the new environment.

.. code-block:: bash

   conda activate new_env


Then install the package.

.. code-block:: bash

   conda install -c conda-forge neutronics_material_maker

Now you should be ready to import neutronics-material-maker from your new python
environment.


Install (conda + pip)
---------------------

Create a new environment (Python 3.6, 3.7, 3.8, 3.9 are supported).

.. code-block:: bash

   conda create --name new_env python=3.8


Then activate the new environment.

.. code-block:: bash

   conda activate new_env


Then install the OpenMC.

.. code-block:: bash

   conda install -c conda-forge openmc

Then pip install the package.

.. code-block:: bash

   pip install neutronics-material-maker

Now you should be ready to import neutronics-material-maker from your new python
environment.

To include the optional capability of calculating the density of coolants
additional packages are needed (CoolProp). A slightly modified pip install
is required in this case.

.. code-block:: bash

   pip install "neutronics_material_maker[density]"
