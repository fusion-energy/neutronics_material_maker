# build with the following command
# sudo docker build -t neutronics_material_maker .

FROM continuumio/miniconda3:4.9.2


# install openmc from conda
RUN conda install -c conda-forge openmc

RUN apt-get update
RUN apt-get install -y git

# clone the openmc nuclear data repository
RUN git clone https://github.com/openmc-dev/data.git

# install endf nuclear data
# run script that converts ACE data to hdf5 data
RUN python data/convert_nndc71.py --cleanup

ENV OPENMC_CROSS_SECTIONS=/nndc-b7.1-hdf5/cross_sections.xml

RUN pip install-neutronics-material-maker
