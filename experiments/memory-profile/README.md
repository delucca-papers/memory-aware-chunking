# Memory Profile

## Overview

This experiment is designed to evaluate the memory usage patterns of various seismic attributes during their computation.
This is crucial for understanding how different attributes consume resources, allowing for more efficient memory management in seismic data processing workflows.
By monitoring memory usage across distinct stages, this experiment aims to identify optimization opportunities and ensure resource-efficient attribute calculations.

## Prerequisites

- **Docker**:
Ensure Docker is installed on your system.
This experiment runs inside a Docker container to standardize the environment across different systems.

## Setup and Execution

1. **Build the base Docker image**:

All experiments share a base Docker image that contains some common dependencies and setup.
So, the first step is to go on the parent directory (`/experiments`) and run the following command:

```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t discovery/experiments .
```

2. **Build the Docker Container**:
With the base image built, get back to this directory (`/experiments/memory-profile`) and build the Docker container for the experiment.
This process includes installing Python and the necessary packages.

```bash
docker build -t discovery/experiments/memory-profile .
```

2. **Run the Experiment**:
After building the container, run the experiment.
This step will execute the memory-intensive task within the Docker environment and log the memory usage data for each tool.

```bash
docker run --mount type=bind,source="$(pwd)"/output,target=/experiments/memory-profile/output --rm discovery/experiments/memory-profile
```

> [!TIP]
> You can customize the experiment input parameters.
> To do so, simply change the section "Input paramenters" on the `./run.sh` script.

## How It Works

The experiment operates by employing the specified step size (default of 500) along the inline dimension, while maintaining the crossline and time/depth dimensions fixed at 200.
This methodology involves generating a synthetic dataset and storing it on disk, followed by executing the desired attribute calculation using the DASK framework.
The experiment is designed to pause at key events, allowing for the monitoring of memory usage:

- At the start of the experiment;
- When the dataset is fully loaded;
- Upon completion of the attribute calculation.

This approach enables detailed evaluation of both the overall and incremental memory usage, facilitating a comprehensive analysis of the attributes' resource efficiency.

## Analyzing the Results

TODO

## Expected Results and Conclusion

TODO