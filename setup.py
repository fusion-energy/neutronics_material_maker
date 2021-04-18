import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neutronics_material_maker",
    version="0.3.2",
    summary="Package for making material cards for neutronics codes",
    author="neutronics_material_maker development team",
    author_email="mail@jshimwell.com",
    description="A tool for making neutronics material cards for use in OpenMC, MCNP, Serpent, Shift and Fispact",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ukaea/neutronics_material_maker",
    packages=setuptools.find_packages(),
    zip_safe=True,
    package_dir={"neutronics_material_maker": "neutronics_material_maker"},
    package_data={
        "neutronics_material_maker": [
            "requirements.txt",
            "README.md",
            "LICENSE.txt",
            "data/*.json",
        ]
    },
    tests_require=["pytest-cov", "pytest-runner"],
    install_requires=[
        "coolprop",
        "asteval",
        # 'openmc' when pip install is available
    ],
)
