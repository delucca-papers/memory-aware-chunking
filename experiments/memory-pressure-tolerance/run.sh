#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
export NUM_INLINES
export NUM_CROSSLINES
export NUM_SAMPLES
export STARTING_PRESSURE
export STEP_SIZE
export NUM_ITERATIONS
export ATTRIBUTES
export OUTPUT_DIR
export LOG_LEVEL
#
# For development
NUM_INLINES="10"
NUM_CROSSLINES="10"
NUM_SAMPLES="10"
STARTING_PRESSURE="20"
STEP_SIZE="10"
NUM_ITERATIONS="2"
ATTRIBUTES="chaos"
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
LOG_LEVEL="DEBUG"
#
# For production
# NUM_INLINES="200"
# NUM_CROSSLINES="200"
# NUM_SAMPLES="1000"
# STARTING_PRESSURE="0"
# STEP_SIZE="1"
# NUM_ITERATIONS="5"
# ATTRIBUTES=$(find "${SCRIPT_DIR}/experiment/common/attributes" -type f -name "*.py" -exec basename {} .py \; | paste -sd ',' -)
# OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
# LOG_LEVEL="DEBUG"
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
    echo "Number of Inlines, Number of Crosslines, Number of Samples, Starting Pressure, Step Size, Number of Iterations, Attributes, Output Directory, Log Level" >"${OUTPUT_DIR}/input.csv"
    echo "\"${NUM_INLINES}\",\"${NUM_CROSSLINES}\",\"${NUM_SAMPLES}\",\"${STARTING_PRESSURE}\",\"${STEP_SIZE}\",\"${NUM_ITERATIONS}\",\"${ATTRIBUTES}\",\"${OUTPUT_DIR}\",\"${LOG_LEVEL}\"" >>"${OUTPUT_DIR}/input.csv"
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
