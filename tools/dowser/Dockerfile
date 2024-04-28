FROM python:3.10

ARG DOWSER_HOME="/root/.local/src/dowser"

WORKDIR ${DOWSER_HOME}

RUN apt-get update && \
    pip install --upgrade pip

COPY . .

RUN pip install .