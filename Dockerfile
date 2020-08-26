# build with the following command
# sudo docker build -t neutronics_material_maker .

FROM ubuntu:18.04

# Updating Ubuntu packages
RUN apt-get update && yes|apt-get upgrade

# Adding wget and bzip2
RUN apt-get install -y wget bzip2

# Anaconda installing
RUN wget https://repo.continuum.io/archive/Anaconda3-2020.02-Linux-x86_64.sh

RUN bash Anaconda3-2020.02-Linux-x86_64.sh -b

RUN rm Anaconda3-2020.02-Linux-x86_64.sh

# Set path to conda
ENV PATH /root/anaconda3/bin:$PATH

# install openmc from conda involves less sets compared to compiling it from source
RUN conda install -c conda-forge openmc


# install endf nuclear data

# clone the openmc nuclear data repository
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/openmc-dev/data.git

# run script that converts ACE data to hdf5 data
RUN python data/convert_nndc71.py --cleanup

ENV OPENMC_CROSS_SECTIONS=/nndc-b7.1-hdf5/cross_sections.xml

RUN pip install-neutronics-material-maker
