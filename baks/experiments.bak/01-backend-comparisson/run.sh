#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_ELEMENTS
export OUTPUT_DIR
export LOGGING_LEVEL
export UNIT
#
# For development
# NUM_ELEMENTS="100000"
# OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# LOGGING_LEVEL="DEBUG"
# UNIT="kb"
#
# For production
NUM_ELEMENTS="10_000_000"
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
LOGGING_LEVEL="DEBUG"
UNIT="mb"
#
################################################################################

function main {
    save_input

    run_with_backend "psutil"
    run_with_backend "resource"
    run_with_backend "mprof"
    run_with_backend "tracemalloc"
    run_with_backend "kernel"

    summarize_experiment
}

function save_input {
    mkdir -p "${OUTPUT_DIR}"

    echo "Saving experiment input..."
    echo "num_elements" >"${OUTPUT_DIR}/input.csv"
    echo "${NUM_ELEMENTS}" >>"${OUTPUT_DIR}/input.csv"
    echo
}

function run_with_backend {
    local backend_name=$1

    export DOWSER_OUTPUT_DIR="${OUTPUT_DIR}"
    export DOWSER_METRICS_MEMORY_USAGE_UNIT="${UNIT}"
    export DOWSER_LOGGING_LEVEL="${LOGGING_LEVEL}"
    export EXPERIMENT_BACKEND="${backend_name}"
    export EXPERIMENT_NUM_ELEMENTS="${NUM_ELEMENTS}"

    echo "Running with ${backend_name} backend..."
    python experiment/profile_backend.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py
}

main
