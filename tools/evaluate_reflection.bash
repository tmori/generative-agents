#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <qa_dir>"
    exit 1
fi

qa_dir=${1}

python3 tools/evaluate_reflection.py \
    ${qa_dir}/q_1/result/reflection.json

python3 tools/evaluate_reflection.py \
    ${qa_dir}/q_2/result/reflection.json
