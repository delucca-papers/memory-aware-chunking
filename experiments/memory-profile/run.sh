#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_INLINES="10"
export NUM_CROSSLINES="10"
export NUM_SAMPLES="10"
export STEP_SIZE="10"
export RANGE_SIZE="1"
export NUM_ITERATIONS="1"
export ATTRIBUTES="chaos"
export OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
export LOG_LEVEL="DEBUG"
#
# For production
# export NUM_INLINES="500"
# export NUM_CROSSLINES="500"
# export NUM_SAMPLES="1000"
# export STEP_SIZE="200"
# export RANGE_SIZE="20"
# export NUM_ITERATIONS="5"
# export ATTRIBUTES=$(find "${SCRIPT_DIR}/experiment/common/attributes" -type f -name "*.py" -exec basename {} .py \; | paste -sd ',' -)
# export OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# export LOG_LEVEL="DEBUG"
#
################################################################################

function main {
    save_input
    run_experiment
    summarize_experiment
}

function save_input {
    mkdir -p "${OUTPUT_DIR}"

    echo "Saving experiment input..."
    echo "Number of Inlines Step,Number of Inlines Range Size,Attributes,Number of Crosslines and Samples, Number of Iterations per Inline" >"${OUTPUT_DIR}/input.csv"
    echo "\"${NUM_INLINES_STEP}\",\"${NUM_INLINES_RANGE_SIZE}\",\"${ATTRIBUTES}\",\"${NUM_CROSSLINES_AND_SAMPLES}\",\"${NUM_ITERATIONS_PER_INLINE}\"" >>"${OUTPUT_DIR}/input.csv"
    echo
}

function run_experiment {
    echo "Running experiment..."
    python experiment/evaluate.py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py
}

main
