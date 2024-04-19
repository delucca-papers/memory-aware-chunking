FROM continuumio/miniconda3:23.5.2-0-alpine

ARG USER_ID
ARG GROUP_ID
ARG SSH_KEY
ARG USER_NAME=experimentuser
ARG GROUP_NAME=experimentuser
ARG DIRNAME=experiments

ENV HOME="/home/${USER_NAME}"


RUN apk update && \
    apk add git g++ make openssh-client && \
    pip install --upgrade pip

COPY requirements.txt ${DIRNAME}/requirements.txt

RUN conda config --set channel_priority flexible && \
    conda install -n base conda-libmamba-solver && \
    conda config --set solver libmamba && \
    conda create -c rapidsai -c conda-forge -c nvidia --name experiments --file ${DIRNAME}/requirements.txt -y

RUN if getent passwd ${USER_ID} >/dev/null; then \
    deluser $(getent passwd ${USER_ID} | cut -d: -f1); fi && \
    if getent group ${GROUP_ID} >/dev/null; then \
    delgroup $(getent group ${GROUP_ID} | cut -d: -f1); fi && \
    addgroup --system --gid ${GROUP_ID} ${GROUP_NAME} && \
    adduser --system --disabled-password --home ${HOME} --uid ${USER_ID} --ingroup ${GROUP_NAME} ${USER_NAME}
RUN chown -R ${USER_ID}:${GROUP_ID} ${HOME}
USER ${USER_ID}
WORKDIR ${DIRNAME}

RUN mkdir ${HOME}/.ssh/ && \
    echo "${SSH_KEY}" > ${HOME}/.ssh/id_rsa && \
    chmod 600 ${HOME}/.ssh/id_rsa

RUN conda run -n experiments pip3 install --extra-index-url https://test.pypi.org/simple/ XPySom-dask git+https://github.com/discovery-unicamp/dasf-core.git && \
    conda run -n experiments pip3 install git+ssh://git@ssh.github.com:443/discovery-unicamp/dasf-seismic.git && \
    conda run -n experiments pip3 install dask-cuda==23.8.0

RUN rm -rf ${HOME}/.ssh

COPY common/ /${DIRNAME}/common/

ENV PYTHONPATH "${PYTHONPATH}:${DIRNAME}"