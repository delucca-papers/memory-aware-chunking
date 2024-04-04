#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"

NUM_INLINES_STEP=${1:-500}
NUM_INLINES_RANGE_SIZE=${2:-2}
ATTRIBUTES="envelope"
#ATTRIBUTES=${3:-$(find "${SCRIPT_DIR}/experiment/common/attributes" -type f -name "*.py" -exec basename {} .py \; | paste -sd ',' -)}
NUM_CROSSLINES_AND_SAMPLES=${4:-200}

function main {
    save_input
    run_experiment
    summarize_experiment
}

function save_input {
    mkdir -p "${OUTPUT_DIR}"

    echo "Saving experiment input..."
    echo "num_inlines_step,num_inlines_range_size,attributes,num_crosslines_and_samples" >"${OUTPUT_DIR}/input.csv"
    echo "\"${NUM_INLINES_STEP}\",\"${NUM_INLINES_RANGE_SIZE}\",\"${ATTRIBUTES}\",\"${NUM_CROSSLINES_AND_SAMPLES}\"" >>"${OUTPUT_DIR}/input.csv"
    echo
}

function run_experiment {
    echo "Running experiment..."
    python experiment/evaluate.py "${NUM_INLINES_STEP}" "${NUM_INLINES_RANGE_SIZE}" "${ATTRIBUTES}" "${NUM_CROSSLINES_AND_SAMPLES}" "${OUTPUT_DIR}"
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py "${OUTPUT_DIR}"
}

main
