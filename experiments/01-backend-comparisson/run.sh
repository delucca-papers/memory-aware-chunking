#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_ELEMENTS
export OUTPUT_DIR
export LOGGING_LEVEL
#
# For development
# NUM_ELEMENTS="100"
# OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# LOGGING_LEVEL="DEBUG"
#
# For production
NUM_ELEMENTS="1000000"
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
LOGGING_LEVEL="INFO"
#
################################################################################

function main {
    save_input

    run_with_backend "psutil"
    run_with_backend "resource"
    run_with_backend "mprof"
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

    export DOWSER_OUTPUT_DIR="${OUTPUT_DIR}/${backend_name}"
    export EXPERIMENT_BACKEND="${backend_name}"

    echo "Running with ${backend_name} backend..."
    python experiment/profile.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    #python experiment/summarize.py
}

main
