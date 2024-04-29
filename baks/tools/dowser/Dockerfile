FROM python:3.10-alpine

ARG DOWSER_HOME="/root/.local/src/dowser"

WORKDIR ${DOWSER_HOME}

RUN apk update && \
    pip install --upgrade pip

RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers

COPY . .

RUN pip install .