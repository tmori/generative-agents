#!/usr/bin/python
# -*- coding: utf-8 -*-

from document_db import load_db_with_type

def get_qa(db_dir: str, doc_id: str):
    return load_db_with_type(db_dir + "/" + doc_id)
