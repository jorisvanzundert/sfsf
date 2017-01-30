FROM kaixhin/theano:latest
LABEL maintainer "Joris J. van Zundert <joris.van.zundert@gmail.com>"

RUN apt-get update
RUN apt-get -y install python3-pip
RUN apt-get -y install libxml2-dev libxslt1-dev python-dev zlib1g-dev
RUN useradd -ms /bin/bash sfsfuser
RUN cd /home/sfsfuser
RUN mkdir sfsf
COPY . /home/sfsfuser/sfsf
WORKDIR /home/sfsfuser/sfsf
RUN pip3 install -r requirements.txt
USER root
RUN chown -R sfsfuser:users /home/sfsfuser/sfsf
USER sfsfuser
WORKDIR /home/sfsfuser
