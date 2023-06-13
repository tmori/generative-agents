#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <query_dir>"
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
query_dir=$1
query="`cat ${query_dir}/query.txt`"


TRY_NO=1
if [ ${TRY_NO} = 1 ]
then
    rm -rf test/result/*
    rm -rf test/*.json
    python3 critical_thinking.py  "$query"
    python3 planner.py "$query" ../documents/document.list test/result/critical_thinking.json
else
    python3 planner.py "$query" ../documents/document.list test/result/reflection.json
fi
python3 tactical_plannig.py
python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json
python3 reflection.py "$query"


dir_name=q_${TRY_NO}
if [ -d ${query_dir}/${dir_name} ]
then
    :
else
    mkdir ${query_dir}/${dir_name}
fi
cp -rp test/* ${query_dir}/${dir_name}/
