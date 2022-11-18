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

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

COPY flask/requirements.txt  requirements.txt

# Install any dependencies
RUN pip3 install -r requirements.txt

# Copy the app to the working directory
COPY flask .

# Specify the command to run on container start
CMD [ "/bin/bash", "./run.sh" ]