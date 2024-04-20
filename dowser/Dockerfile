FROM python:3.10-alpine

ARG USER_ID
ARG GROUP_ID
ARG USER_NAME=dowser
ARG GROUP_NAME=dowser

ENV HOME="/home/${USER_NAME}"

WORKDIR ${HOME}/.local/src/dowser

RUN apk update && \
    pip install --upgrade pip

RUN apk add gcc python3-dev musl-dev linux-headers

RUN if getent passwd ${USER_ID} >/dev/null; then \
    deluser $(getent passwd ${USER_ID} | cut -d: -f1); fi && \
    if getent group ${GROUP_ID} >/dev/null; then \
    delgroup $(getent group ${GROUP_ID} | cut -d: -f1); fi && \
    addgroup --system --gid ${GROUP_ID} ${GROUP_NAME} && \
    adduser --system --disabled-password --home ${HOME} --uid ${USER_ID} --ingroup ${GROUP_NAME} ${USER_NAME}
RUN chown -R ${USER_ID}:${GROUP_ID} ${HOME}

USER ${USER_ID}

COPY --chown=${USER_NAME}:${GROUP_NAME} . .

RUN pip install --user .

ENV PATH="/home/${USER_NAME}/.local/bin:${PATH}"