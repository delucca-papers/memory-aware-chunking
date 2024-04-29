FROM continuumio/miniconda3:23.5.2-0

ARG SEISMIC_HOME="/root/.local/src/seismic"

WORKDIR ${SEISMIC_HOME}

COPY requirements.txt requirements.txt

RUN conda config --set channel_priority flexible && \
    conda install -n base conda-libmamba-solver && \
    conda config --set solver libmamba && \
    conda create -c rapidsai -c conda-forge -c nvidia --name experiments python=3.10 --file requirements.txt -y

ARG DOWSER_HOME="/root/.local/src/dowser"
RUN mkdir -p ${DOWSER_HOME} && \
    cd ${DOWSER_HOME} && \
    git clone https://github.com/delucca-papers/seismic-attributes-memory-profile.git && \
    cd seismic-attributes-memory-profile && \
    # Temporary, until I finish the refactor
    git checkout e9d3801 && \
    mv tools/dowser/* ../ && \
    cd .. && \
    rm -rf seismic-attributes-memory-profile && \
    conda run -n experiments pip3 install . && \
    cd ${SEISMIC_HOME}

RUN conda run -n experiments pip3 install ${DOWSER_HOME}

ARG SSH_KEY
RUN apt-get update && \
    apt-get install -y build-essential && \
    conda run -n experiments pip3 install --upgrade setuptools
RUN mkdir ~/.ssh/ && \
    echo "$SSH_KEY" > ~/.ssh/id_rsa && \
    ssh-keyscan -p 443 ssh.github.com > ~/.ssh/known_hosts && \
    chmod 600 ~/.ssh/id_rsa && \
    conda run -n experiments pip3 install --extra-index-url https://test.pypi.org/simple/ XPySom-dask git+https://github.com/discovery-unicamp/dasf-core.git && \
    conda run -n experiments pip3 install git+ssh://git@ssh.github.com:443/discovery-unicamp/dasf-seismic.git && \
    rm -rf ~/.ssh

COPY . .

RUN conda run -n experiments pip3 install .