# Experiments Directory

This directory contains a collection of Jupyter Notebooks that explore different aspects of Dask’s Auto-Chunking feature.
Each notebook is an independent experiment aimed at understanding and improving how Dask handles chunking for distributed computations.

## How to Run the Experiments

	1.	Launch Jupyter Lab from the root of the repository:
```sh
jupyter lab
```
	2.	Navigate to the `experiments/` directory and open the notebook corresponding to the experiment you’d like to explore.
	3.	Execute the cells within the notebook to run the experiment. Each notebook includes instructions and markdown explanations to guide you through the process.

## Available Experiments

	1.	[`001-chunk-size-vs-execution-time`](./001-chunk_size_vs_execution_time.ipynb)

**Objective**:
This experiment explores how different chunk sizes affect the execution time of distributed computations in Dask.
The goal is to identify the optimal chunk size that balances performance with resource utilization.

**Key Questions**:
- How does varying the chunk size influence execution time?
- What is the relationship between chunk size, task scheduling overhead, and overall computation time?

	2.	[`002-auto-chunking-memory-impact`](./002-auto_chunking_memory_impact.ipynb)

**Objective**:
Investigate how Dask’s Auto-Chunking feature handles memory consumption during execution.
This experiment will determine whether Auto-Chunking takes memory constraints into account, or if it prioritizes other performance factors.

Key Questions:
- Does Auto-Chunking optimize for memory usage, or are there scenarios where it overlooks memory constraints?
- How does memory consumption vary between auto and manual chunking strategies?

	3.	[`003-memory-usage-by-algorithm`](./003-memory-usage-by-algorithm.ipynb)

**Objective**:
This experiment looks into how specific algorithms consume memory during their execution.
We aim to identify patterns in memory usage across different types of tensorial algorithms.

**Key Questions**:
- Which algorithms consume the most memory, and why?
- Is the memory usage directly related to the input shape, and how?

	4.	[`004-predicting-memory-usage`](./004-predicting-memory-usage.ipynb)

**Objective**:
This experiment attempts to predict the memory usage of tensorial algorithms based solely on their input shapes.
The goal is to develop a reliable model that can provide accurate memory estimates prior to execution.

**Key Questions**:
- Can we accurately predict memory usage given only input shapes?
- What factors influence the accuracy of these predictions?

	5.	[`005-best-chunk-size`](./005-best-chunk-size.ipynb)

**Objective**:
The focus of this experiment is to identify the best chunk size based on memory consumption and the available memory on the workers.
The goal is to strike a balance between memory constraints and performance.

**Key Questions**:
- How can we optimize chunk sizes to prevent exceeding worker memory?
- What trade-offs exist between chunk size and memory overhead?

	6.	[`006-memory-usage-prediction-accuracy`](./006-memory-usage-prediction-accuracy.ipynb)

**Objective**:
This experiment tests the accuracy of predicting memory usage for tensorial algorithms.
By refining our prediction models, we aim to create a robust tool for memory forecasting in distributed systems.

**Key Questions**:
- How accurately can we predict memory usage?
- What external factors might affect prediction accuracy?

	7.	[`007-optimal-chunk-size-decision`](./007-optimal-chunk-size-decision.ipynb)

**Objective**:
The goal of this experiment is to develop a strategy for deciding the best chunk size based on various factors like memory usage, and available resources.
This will help automate the chunking process for large-scale computations.

**Key Questions**:
- What metrics should be used to determine the best chunk size?
- Can we create an algorithm to automate chunk size decisions?