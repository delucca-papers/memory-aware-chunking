# Backend Comparisson Experiment

## Overview

TODO

## Prerequisites

- **Docker**:
Ensure Docker is installed on your system.
This experiment runs inside a Docker container to standardize the environment across different systems.

## Setup and Execution

### Step 1: Build the base Seismic Docker image

To do so, follow [the steps on the Seismic README](../../tools/seismic/docker/README.md).

### Step 2: Build the experiment Docker image

To build the Docker image for the experiment, run the following command:

```bash
docker build \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  -t experiment .
```

### Step 3: Execute the experiment

With the Docker images built, you can now run the experiment with the following command:

```bash
docker run \
  --mount type=bind,source="$(pwd)"/output,target=/home/experiments/02-seismic-backend-comparisson/output \
  --rm \
  experiment
```

## How It Works

TODO

## Analyzing the Results

TODO

## Expected Results and Conclusion

TODO