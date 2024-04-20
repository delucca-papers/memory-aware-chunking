#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_ELEMENTS
export OUTPUT_DIR
export EXECUTION_ID
export LOGGING_LEVEL
export UNIT
#
# For development
# NUM_ELEMENTS="100000"
# OUTPUT_DIR="${SCRIPT_DIR}/output"
# EXECUTION_ID="${TIMESTAMP}"
# LOGGING_LEVEL="DEBUG"
# UNIT="kb"
#
# For production
NUM_ELEMENTS="10_000_000"
OUTPUT_DIR="${SCRIPT_DIR}/output/"
EXECUTION_ID="${TIMESTAMP}"
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

    #summarize_experiment
}

function save_input {
    local expected_output_dir="${OUTPUT_DIR}/${EXECUTION_ID}"

    mkdir -p "${expected_output_dir}"

    echo "Saving experiment input..."
    echo "num_elements" >"${expected_output_dir}/input.csv"
    echo "${NUM_ELEMENTS}" >>"${expected_output_dir}/input.csv"
    echo
}

function run_with_backend {
    local backend_name=$1

    echo "Running with ${backend_name} backend..."
    EXPERIMENT_EXECUTION_ID="${TIMESTAMP}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}" \
        EXPERIMENT_UNIT="${UNIT}" \
        EXPERIMENT_LOGGING_LEVEL="${LOGGING_LEVEL}" \
        EXPERIMENT_BACKEND="${backend_name}" \
        EXPERIMENT_NUM_ELEMENTS="${NUM_ELEMENTS}" \
        python experiment/profile_backend.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py
}

main
