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
export LOG_LEVEL
#
# For development
# NUM_INLINES="10"
# NUM_CROSSLINES="10"
# NUM_SAMPLES="10"
# STEP_SIZE="10"
# RANGE_SIZE="2"
# NUM_ITERATIONS="2"
# ATTRIBUTES="chaos"
# OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# LOG_LEVEL="DEBUG"
#
# For production
NUM_INLINES="200"
NUM_CROSSLINES="200"
NUM_SAMPLES="1000"
STEP_SIZE="100"
RANGE_SIZE="20"
NUM_ITERATIONS="5"
ATTRIBUTES=$(find "${SCRIPT_DIR}/experiment/common/attributes" -type f -name "*.py" -exec basename {} .py \; | paste -sd ',' -)
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
LOG_LEVEL="DEBUG"
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
