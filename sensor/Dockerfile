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

ADD requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /usr/src/app
COPY . .
COPY ./entry.sh /usr/src/app/
RUN chmod +x /usr/src/app/entry.sh

CMD ["./entry.sh"]
