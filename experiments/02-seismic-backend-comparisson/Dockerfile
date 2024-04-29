FROM seismic

ARG USER_ID
ARG GROUP_ID
ARG USER_NAME=experiments
ARG GROUP_NAME=experiments

ENV HOME="/home/${USER_NAME}"

WORKDIR ${HOME}/02-seismic-backend-comparisson

RUN if getent passwd ${USER_ID} >/dev/null; then \
    deluser $(getent passwd ${USER_ID} | cut -d: -f1); fi && \
    if getent group ${GROUP_ID} >/dev/null; then \
    delgroup $(getent group ${GROUP_ID} | cut -d: -f1); fi && \
    addgroup --system --gid ${GROUP_ID} ${GROUP_NAME} && \
    adduser --system --disabled-password --home ${HOME} --uid ${USER_ID} --ingroup ${GROUP_NAME} ${USER_NAME}
RUN chown -R ${USER_ID}:${GROUP_ID} ${HOME}

USER ${USER_ID}

COPY requirements.txt .
RUN conda run -n experiments pip install -r requirements.txt

COPY experiment/generate.py experiment/
COPY experiment/profile_backend.py experiment/
COPY experiment/summarize.py experiment/
COPY run.sh .

ENTRYPOINT ["./run.sh", "conda run -n experiments python"]