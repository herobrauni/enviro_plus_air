FROM python:latest

WORKDIR /usr/src/app

ADD raspberrypi.list /etc/apt/sources.list.d/raspberrypi.list
RUN wget -O - http://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add -

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    python3 python3-numpy \
    python python-numpy \
    python-pip python3-pip python-wheel \
    libraspberrypi-bin 

RUN pip install --upgrade pip setuptools

#RUN curl -sSL https://get.pimoroni.com/enviroplus | bash

ADD requirements.txt .

# RUN pip install numpy

RUN pip3 install -r requirements.txt

CMD [ "/home/pirate/python/all-in-one-no-pm.py" ]

