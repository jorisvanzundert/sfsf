FROM ubuntu:latest

LABEL maintainer "Joris J. van Zundert <joris.van.zundert@gmail.com>"

RUN grep -v '^#' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install python3-pip
RUN apt-get -y install libxml2-dev libxslt1-dev python-dev zlib1g-dev
# RUN apt-get -y install libopenblas-dev python-nose g++  git
RUN useradd -ms /bin/bash sfsfuser
RUN cd /home/sfsfuser
RUN mkdir sfsf
RUN mkdir -p /home/sfsfuser/.keras
RUN echo '{"image_dim_ordering":"tf","epsilon": 1e-07,"floatx": "float32","backend": "theano"}' | python3 -m json.tool > /home/sfsfuser/.keras/keras.json
COPY . /home/sfsfuser/sfsf
WORKDIR /home/sfsfuser/sfsf
# Rather than using apt-get install python-numpy python-scipy etc... use
# requirements.txt as it downloads more current versions dan system
# wide package installers
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data punkt
USER root
RUN export PYTHONIOENCODING=utf-8
RUN chown -R sfsfuser:users /home/sfsfuser/sfsf
USER sfsfuser
WORKDIR /home/sfsfuser
