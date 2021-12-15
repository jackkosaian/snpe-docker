# SNPE on Docker Example
This repository contains an example of how to run a basic [Qualcomm SNPE](https://developer.qualcomm.com/sites/default/files/docs/snpe/overview.html)
workflow when using a Docker container.

## Repository structure
* [docker](docker): Dockerfile used for running experiments
* [save_mnist_model.py](save_mnist_model.py): script for generating and saving a simple TensorFlow graph and setting up the command-line arguments needed for using SNPE command-line tools.
* [print_snpe_output.py](print_snpe_output.py): script for printing the output resulting from running SNPE

## Requirements
The only requirement currently known is Docker. This repository was also tested
only with SNPE version 1.54.2.2899.

## Building the Docker container
You must download the SNPE zip file. This will be used as input to the Docker
build process and copied into the container.

To build the Docker container, run:
```bash
cd docker
cp /path/to/snpe-1.54.2.zip snpe-1.54.2.zip
docker build . -t snpe --build-arg SNPE_ZIP=snpe-1.54.2.zip
docker run -it --rm snpe
```

## Running the Docker container
To enter the Docker container, run:
```bash
docker run -it --rm snpe -v /path/on/host/to/snpe-docker:/home/snpe-docker
```

## Running the TF to SNPE example
Once you have entered, the Docker container, run the following commands:
```bash
cd /home/snpe-docker
python save_mnist_model.py outdir
```
This will (1) save a TF model to `outdir/pb`, along with a sample image from
the MNIST dataset to be used as input to the SNPE command-line tools, and (2)
print commands needed to convert the TF model to DLC format and run the DLC
file using the SNPE command-line tools. This final step could be added to an
overarching script to streamline the overall process.

Follow the commands printed at the end of the step above to convert the TF
model to a DLC file and run it using the `snpe-net-run` utility.

To print the output that results from running `snpe-net-run`, run:
```bash
python print_snpe_output.py outdir/out/Result_0/
```
