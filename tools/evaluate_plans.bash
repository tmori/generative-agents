#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <qa_dir>"
    exit 1
fi

qa_dir=${1}

python3 evaluate_results.py \
    ${qa_dir}/query.txt \
    ${qa_dir}/q_1/result/updated_plan.json \
    ${qa_dir}/q_2/result/updated_plan.json \
    ./tools/prompt_templates/ptemplate_evaluate_plans.txt

