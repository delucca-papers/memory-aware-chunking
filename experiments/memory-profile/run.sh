#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"

NUM_INLINES_STEP=${1:-500}
NUM_INLINES_RANGE_SIZE=${2:-20}
ATTRIBUTES=${3:-$(find "${SCRIPT_DIR}/experiment/common/attributes" -type f -name "*.py" -exec basename {} .py \; | paste -sd ',' -)}
NUM_CROSSLINES_AND_SAMPLES=${4:-200}
NUM_ITERATIONS_PER_INLINE=${5:-5}

# For dev
# ATTRIBUTES="envelope,chaos"
# NUM_INLINES_RANGE_SIZE=${2:-2}
# NUM_ITERATIONS_PER_INLINE=${5:-2}

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
    python experiment/evaluate.py "${NUM_INLINES_STEP}" "${NUM_INLINES_RANGE_SIZE}" "${ATTRIBUTES}" "${NUM_CROSSLINES_AND_SAMPLES}" "${OUTPUT_DIR}" "${NUM_ITERATIONS_PER_INLINE}"
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py "${OUTPUT_DIR}"
}

main
