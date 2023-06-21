#!/bin/bash

if [ $# -ne 1 ]
then
	echo "Usage: $0 <reflection path>"
	exit 1
fi

reflection_path=${1}

grep Term ${reflection_path}  | awk -F: '{print $2}' | sort | uniq | sed 's/\"//g'| sed ':a;N;$!ba;s/\n//g'
