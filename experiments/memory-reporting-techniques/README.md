# Memory Reporting Techniques Experiment

## Overview

This experiment aims to compare different memory usage reporting tools in Python by monitoring the memory usage of a specific task.
The tools we're evaluating are:

- **mprof**:
A tool for tracking memory usage over time.

- **psutil**:
A library for getting information on running processes and system utilization.

- **resource**:
A Python standard library for measuring and controlling system resources.

- **querying `/proc` directly**:
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

1. **Build the base Docker image**:

All experiments share a base Docker image that contains some common dependencies and setup.
So, the first step is to go on the parent directory (`/experiments`) and run the following command:

```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t memory-profile/experiment .
```

2. **Build the Docker Container**:
With the base image built, get back to this directory (`/experiments/memory-reporting-techniques`) and build the Docker container for the experiment.
This process includes installing Python and the necessary packages.

```bash
docker build -t memory-profile/experiment/memory-reporting-techniques .
```

2. **Run the Experiment**:
After building the container, run the experiment.
This step will execute the memory-intensive task within the Docker environment and log the memory usage data for each tool.

```bash
docker run --mount type=bind,source="$(pwd)"/output,target=/experiments/memory-reporting-techniques/output --rm memory-profile/experiment/memory-reporting-techniques
```

> [!TIP]
> The default array size is 1.000.000.
> If you want to run the experiment with a larger array (to consume more memory) you can pass it as an argument.
> Like this: `docker run ... memory-profile/experiment/memory-reporting-techniques <array-size>

## How It Works

The Docker container encapsulates the environment and dependencies needed for the experiment.
When you run the container, it executes a predefined memory-intensive task.
The experiment script inside the container is designed to measure and log memory usage using the tools mentioned above at different stages: initial, peak, and final memory usage.

## Analyzing the Results

The experiment outputs the memory usage data for each tool.
Compare these results to assess the accuracy and efficiency of each memory reporting technique.
The analysis can help understand how each tool performs under the same conditions and which might be most suitable for your needs.

After the experiment is executed, a new timestamped folder will be created inside the `output` folder.
Inside that folder you will find:
- A `summary.jpg` file containing a graph of the memory usage data comparing all tools.
- A directory for each tool, containing detailed information of each.

## Expected Results and Conclusion

After running your experiment, you should find a result similar to this:

<table>
  <tr>
    <td><img src="./output/20240401_153049/summary.jpg" /></td>
    <td><img src="./output/20240401_195942/summary.jpg" /></td>
  </tr>
  <tr>
    <td align="center"><sub><strong>Figure 1:</strong> Memory reporting comparisson while using the input paratemeter <code>num_elements=1_000_000</code></sub><br/></td>
    <td align="center"><sub><strong>Figure 2:</strong> Memory reporting comparisson while using the input paratemeter <code>num_elements=100_000_000</code></sub></td>
  </tr>
</table>

Upon examining the memory usage reported by mprof, psutil, resource, and direct querying from /proc during a memory-intensive task, we can draw the following conclusions:

- **/proc:**
Representing the kernel's direct report, it started with a low initial memory footprint, showed a consistent rise to peak memory usage, and a substantial drop to a final memory value that is slightly above the initial value.
Given that this data comes directly from the kernel, it can be considered the most accurate and reliable among the tools tested.

- **psutil and resource:**
Neither tool was able to capture the peak memory usage, which significantly limits their utility in scenarios where understanding peak memory allocation is critical.
Despite this limitation, psutil displayed a memory usage pattern with proper release after the task completion, whereas resource reported a lower initial usage and an increase at the final check, which, in the absence of peak memory data, is difficult to evaluate for accuracy.

- **mprof:**
This tool reported a continuous increase from initial to final memory usage.
However, with /proc as the source of truth, the peak memory usage reported by mprof must be viewed critically, especially since mprof may include additional overhead in its measurements.

Based on the results from *figure 1*, we can see the difference between the memory reporting techniques.
If we scale the input parameter, like in *figure 2*, this difference becomess less evident.
Considering the source of truth and the limitations of psutil and resource, the direct measurements from /proc are recommended for evaluating memory usage of a given algorithm.
This method reflects the most accurate memory usage pattern from the kernel's perspective, ensuring the highest fidelity in reporting actual memory usage, including the peak memory, which is often the most critical aspect when assessing the memory efficiency of an algorithm.

It is essential to note that while /proc provides the most accurate measurements, the practicality of using it directly may depend on the ease of access, parsing, and integration into existing toolchains.
For a more convenient and integrated approach, tools like psutil might still be preferable in less critical scenarios where peak memory usage is not the primary concern.