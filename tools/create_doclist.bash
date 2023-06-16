#!/bin/bash

TITLE=""
function do_task()
{
    ## CREATE DB
    python3 generative-agents/document_db.py new tmp tmp/DB

    ## GET TITLE
    TITLE=`python3 generative-agents/document_db.py question "この文書の概要を調査し 、適切なタイトルを英名で階層形式(最大５階層)で表現して：<level1>-<level2>-<level3>-..。levelには空白文字は入れないで。例 ：aaa-bbb-ccc-ddd" tmp/DB | tail -n 1 | sed  's/\//\-/g'`

    ## ADD TITLE ON DOCLIST
    echo "$TITLE" >> documents/document.list

    ## MV DB TO TITLE
    mv tmp/DB documents/dbs/$TITLE
}
rm -f documents/document.list
rm -f documents/document-title-mapping.list
rm -rf documents/dbs/*

ls documents/docs > list.txt

while IFS= read -r filepath || [[ -n "$filepath" ]]; do
  if [ -n "$filepath" ]; then
    rm -rf tmp
    mkdir tmp
    cp documents/docs/"$filepath" tmp/
    do_task
    echo "${TITLE}: $filepath" >> documents/document-title-mapping.list
  fi
done < list.txt
