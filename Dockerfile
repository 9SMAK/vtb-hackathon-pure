FROM python:3.9-buster

RUN apt-get update

WORKDIR /server

COPY ./requirements.txt ./requirements.txt

RUN bash -c 'echo -e 1'

RUN pip3 install --no-cache-dir --disable-pip-version-check -r ./requirements.txt

RUN bash -c 'echo -e 2'

COPY ./src ./src

RUN bash -c 'echo -e 3'