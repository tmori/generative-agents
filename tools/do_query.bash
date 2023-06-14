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

export NEW_STARTEGY=
for TRY_NO in `seq 1 2`
do
    if [ ${TRY_NO} -eq 1 ]
    then
        rm -rf test/result/*
        rm -rf test/*.json
        python3 critical_thinking.py  "$query"
        python3 planner.py "$query" ../documents/document.list test/result/critical_thinking.json
    else
        python3 planner.py "$query" ../documents/document.list test/result/reflection.json
    fi
    python3 tactical_plannig.py
    python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json | tee ./test/result/result.txt
    python3 reflection.py "$query"
    grep "NewStrategy:" ./test/result/result.txt
    if [ $? -eq 0 ]
    then
        export NEW_STARTEGY=`grep "NewStrategy:" ./test/result/result.txt | awk -F: '{print $2}'`
        echo $NEW_STRATEGY
    fi

    dir_name=q_${TRY_NO}
    if [ -d ${query_dir}/${dir_name} ]
    then
        :
    else
        mkdir ${query_dir}/${dir_name}
    fi
    cp -rp test/* ${query_dir}/${dir_name}/
done
