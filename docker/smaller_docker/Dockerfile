# The build-stage image:
FROM --platform=linux/amd64 continuumio/miniconda3 AS build
COPY environment.yml .
USER root

# Activate the base environment
SHELL ["/bin/bash", "-c"]

# Install basic utilities
RUN apt-get update && \
    apt-get install -y --reinstall build-essential && \
    apt-get install -y gcc git

# Install conda environment and unpack it 
RUN conda env create -f environment.yml && \
    conda clean --all --yes && \
    source activate jim && \
    pip install --upgrade "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html && \
    pip install --force-reinstall -v "jax==0.4.21" && \
    conda install -c conda-forge conda-pack && \
    conda-pack -n jim -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar && \
    /venv/bin/conda-unpack

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM --platform=linux/amd64 debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv