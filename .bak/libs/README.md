# Libraries Directory

This directory contains shared libraries and utility code that are used across the various experiments in the repository.
The code in this directory is modular and reusable, designed to assist with common tasks like chunking strategies, memory usage estimation, and other helper functions for Dask operations.

## How to Use the Libraries

1. Ensure you have the required dependencies installed for the repository.
2. Before importing the libraries, make sure the libs folder is added to your Python `sys.path`. You can do this by adding the following code snippet to the top of your Jupyter notebooks or Python scripts:
```python
import sys
import os

libs_path = os.path.abspath('../libs')
if libs_path not in sys.path:
    sys.path.append(libs_path)
```
3. After adding the libs folder to the path, import the necessary libraries into your Jupyter notebooks or Python scripts:
```python
from chunking_utils import create_manual_chunks
```

## Available Libraries

The libraries in this folder are used to support the experiments in the [`experiments/`](../experiments) directory.
Below is an overview of the currently available libraries.
Each of these libraries can be imported and reused in different contexts to streamline your experiments.

1. `chunking_utils.py`

**Objective**:
Provides utility functions for handling chunk sizes and strategies.
This includes functions for defining manual chunk sizes, comparing different chunking methods, and testing performance with varying chunk parameters.

**Key Features**:
- Functions to generate manual chunks based on input size and worker memory.
- Helper methods to compare Dask Auto-Chunking with custom chunking strategies.