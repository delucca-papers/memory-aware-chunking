FROM dowser

COPY requirements.txt requirements.txt

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    sh miniconda.sh -b -p /miniconda && \
    rm miniconda.sh

ENV PATH="/miniconda/bin:${PATH}"

RUN conda config --set channel_priority flexible && \
    conda install -n base conda-libmamba-solver && \
    conda config --set solver libmamba && \
    conda create -c rapidsai -c conda-forge -c nvidia --name experiments --file requirements.txt -y

ARG DOWSER_HOME="/root/.local/src/dowser"
RUN conda run -n experiments pip3 install ${DOWSER_HOME}

ARG SSH_KEY
RUN mkdir ~/.ssh/ && \
    echo "$SSH_KEY" > ~/.ssh/id_rsa && \
    ssh-keyscan -p 443 ssh.github.com > ~/.ssh/known_hosts && \
    chmod 600 ~/.ssh/id_rsa && \
    conda run -n experiments pip3 install --extra-index-url https://test.pypi.org/simple/ XPySom-dask git+https://github.com/discovery-unicamp/dasf-core.git && \
    conda run -n experiments pip3 install git+ssh://git@ssh.github.com:443/discovery-unicamp/dasf-seismic.git && \
    conda run -n experiments pip3 install dask-cuda==23.8.0 && \
    rm -rf ~/.ssh

ARG SEISMIC_HOME="/root/.local/src/seismic"

WORKDIR ${SEISMIC_HOME}

COPY . .

RUN conda run -n experiments pip3 install .