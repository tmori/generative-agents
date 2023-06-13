#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <query.txt>"
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
query="`cat $1`"
python3 planner.py "$query" ../documents/document.list 
python3 tactical_plannig.py
python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json

