FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && apt-get install -y \
    build-essential curl git libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------
# pyenv setup
# ----------------------------
USER vscode
ENV PYENV_ROOT="/home/vscode/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

RUN curl https://pyenv.run | bash

# minimal and safe init (Codespaces friendly)
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc \
 && echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"' >> ~/.bashrc \
 && echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

# install single python version and strict pip version
RUN bash -lc "pyenv install 3.10.13" \
 && bash -lc "pyenv global 3.10.13" \
 && bash -lc "pip install --upgrade pip==20.3.4"

CMD ["bash"]

