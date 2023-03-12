FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install build-essential

# add python and libraries
RUN apt-get -y install python3.9 && \
	apt-get -y install python3-pip && \
	pip3 install --upgrade setuptools pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# add git, vim and curl
RUN apt-get -y install git

# Set the working directory in the container
WORKDIR /app

COPY flask/requirements.txt  requirements.txt

# Install any dependencies
RUN pip3 install -r requirements.txt

# Copy the app to the working directory
COPY flask .

ARG INATURALIST_API
ENV INATURALIST_API=$INATURALIST_API

ARG INATURALIST_WEBAPP
ENV INATURALIST_WEBAPP=$INATURALIST_WEBAPP

ARG BUGGY_BACKUP_PATH
ENV BUGGY_BACKUP_PATH=$BUGGY_BACKUP_PATH

# Specify the command to run on container start
CMD [ "python3", "./app.py" ]