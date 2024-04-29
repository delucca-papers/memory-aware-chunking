#!/usr/bin/env bash

PYTHON_CMD=${1:-"python"}
SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_INLINES
export NUM_CROSSLINES
export NUM_SAMPLES
export ATTRIBUTE
export OUTPUT_DIR
export SESSION_ID
export PRECISION
export LOG_LEVEL
#
# For development
NUM_INLINES="100"
NUM_CROSSLINES="100"
NUM_SAMPLES="100"
ATTRIBUTE="envelope"
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
SESSION_ID="${TIMESTAMP}"
PRECISION="2"
LOG_LEVEL="DEBUG"
#
# For production
# NUM_INLINES="100"
# NUM_CROSSLINES="600"
# NUM_SAMPLES="1000"
# ATTRIBUTE="envelope"
# OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# SESSION_ID="${TIMESTAMP}"
# PRECISION="2"
# LOG_LEVEL="INFO"
#
################################################################################

function main {
    save_input
    generate_synthetic_data

    run_with_backend "psutil"
    run_with_backend "resource"
    run_with_backend "mprof"
    run_with_backend "tracemalloc"
    run_with_backend "kernel"
    run_with_fil_profiler

    summarize_experiment
}

function save_input {
    mkdir -p "${OUTPUT_DIR}"

    echo "Saving experiment input..."
    echo "Number of Inlines, Number of Crosslines, Number of Samples, Attribute, Output Directory, Session ID, Precision, Log Level" >"${OUTPUT_DIR}/input.csv"
    echo "${NUM_INLINES},${NUM_CROSSLINES},${NUM_SAMPLES},${ATTRIBUTE},${OUTPUT_DIR},${SESSION_ID},${PRECISION},${LOG_LEVEL}" >>"${OUTPUT_DIR}/input.csv"
    echo
}

function generate_synthetic_data {
    echo "Generating synthetic data..."
    EXPERIMENT_SESSION_ID="${SESSION_ID}" \
        EXPERIMENT_NUM_INLINES="${NUM_INLINES}" \
        EXPERIMENT_NUM_CROSSLINES="${NUM_CROSSLINES}" \
        EXPERIMENT_NUM_SAMPLES="${NUM_SAMPLES}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}/data" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        ${PYTHON_CMD} experiment/generate.py
    echo
}

function run_with_backend {
    local backend_name=$1

    echo "Running with ${backend_name} backend..."
    EXPERIMENT_BACKEND_NAME="${backend_name}" \
        EXPERIMENT_DATA_DIR="${OUTPUT_DIR}/data" \
        EXPERIMENT_SESSION_ID="${SESSION_ID}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}/${backend_name}" \
        EXPERIMENT_ATTRIBUTE="${ATTRIBUTE}" \
        EXPERIMENT_PRECISION="${PRECISION}" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        ${PYTHON_CMD} experiment/profile_backend.py
    echo
}

function run_with_fil_profiler {
    echo "Running with fil-profiler..."
    EXPERIMENT_DATA_DIR="${OUTPUT_DIR}/data" \
        EXPERIMENT_SESSION_ID="${SESSION_ID}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}/fil" \
        EXPERIMENT_ATTRIBUTE="${ATTRIBUTE}" \
        EXPERIMENT_PRECISION="${PRECISION}" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        EXPERIMENT_ENABLED_METRICS="time" \
        ${PYTHON_CMD} \
        -m filprofiler \
        -o "${OUTPUT_DIR}/fil" \
        --no-browser \
        run experiment/profile_backend.py

    pushd "${OUTPUT_DIR}/fil" || return
    find . -mindepth 2 -type f -exec mv {} . \; && find . -mindepth 1 -type d -empty -delete
    popd || return

    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}" \
        ${PYTHON_CMD} experiment/summarize.py
}

main
