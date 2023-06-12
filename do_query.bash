#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <query>"
    exit 1
fi
python3 planner.py "$1" ../tutorial_langchain/docs/list.txt
python3 tactical_plannig.py
python3 evaluator.py "$1" ./test/updated_plan.json ./test/memory.json