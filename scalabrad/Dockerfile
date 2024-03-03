#FROM python:3.11-slim-bookworm
#ADD ./app /tmp/app
#RUN apt update -y && apt upgrade -y && apt install -y git
#RUN python -m pip install -U pip pylabrad
#CMD ["bash"]

FROM openjdk
WORKDIR /srv
RUN curl -L -O https://github.com/labrad/scalabrad/releases/download/v0.8.3/scalabrad-0.8.3.tar.gz && tar zxf scalabrad-0.8.3.tar.gz
#CMD ["bash","scalabrad-0.8.3/bin/labrad", "--help"]
CMD ["bash", "scalabrad-0.8.3/bin/labrad", "--tls-required=false", "--tls-hosts=scalabrad" ]
