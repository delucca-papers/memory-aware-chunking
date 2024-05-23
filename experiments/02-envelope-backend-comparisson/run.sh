#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_INLINES
export NUM_CROSSLINES
export NUM_SAMPLES
export OUTPUT_DIR
export SESSION_ID_PREFIX
export UNIT
export LOG_LEVEL
#
# For development
#NUM_INLINES="100"
#NUM_CROSSLINES="100"
#NUM_SAMPLES="100"
#OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
#SESSION_ID_PREFIX="${TIMESTAMP}"
#UNIT="mb"
#LOG_LEVEL="DEBUG"
#
# For production
NUM_INLINES="100"
NUM_CROSSLINES="600"
NUM_SAMPLES="1000"
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
SESSION_ID_PREFIX="${TIMESTAMP}"
UNIT="mb"
LOG_LEVEL="INFO"
#
################################################################################

function main {
    save_input
    generate_synthetic_data

    run_with_backend "psutil"
    run_with_backend "kernel"
    run_with_backend "tracemalloc"
    run_with_backend "resource"

    summarize_experiment
}

function save_input {
    mkdir -p "${OUTPUT_DIR}"

    echo "Saving experiment input..."
    echo "Number of Inlines, Number of Crosslines, Number of Samples, Output Directory, Session ID, Log Level" >"${OUTPUT_DIR}/input.csv"
    echo "${NUM_INLINES},${NUM_CROSSLINES},${NUM_SAMPLES},${OUTPUT_DIR},${SESSION_ID},${LOG_LEVEL}" >>"${OUTPUT_DIR}/input.csv"
    echo
}

function generate_synthetic_data {
    echo "Generating synthetic data..."
    EXPERIMENT_NUM_INLINES="${NUM_INLINES}" \
        EXPERIMENT_NUM_CROSSLINES="${NUM_CROSSLINES}" \
        EXPERIMENT_NUM_SAMPLES="${NUM_SAMPLES}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}/data" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        python3 experiment/generate_data.py
    echo
}

function run_with_backend {
    local backend_name=$1

    echo "Running with ${backend_name} backend..."
    EXPERIMENT_SESSION_ID="${SESSION_ID_PREFIX}-${backend_name}" \
        EXPERIMENT_BACKEND_NAME="${backend_name}" \
        EXPERIMENT_DATA_DIR="${OUTPUT_DIR}/data" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}/${backend_name}" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        python3 experiment/profile_envelope.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}" \
        EXPERIMENT_UNIT="${UNIT}" \
        python3 experiment/summarize.py
}

main
