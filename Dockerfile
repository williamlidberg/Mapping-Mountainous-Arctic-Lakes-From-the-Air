FROM nvcr.io/nvidia/tensorflow:21.12-tf2-py3

RUN apt-get update
# install dependencies for opencv
RUN pip install tifffile
RUN pip install whitebox==2.0.3
# added to install splitraster witout numpy version conclict
RUN pip install geopandas
RUN pip install splitraster

# setup GDAL
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntugis/ppa && apt-get update
RUN apt-get install -y gdal-bin
RUN apt-get install -y libgdal-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip install GDAL

# create mount points for data and source code in container's start directory
RUN mkdir /workspace/data
RUN mkdir /workspace/code

