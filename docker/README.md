A short explanation on how to run Python scripts with your own docker image in HTCondor jobs.

In particular, we are going to create a Docker image with a conda environment that contains the packages we need to run our Python scripts. Then, we will run the Docker image in HTCondor jobs.

# Get the packages

Assuming you have a conda environment with the packages you need to run your Python scripts, you can export the environment to a file with the following command:

```bash
conda env export > environment.yml
```

Inspect the `environment.yml` file and make sure that it contains all the packages you need. We are going to use the `environment.yml` file to create a conda environment when building the Docker image.

If you want to install packages from a Github repository, check the example in the `environment.yml` file to see how to do it. Notice how you are able to specify a particular branch when installing the package.

# Build the Docker image

First, you need to build the Docker image. To do so, you need to have Docker installed on your machine. Then, you can run the following command:

```bash
docker build -t <image_name> .
```

where `<image_name>` is the name you want to give to your image. This command will build the image using the `Dockerfile` in the current directory.

## Building a smaller Docker image

I had some issues with the size of the Docker image, since it was too big. I was able to reduce the size of the image by using a slightly different and more complicated Dockerfile, which you can find in the `smaller_docker` directory. The information regarding this Dockerfile can be found [here](https://pythonspeed.com/articles/conda-docker-image-size/).

In the provided example Dockerfile, you can ignore the following lines, since they were specifically for my use case. The remainder of the Dockerfile should be kept identical.
```bash
pip install --upgrade "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html && \
pip install --force-reinstall -v "jax==0.4.21" && \
```

With this dockerfile, note that conda is no longer present and the environment is copied under the name `venv` (although you can change that if desired). When running the docker container, you can access the environment by running
```bash
source /venv/bin/activate
```
After that, you can run your python scripts as usual. Make sure to test this first locally before submitting to Docker hub.

# Run the Docker image

Once the image is built, you can run it with the following command:

```bash
docker run -it <image_name>
```

This will run the image in interactive mode (`-it`), which means that you will be able to interact with the container. If you want to open a shell in the container, you can run the following command:

```bash
docker run -it <image_name> /bin/bash
```
There, you can test e.g. whether you are able to load the conda environment and test if you can import one of your installed packages.

# Push the Docker image to Docker Hub

If you want to use the Docker image in HTCondor jobs, you need to push it to Docker Hub. To do so, you need to create a Docker Hub account and then run the following commands:

```bash
docker login
docker tag <image_name> <docker_hub_username>/<image_name>
docker push <docker_hub_username>/<image_name>
```
where `<image_name>` is the name you gave to your image and `<docker_hub_username>` is your Docker Hub username. Additionally, you can give a tag to your image by appending `:<tag>` to the image name. For example, you can tag your image as `latest` by running `docker tag <image_name> <docker_hub_username>/<image_name>:latest`. It is recommended to use tags and to avoid using simply `latest` so to make sure you do not encounter unexpected issues in HTCondor.

To publish to the hub, the easiest way is the
following:
1. In Docker Desktop, go to the Images tab
2. In the Actions column for your image, select the Show image actions icon. (Note: use
drop down menu next to “Run” if you don’t see this)
3. Select Push to Hub.

To push a new tag, run the following command:

```bash
docker push <docker_hub_username>/<image_name>:<tag>
```

# Run the Docker image in HTCondor jobs

See an example submit file in `condor.sub`.

# Docker debugging

Some information regarding annoying docker problems.

- If you encounter the error "At least one invalid signature was encountered" when building a new image, try to run the following command:
```bash
docker builder prune
```
- I encountered errors when trying to run the Docker image in HTCondor jobs. The error was related to the fact that the Docker image was built on a different platform architecture than the one used by HTCondor. To solve this, I added the following flag to the Dockerfile when building the image. It seems that HTCondor only runs with the `linux/amd64` platform architecture and throws a Shadow Exception otherwise (note: this means your jobs will alternate between idle and running, so pay attention to that if using Docker with HTCondor).
```bash
RUN --platform=linux/amd64 ...
```
with the dots being the base image used in building the image. 
- The Docker builder caches a lot of stuff. Therefore, if you e.g. add the platform architecture flag, it might not trigger a rebuild automatically. To force a rebuild, you can run the following command:
```bash
docker build --no-cache -t <image_name> .
```
- If you receive an error such as "Cannot write: No space left on device", run 
```bash
docker system prune -a
```
to remove all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes. This will free up space on your machine.

