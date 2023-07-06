#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

def get_param(param_name: str):
    with open('./params.json', 'r') as file:
        param = json.load(file)
        return param.get(param_name)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: <param_name>")
        sys.exit(1)
    param_name = sys.argv[1]

    print(get_param(param_name))
