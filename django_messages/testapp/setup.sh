#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

pip install -r "${SCRIPT_DIR}/requirements.text"

ansible-playbook "${SCRIPT_DIR}/ansible_setup_test.yml"