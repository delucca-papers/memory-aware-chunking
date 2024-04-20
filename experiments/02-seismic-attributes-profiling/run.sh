#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_INLINES
export NUM_CROSSLINES
export NUM_SAMPLES
export STEP_SIZE
export RANGE_SIZE
export NUM_ITERATIONS
export ATTRIBUTES
export OUTPUT_DIR
export EXECUTION_ID
export LOG_LEVEL
#
# For development
NUM_INLINES="10"
NUM_CROSSLINES="10"
NUM_SAMPLES="10"
STEP_SIZE="10"
RANGE_SIZE="2"
NUM_ITERATIONS="5"
ATTRIBUTES="envelope"
OUTPUT_DIR="${SCRIPT_DIR}/output"
EXECUTION_ID="${TIMESTAMP}"
LOG_LEVEL="DEBUG"
#
# For production
# NUM_INLINES="200"
# NUM_CROSSLINES="200"
# NUM_SAMPLES="1000"
# STEP_SIZE="100"
# RANGE_SIZE="20"
# NUM_ITERATIONS="5"
# ATTRIBUTES=$(find "${SCRIPT_DIR}/experiment/common/attributes" -type f -name "*.py" -exec basename {} .py \; | paste -sd ',' -)
# OUTPUT_DIR="${SCRIPT_DIR}/output"
# EXECUTION_ID="${TIMESTAMP}"
# LOG_LEVEL="DEBUG"
#
################################################################################

function main {
    save_input

    generate_synthetic_data
    run_experiment

    #summarize_experiment
}

function save_input {
    local expected_output_dir="${OUTPUT_DIR}/${EXECUTION_ID}"

    mkdir -p "${expected_output_dir}"

    echo "Saving experiment input..."
    echo "Number of Inlines, Number of Crosslines, Number of Samples, Step Size, Range Size, Number of Iterations, Attributes" >"${expected_output_dir}/input.csv"
    echo "\"${NUM_INLINES}\",\"${NUM_CROSSLINES}\",\"${NUM_SAMPLES}\",\"${STEP_SIZE}\",\"${RANGE_SIZE}\",\"${NUM_ITERATIONS}\",\"${ATTRIBUTES}\"" >>"${expected_output_dir}/input.csv"
    echo
}

function generate_synthetic_data {
    echo "Generating synthetic data..."
    EXPERIMENT_EXECUTION_ID="${EXECUTION_ID}" \
        EXPERIMENT_NUM_INLINES="${NUM_INLINES}" \
        EXPERIMENT_NUM_CROSSLINES="${NUM_CROSSLINES}" \
        EXPERIMENT_NUM_SAMPLES="${NUM_SAMPLES}" \
        EXPERIMENT_STEP_SIZE="${STEP_SIZE}" \
        EXPERIMENT_RANGE_SIZE="${RANGE_SIZE}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        python experiment/generate.py
    echo
}

function run_experiment {
    echo "Running experiment..."
    EXPERIMENT_EXECUTION_ID="${EXECUTION_ID}" \
        EXPERIMENT_OUTPUT_DIR="${OUTPUT_DIR}" \
        EXPERIMENT_NUM_ITERATIONS="${NUM_ITERATIONS}" \
        EXPERIMENT_ATTRIBUTES="${ATTRIBUTES}" \
        EXPERIMENT_LOGGING_LEVEL="${LOG_LEVEL}" \
        python experiment/evaluate.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py
}

main
