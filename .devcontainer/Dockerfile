# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/devcontainers/python:3

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode
RUN apt update \
    && apt install -y --no-install-recommends curl wget git sudo build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev 

USER ${USER}
ARG HOME="/home/${USER}"
WORKDIR ${HOME}

ARG PYTHON_VERSION=3.11
ENV PYENV_ROOT=${HOME}/.pyenv
ARG PYENV_PATH="${PYENV_ROOT}/bin:${PYENV_ROOT}/shims"
ENV PATH="${PYENV_PATH}:$PATH"
RUN set -x \
    && curl http://pyenv.run | bash \
    && echo 'eval "$(pyenv init -)"' >>${HOME}/.bashrc \
    && pyenv install -v ${PYTHON_VERSION} \
    && pyenv global ${PYTHON_VERSION}

# Install Poetry
ENV POETRY_HOME=${HOME}/.poetry
ARG POETRY_PATH="${POETRY_HOME}/bin"
ENV PATH="${POETRY_PATH}:$PATH"
RUN curl -sSL https://install.python-poetry.org | python -

# Install pdm
ARG PDM_PATH="${HOME}/.local/bin"
ENV PATH="${PDM_PATH}:$PATH"
RUN curl -sSL https://pdm.fming.dev/install-pdm.py | python - 

RUN pip install jupyterlab

#RUN set -x && pipx install pyscaffold && \
#pipx install cookiecutter && \ 
#pipx inject pyscaffold pyscaffoldext-cookiecutter