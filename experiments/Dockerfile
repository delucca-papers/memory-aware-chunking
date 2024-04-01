FROM python:3.10.13

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID experimentuser && \
    adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID experimentuser

COPY common/ /experiments/common/