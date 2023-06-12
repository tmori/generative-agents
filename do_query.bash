#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <query>"
    exit 1
fi

if [ -d test ]
then
    :
else
    mkdir test
fi
if [ -d test/result ]
then
    :
else
    mkdir test/result
fi

python3 planner.py "$1" ../documents/document.list 
python3 tactical_plannig.py
python3 evaluator.py "$1" ./test/result/updated_plan.json ./test/result/memory.json

