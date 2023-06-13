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

rm -rf test/result/*
rm -rf test/*.json

TRY_NO=1
python3 planner.py "$query" ../documents/document.list 
python3 tactical_plannig.py
python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json

dir_name=q_${TRY_NO}
if [ -d ${query_dir}/${dir_name} ]
then
    :
else
    mkdir ${query_dir}/${dir_name}
fi
cp -rp test/* ${query_dir}/${dir_name}/
