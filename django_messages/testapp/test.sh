#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

${SCRIPT_DIR}/setup.sh

export PYTHONPATH="${SCRIPT_DIR}/../../"; pytest ${SCRIPT_DIR}/../tests --gui