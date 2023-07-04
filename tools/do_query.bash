#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:`pwd`

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

if [ -d reflections_data ]
then
    :
else
    mkdir reflections_data
fi
if [ -d documents_data ]
then
    :
else
    mkdir documents_data
fi

function get_docs()
{
    local query="${1}"
    local json_file=${2}
    TERMS=`bash tools/get_terms.bash test/result/${json_file}`
    python3 db_manager.py ../documents/dbs ../documents/document.list "${query}, ${TERMS}" 10 | tee tmp.list
}

query_dir=$1
background_file=$2
query="`cat ${query_dir}/query.txt`"

DOCUMENT_TOKENS=2048
REFLECTION_TOKENS=2048

ADD_REFLECTION="TRUE"
#ADD_REFLECTION="FALSE"
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
            echo "INFO: SIMLIRARITY EXTRACT FOR BACKGROUND KNOWLEDGES"
            if [ -d reflections_data/data_model ]
            then
                echo "INFO: CLEANING EXISTING MODELS"
                python3 data_model/reflection_data_cleaner.py reflections_data
                python3 data_model/document_data_cleaner.py documents_data

                python3 data_model/reflection_similarity_extractor.py "$query" reflections_data ${REFLECTION_TOKENS} > ./test/result/background_knowledges.json
                python3 critical_thinking.py  "$query" ./test/result/background_knowledges.json
                python3 check_recover_json.py ./test/result/critical_thinking.json
                if [ $? -ne 0 ]
                then
                    exit 1
                fi
                python3 data_model/reflection_data_persistentor.py reflections_data ./test/result/critical_thinking.json
            else
                python3 critical_thinking.py  "$query" ${background_file}
                python3 check_recover_json.py ./test/result/critical_thinking.json
                if [ $? -ne 0 ]
                then
                    exit 1
                fi
                python3 data_model/reflection_data_persistentor.py reflections_data ./test/result/critical_thinking.json
            fi
            echo "INFO: GETTING DOCUMENTS"
            get_docs "${query}" critical_thinking.json
            documents=`cat tmp.list`
            echo "INFO: PLANNING"
            python3 planner.py "$query\n: Please research focusing on the following document:\n ${documents} " ../documents/document.list ${background_file} test/result/critical_thinking.json 
            if [ $? -ne 0 ]
            then
                exit 1
            fi
        else
            echo "INFO: PLANNING"
            echo "INFO: GETTING DOCUMENTS"
            get_docs "${query}" reflection.json
            documents=`cat tmp.list`
            python3 planner.py "$query\n: Please research focusing on the following document:\n ${documents}" ../documents/document.list ${background_file} test/result/reflection.json
            if [ $? -ne 0 ]
            then
                exit 1
            fi
        fi
    else
        echo "INFO: PLANNING"
        rm -rf test/result/*
        rm -rf test/*.json
        touch test/result/reflection.json
        python3 planner.py "$query" ../documents/document.list ${background_file} test/result/reflection.json
        if [ $? -ne 0 ]
        then
            exit 1
        fi
    fi
    echo "INFO: TACTICAL PLANNING"
    python3 tactical_plannig.py
    echo "INFO: MERGING RESULT"
    if [ -f "./test/result/plan_result.json" ]
    then
        #mv ./test/result/plan_result.json ./test/result/prev_plan_result.json
        python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json
        #mv ./test/result/plan_result.json ./test/result/next_plan_result.json

        #cat ./test/result/prev_plan_result.json  > ./test/result/plan_result.json
        #cat ./test/result/next_plan_result.json >> ./test/result/plan_result.json
    else
        python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json
    fi

    echo "INFO: saving results"
    python3 data_model/document_data_persistentor.py ./documents_data ./test/result/plan_result.json
    echo "INFO: SIMILARITY EXTRACTOR FOR DOCUMENTS"
    python3 data_model/document_similarity_extractor.py "$query" ./documents_data ${DOCUMENT_TOKENS} | tee ./test/result/plan_result.json

    if [ ${ADD_REFLECTION} = "TRUE" ]
    then
        echo "INFO: REFLECTING..."
        if [ -f "./test/result/reflection.json" ]
        then
            python3 reflection.py "$query" ../documents/document.list "./test/result/reflection.json" ${background_file} "./prompt_templates/ptemplate_reflection.txt"
        else
            python3 reflection.py "$query" ../documents/document.list "./test/result/critical_thinking.json" ${background_file} "./prompt_templates/ptemplate_reflection.txt"
        fi
        python3 check_recover_json.py ./test/result/reflection.json
        if [ $? -ne 0 ]
        then
            exit 1
        fi
        python3 data_model/reflection_data_persistentor.py reflections_data ./test/result/reflection.json

        echo "INFO: ADD REFLECTION TERMS..."
        #cp ./test/result/reflection.json ./test/result/prev_reflection.json
        python3 reflection.py "$query" ../documents/document.list "./test/result/reflection.json" ${background_file} "./prompt_templates/ptemplate_reflection_addterms.txt"
        python3 check_recover_json.py ./test/result/reflection.json
        if [ $? -ne 0 ]
        then
            exit 1
        fi
        python3 data_model/reflection_data_persistentor.py reflections_data ./test/result/reflection.json
        
        echo "INFO: SIMLIRARITY EXTRACT FOR REFLECTION"
        python3 data_model/reflection_similarity_extractor.py "$query" reflections_data ${REFLECTION_TOKENS} > ./test/result/reflection.json
    else
        echo "INFO: SKIP REFLECTION"
    fi
    echo "INFO: EVALUATE"
    python3 evaluator.py "$query" \
            ./test/result/updated_plan.json \
            ./test/result/memory.json \
            ./test/result/reflection.json \
            | tee ./test/result/result.txt

    dir_name=q_${TRY_NO}
    if [ -d ${query_dir}/${dir_name} ]
    then
        :
    else
        mkdir ${query_dir}/${dir_name}
    fi
    cp -rp test/* ${query_dir}/${dir_name}/
done
