FROM ubuntu:18.04
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y git sudo
COPY ./ /var/app/chainhammer
WORKDIR /var/app/chainhammer
