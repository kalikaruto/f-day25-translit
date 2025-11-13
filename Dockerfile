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
RUN curl https://pyenv.run | bash && \
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> /root/.bashrc && \
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /root/.bashrc && \
  echo 'eval "$(pyenv init --path)"' >> /root/.bashrc && \
  echo 'eval "$(pyenv init -)"' >> /root/.bashrc

# Install Python 3.10 with pyenv
RUN bash -lc "pyenv install 3.10.14 && pyenv global 3.10.14"

# Preinstall your Python deps (optional)
COPY requirements.txt /tmp/requirements.txt
RUN bash -lc "pip install -r /tmp/requirements.txt"

# Set default shell
CMD [ "bash" ]

