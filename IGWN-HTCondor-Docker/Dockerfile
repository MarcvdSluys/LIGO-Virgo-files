FROM --platform=linux/amd64 continuumio/miniconda3
COPY environment.yml /tmp/environment.yml
USER root

# Activate the base environment
SHELL ["/bin/bash", "-c"]

# Install basic utilities
RUN apt-get update && \
    apt-get install -y --reinstall build-essential && \
    apt-get install -y gcc git

# Create a conda environment called jim based on environment.yml
RUN conda env create -f /tmp/environment.yml && \
    conda clean --all --yes && \
    source activate jim && \
    pip install --upgrade "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

# # Remove unnecessary packages to reduce image size
# RUN apt-get purge -y build-essential gcc git && \
#     apt-get autoremove -y && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*