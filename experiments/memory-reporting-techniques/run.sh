#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

################################################################################
#
# Input Parameters
# export NUM_ELEMENTS="100"
# export OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
#
# For production
export NUM_ELEMENTS="1000000"
export OUTPUT_DIR="${SCRIPT_DIR}/output/${TIMESTAMP}"
#
################################################################################

function main {
    save_input

    run_tool "mprof"
    run_tool "psutil"
    run_tool "resource"
    run_tool "proc"

    summarize_experiment
}

function save_input {
    mkdir -p "${OUTPUT_DIR}"

    echo "Saving experiment input..."
    echo "num_elements" >"${OUTPUT_DIR}/input.csv"
    echo "${NUM_ELEMENTS}" >>"${OUTPUT_DIR}/input.csv"
    echo
}

function run_tool {
    local tool_name=$1

    export TOOL_OUTPUT_DIR="${OUTPUT_DIR}/${tool_name}"
    mkdir -p "${TOOL_OUTPUT_DIR}"

    echo "Running ${tool_name}..."
    python experiment/evaluate_"${tool_name}".py
    echo
}

function summarize_experiment {
    echo "Summarizing experiment..."
    python experiment/summarize.py
}

main
