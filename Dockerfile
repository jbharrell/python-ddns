FROM ubuntu

MAINTAINER Jason Harrell icubedjbh@gmail.com

WORKDIR /home/ddns
COPY src/* ./

RUN apt-get update && apt-get install -y python3 python-setuptools python-dev gcc libcurl4-openssl-dev libssl-dev && easy_install pip && pip install .

CMD ["ddns", "jason.yaml"]
