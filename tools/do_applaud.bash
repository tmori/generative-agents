#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:`pwd`

if [ $# -ne 1 ]
then
    echo "Usage: $0 <name>"
    exit 1
fi

PRMT_TMP_PATH=`python3 params.py "prompt_templates_path"`
if [ ! -d ${PRMT_TMP_PATH} ]
then
    echo "ERROR: can not found path: ${PRMT_TMP_PATH}"
    exit 1
fi
DOCUMENT_PATH=`python3 params.py "documents_path"`
if [ ! -d ${DOCUMENT_PATH} ]
then
    echo "ERROR: can not found path: ${DOCUMENT_PATH}"
    exit 1
fi
DOC_DATA_PATH=`python3 params.py "documents_data_path"`
if [ ! -d ${DOC_DATA_PATH} ]
then
    mkdir ${DOC_DATA_PATH}
fi
REF_DATA_PATH=`python3 params.py "reflections_data_path"`
if [ ! -d ${REF_DATA_PATH} ]
then
    mkdir ${REF_DATA_PATH}
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

name="$1"applaud_params.json
query_dir=./applaud_data/query_dir
background_file="noidea.txt"
cp param_templates/applaud_params.json params.json
query="$(cat ${query_dir}/query.txt | sed -e "s/<NAME>/${name}/g")"

DOCUMENT_TOKENS=3096
REFLECTION_TOKENS=3096
#USE_BACKGROUND="FALSE"
USE_BACKGROUND="TRUE"
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
            if [ ${USE_BACKGROUND} = "TRUE" -a -d ${REF_DATA_PATH}/data_model ]
            then
                echo "INFO: CLEANING EXISTING MODELS"
                python3 data_model/reflection_data_cleaner.py ${REF_DATA_PATH}
                python3 data_model/document_data_cleaner.py ${DOC_DATA_PATH}

                python3 data_model/reflection_similarity_extractor.py "$query" ${REF_DATA_PATH} ${REFLECTION_TOKENS} > ./test/result/background_knowledges.json
                python3 critical_thinking.py  "$query" ./test/result/background_knowledges.json
                python3 check_recover_json.py ./test/result/critical_thinking.json
                if [ $? -ne 0 ]
                then
                    exit 1
                fi
                python3 data_model/reflection_data_persistentor.py ${REF_DATA_PATH} ./test/result/critical_thinking.json
            else
                python3 critical_thinking.py  "$query" ${background_file}
                python3 check_recover_json.py ./test/result/critical_thinking.json
                if [ $? -ne 0 ]
                then
                    exit 1
                fi
                python3 data_model/reflection_data_persistentor.py ${REF_DATA_PATH} ./test/result/critical_thinking.json
            fi
            echo "INFO: PLANNING"
            python3 planner.py "$query ${documents} " ${DOCUMENT_PATH}/document.list ${background_file} test/result/critical_thinking.json 
            if [ $? -ne 0 ]
            then
                exit 1
            fi
        else
            echo "INFO: PLANNING"
            python3 planner.py "$query" ${DOCUMENT_PATH}/document.list ${background_file} test/result/reflection.json
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
        python3 planner.py "$query" ${DOCUMENT_PATH}/document.list ${background_file} test/result/reflection.json
        if [ $? -ne 0 ]
        then
            exit 1
        fi
    fi
    echo "INFO: TACTICAL PLANNING"
    python3 tactical_plannig.py text
    echo "INFO: MERGING RESULT"
    if [ -f "./test/result/plan_result.json" ]
    then
        python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json
    else
        python3 evaluator.py "$query" ./test/result/updated_plan.json ./test/result/memory.json
    fi

    echo "INFO: saving results"
    cp ./test/result/plan_result.json ./test/result/plan_result_org.json
    python3 data_model/document_data_persistentor.py ${DOC_DATA_PATH} ./test/result/plan_result.json
    echo "INFO: SIMILARITY EXTRACTOR FOR DOCUMENTS"
    python3 data_model/document_similarity_extractor.py "$query" ${DOC_DATA_PATH} ${DOCUMENT_TOKENS} | tee ./test/result/plan_result.json

    if [ ${ADD_REFLECTION} = "TRUE" ]
    then
        echo "INFO: REFLECTING..."
        if [ -f "./test/result/reflection.json" ]
        then
            python3 reflection.py "$query" ${DOCUMENT_PATH}/document.list "./test/result/reflection.json" ${background_file} "${PRMT_TMP_PATH}/ptemplate_reflection.txt"
        else
            python3 reflection.py "$query" ${DOCUMENT_PATH}/document.list "./test/result/critical_thinking.json" ${background_file} "${PRMT_TMP_PATH}/ptemplate_reflection.txt"
        fi
        cp ./test/result/reflection.json ./test/result/reflection_org.json
        python3 check_recover_json.py ./test/result/reflection.json
        if [ $? -ne 0 ]
        then
            exit 1
        fi
        python3 data_model/reflection_data_persistentor.py ${REF_DATA_PATH} ./test/result/reflection.json

        echo "INFO: ADD REFLECTION TERMS..."
        python3 reflection.py "$query" ${DOCUMENT_PATH}/document.list "./test/result/reflection.json" ${background_file} "${PRMT_TMP_PATH}/ptemplate_reflection_addterms.txt"
        python3 check_recover_json.py ./test/result/reflection.json
        if [ $? -ne 0 ]
        then
            exit 1
        fi
        python3 data_model/reflection_data_persistentor.py ${REF_DATA_PATH} ./test/result/reflection.json
        
        echo "INFO: SIMLIRARITY EXTRACT FOR REFLECTION"
        python3 data_model/reflection_similarity_extractor.py "$query" ${REF_DATA_PATH} ${REFLECTION_TOKENS} > ./test/result/reflection.json
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
