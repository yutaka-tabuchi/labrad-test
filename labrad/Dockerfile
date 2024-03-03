#FROM python:3.11-slim-bookworm
FROM python:3.10-slim-bookworm
RUN apt update -y && apt upgrade -y && apt install -y git 
RUN apt install -y curl 
RUN apt install -y iputils-ping net-tools python3 python3-pip
RUN python -m pip install -U pip pylabrad ipython
WORKDIR /srv
ENTRYPOINT ["/bin/sh", "-c", "while :; do sleep 10; done"]
