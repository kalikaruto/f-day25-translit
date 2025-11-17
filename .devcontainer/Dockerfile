FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential curl git libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev && \
    rm -rf /var/lib/apt/lists/*

# Install pyenv for the vscode user
USER vscode
ENV PYENV_ROOT="/home/vscode/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

RUN curl https://pyenv.run | bash

RUN echo 'eval "$(pyenv init -)"' >> /home/vscode/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> /home/vscode/.bashrc

# Install Python
RUN bash -lc "pyenv install 3.10.14"
RUN bash -lc "pyenv global 3.10.14"

# Install requirements
COPY requirements.txt /tmp/requirements.txt
RUN bash -lc "pip install --upgrade pip"
RUN bash -lc "pip install -r /tmp/requirements.txt"

CMD ["bash"]

