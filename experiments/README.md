# Experiments Directory

This directory contains all the experiments that are being conducted for this paper.
Each experiment is designed to test specific scenarios and is documented with a brief description and results.

## List of experiments

### Experiment 1: Memory Reporting Techniques
- **Link**: [Experiment 1](./memory-reporting-techniques/)
- **Description**: Compares and evaluate different techniques to report the memory usage of a specific task.

### Experiment 2: Memory Profile
- **Link**: [Experiment 2](./memory-profile/)
- **Description**: Profiles the memory usage of the most relevant seismic attributes.

### Experiment 3: Memory Pressure Tolerance
- **Link**: [Experiment 2](./memory-pressure-tolerance/)
- **Description**: Evaluates the maximum memory pressure that each seismic attribute can handle.

## Building the base Docker image

All experiments share a base Docker image that contains some common dependencies and setup.
So, the first step is to use this directory (`/experiments`) and run the following command:

```bash
docker build \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  --build-arg SSH_KEY="$(cat ~/.ssh/<your SSH key>)" \
  -t discovery/experiments .
```
