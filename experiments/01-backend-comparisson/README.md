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

The experiment focuses on measuring:
- **Initial Memory Used**: Before the task starts.
- **Peak Memory Used**: The highest memory usage during the task.
- **Final Memory Used**: After the task completes.

## Prerequisites

- **Docker**:
Ensure Docker is installed on your system.
This experiment runs inside a Docker container to standardize the environment across different systems.

## Setup and Execution

TODO


## How It Works

The Docker container encapsulates the environment and dependencies needed for the experiment.
When you run the container, it executes a predefined memory-intensive task.
The experiment script inside the container is designed to measure and log memory usage using the tools mentioned while the task is running.

## Analyzing the Results

The experiment outputs the memory usage data for each tool.
Compare these results to assess the accuracy and efficiency of each memory reporting technique.
The analysis can help understand how each tool performs under the same conditions and which might be most suitable for your needs.

After the experiment is executed, a new timestamped folder will be created inside the `output` folder.
Inside that folder you will find:
- A `memory-usage-comparisson.png` file containing a graph of the memory usage data comparing all tools.
- An `execution-time-comparisson.png` file containing a graph of the execution time data comparing all tools.
- A log file containing all the logs generated during the experiment.
- A `profiler` folder containing every data the tool profiled during the execution.

## Expected Results and Conclusion

TODO