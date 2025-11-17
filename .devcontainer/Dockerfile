# Use a base image close to your current one
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install dependencies for pyenv + Python builds
RUN apt-get update && apt-get install -y \
  build-essential curl git libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev && \
  rm -rf /var/lib/apt/lists/*

# Install pyenv
RUN curl https://pyenv.run | bash

# Proper pyenv init
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# pyenv init MUST be in ENV, not only in .bashrc, for Docker build
RUN echo 'eval "$(pyenv init -)"' >> /root/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.bashrc

# Install Python 3.10 with pyenv
RUN bash -lc "pyenv install 3.10.14"
RUN bash -lc "pyenv global 3.10.14"

# Preinstall your Python deps (optional)
COPY requirements.txt /tmp/requirements.txt
RUN bash -lc "pip install -r /tmp/requirements.txt"

# Set default shell
CMD [ "bash" ]

