FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code

COPY requirements requirements
COPY local.json.example /etc/local.json.example
COPY logging.conf /etc/logging.conf


COPY requirements/base.txt requirements/base.txt
COPY requirements/tests.txt requirements/tests.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/base.txt
RUN pip3 install -r requirements/tests.txt
