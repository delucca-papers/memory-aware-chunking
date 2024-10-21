# Dask Auto-Chunking

This repository consolidates experiments and tooling created to explore and improve Dask’s Auto-Chunking feature.
It contains reusable libraries and multiple experiments that demonstrate the performance, behavior, and potential optimizations of Dask’s chunking mechanism in distributed computing environments.

#### Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Repository Structure](#repository-structure)
- [License](#license)

## Introduction

Dask’s Auto-Chunking feature provides an efficient way to split large datasets into smaller chunks that can be processed in parallel.
While Dask offers automatic chunking by default, this repository explores ways to better understand and improve its behavior in specific scenarios.

The goal of this project is to provide a collection of experiments and tools that showcase how Dask’s Auto-Chunking performs in different contexts, with a focus on optimization and scalability.
This includes both theoretical analysis and practical code implementations.

## Getting Started

To get started with this repository, follow the steps below.

Installation

	1.	Clone the repository:
```sh
git clone https://github.com/[your-username]/dask-auto-chunking.git
cd dask-auto-chunking
```

	2.	Install the necessary dependencies (you may use conda, venv, or any other environment manager). Here’s an example using pip:
```sh
pip install -r requirements.txt
```

## Repository Structure

    - [`experiments/`](./experiments): This folder contains all the experiments designed to demonstrate the effects and performance of Dask Auto-Chunking in various scenarios.
	- [`libs/`]: This folder contains shared code, utilities, and helper functions used across multiple experiments and tools. These libraries can be reused to facilitate new experiments or optimize existing workflows.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.