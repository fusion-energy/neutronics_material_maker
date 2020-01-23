import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="neutronics_material_maker",
    version="0.0.4",
    author="Jonathan Shimwell",
    author_email="jonathan.shimwell@ukaea.uk",
    description="A tool for making neutronics material cards for use in OpenMC",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ukaea/neutronics_material_maker",
    packages=setuptools.find_packages(),
    license='GPL version 3',
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest-cov',
    ],
    install_requires = [
        'thermo',
	#'openmc' when pip install is available
    ]
)
