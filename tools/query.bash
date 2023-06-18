#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: $0 <question>"
    exit 1
fi

question=${1}
echo "${question}" > query_dir/query.txt
bash tools/do_query.bash query_dir noidea.txt
