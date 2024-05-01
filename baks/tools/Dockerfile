FROM jcfaracco/dasf_seismic:cpu

ARG DOWSER_HOME="/root/.local/src/dowser"
RUN mkdir -p ${DOWSER_HOME}
COPY dowser ${DOWSER_HOME}
RUN pip install ${DOWSER_HOME}

ARG SEISMIC_HOME="/root/.local/src/seismic"
COPY seismic ${SEISMIC_HOME}
RUN pip install ${SEISMIC_HOME}