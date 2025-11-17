FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && apt-get install -y \
    build-essential curl git libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev && \
    rm -rf /var/lib/apt/lists/*

USER vscode
ENV PYENV_ROOT="/home/vscode/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

RUN curl https://pyenv.run | bash
RUN echo 'eval \"$(pyenv init -)\"' >> /home/vscode/.bashrc
RUN echo 'eval \"$(pyenv virtualenv-init -)\"' >> /home/vscode/.bashrc

RUN bash -lc "pyenv install 3.10.14"
RUN bash -lc "pyenv global 3.10.14"

CMD ["bash"]

