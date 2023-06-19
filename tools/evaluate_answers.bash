#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <qa_dir>"
    exit 1
fi

qa_dir=${1}

python3 evaluate_results.py \
    ${qa_dir}/query.txt \
    ${qa_dir}/q_1/result/result.txt \
    ${qa_dir}/q_2/result/result.txt \
    ./tools/prompt_templates/ptemplate_evaluate_answers.txt

