#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_ELEMENTS
export OUTPUT_DIR
export SESSION_ID_PREFIX
export LOGGING_LEVEL
export LOGGING_TRANSPORTS
export UNIT
#
# For development
# NUM_ELEMENTS="100000"
# OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# SESSION_ID_PREFIX="${TIMESTAMP}"
# LOGGING_LEVEL="DEBUG"
# LOGGING_TRANSPORTS="CONSOLE"
# UNIT="kb"
#
# For production
NUM_ELEMENTS="10_000_000"
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
SESSION_ID_PREFIX="${TIMESTAMP}"
LOGGING_LEVEL="DEBUG"
LOGGING_TRANSPORTS="CONSOLE,FILE"
UNIT="mb"
#
################################################################################

function main {
    #save_input

    #run_with_backend "psutil"
    #run_with_backend "resource"
    run_with_backend "tracemalloc"
    #run_with_backend "kernel"

    #summarize_experiment
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

    echo "Running with ${backend_name} backend..."
    EXPERIMENT_SESSION_ID="${SESSION_ID_PREFIX}-${backend_name}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}/${backend_name}" \
        EXPERIMENT_LOGGING_LEVEL="${LOGGING_LEVEL}" \
        EXPERIMENT_LOGGING_TRANSPORTS="${LOGGING_TRANSPORTS}" \
        EXPERIMENT_BACKEND_NAME="${backend_name}" \
        EXPERIMENT_NUM_ELEMENTS="${NUM_ELEMENTS}" \
        python experiment/profile_backend.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}" \
        EXPERIMENT_UNIT="${UNIT}" \
        python experiment/summarize.py
}

main
