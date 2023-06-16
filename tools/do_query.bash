#!/bin/bash

if [ $# -ne 2 ]
then
    echo "Usage: $0 <query_dir> <background_knowledge_path>"
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
background_file=$2
query="`cat ${query_dir}/query.txt`"

ADD_REFLECTION="TRUE"
export NEW_STARTEGY=
for TRY_NO in `seq 1 2`
do
    if [ ${ADD_REFLECTION} = "TRUE" ]
    then
        if [ ${TRY_NO} -eq 1 ]
        then
            rm -rf test/result/*
            rm -rf test/*.json
            echo "INFO: CRITICAL THINKING"
            python3 critical_thinking.py  "$query" ${background_file}
            echo "INFO: PLANNING"
            python3 planner.py "$query" ../documents/document.list ${background_file} test/result/critical_thinking.json
        else
            echo "INFO: PLANNING"
            python3 planner.py "$query" ../documents/document.list ${background_file} test/result/reflection.json
        fi
    else
        echo "INFO: PLANNING"
        rm -rf test/result/*
        rm -rf test/*.json
        touch test/result/reflection.json
        python3 planner.py "$query" ../documents/document.list ${background_file} test/result/reflection.json
    fi
    echo "INFO: TACTICAL PLANNING"
    python3 tactical_plannig.py
    echo "INFO: MERGING RESULT"
    python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json
    if [ ${ADD_REFLECTION} = "TRUE" ]
    then
        echo "INFO: REFLECTING..."
        python3 reflection.py "$query" ../documents/document.list ${background_file}
    else
        echo "INFO: SKIP REFLECTION"
    fi
    echo "INFO: EVALUATE"
    python3 evaluator.py "$query" \
            ./test/result/updated_plan.json \
            ./test/result/memory.json \
            ./test/result/reflection.json \
            | tee ./test/result/result.txt
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
