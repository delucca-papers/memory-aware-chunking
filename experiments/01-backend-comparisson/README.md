# Backend Comparisson Experiment

## Overview

This experiment aims to compare different memory usage reporting tools in Python by monitoring the memory usage of a specific task.
The tools we're evaluating are:

- **mprof**:
A tool for tracking memory usage over time.

- **psutil**:
A library for getting information on running processes and system utilization.

- **resource**:
A Python standard library for measuring and controlling system resources.

- **tracemalloc**:
A module for tracing memory blocks allocated by Python.

- **querying the kernel directly**:
A method to access system information directly from the Linux kernel.

## Prerequisites

- **Docker**:
Ensure Docker is installed on your system.
This experiment runs inside a Docker container to standardize the environment across different systems.

## Setup and Execution

### Step 1: Build the Dowser Docker image

To do so, follow [the steps on the Dowser README](../../tools/dowser/README.md#with-docker).

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
  --mount type=bind,source="$(pwd)"/output,target=/home/experiments/01-backend-comparisson/output \
  --rm \
  experiment
```

## How It Works

TODO

## Analyzing the Results

TODO

## Expected Results and Conclusion

TODO