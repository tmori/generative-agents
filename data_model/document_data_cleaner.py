#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import traceback
from data_model_accessor import DataModelAccessor
from document_data_model import DocumentDataModel
from document_contents_similarity_merge import merge_and_save_known_infos_json

class DocumentDataCleaner:
    def __init__(self, accessor: DataModelAccessor):
        self.accessor = accessor

    def clean_empty_data_models(self):
        clean_names = []
        for name in self.accessor.get_filelist():
            filepath = self.accessor.get_data_model_filepath(name)
            model = DocumentDataModel.load_json_file(filepath)
            data_model = model.get_model()
            if data_model.is_empty_content() == True:
                print(f"INFO: REMOVING EMPTY MODEL({data_model.get_name()})")
                clean_names.append(name)
        self.accessor.remove_models(clean_names)

    def merge_same_data_models(self):
        for name in self.accessor.get_filelist():
            print("INFO: name=", name)
            filepath = self.accessor.get_data_model_filepath(name)
            ret = merge_and_save_known_infos_json(filepath)
            if ret == False:
                print("INFO: skip merge...error")
                #sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: <dir>")
        sys.exit(1)
    dir = sys.argv[1]
    accessor = DataModelAccessor(dir)

    cleaner = DocumentDataCleaner(accessor)
    cleaner.clean_empty_data_models()
    print("INFO: MERGING REFLECTIONS")
    cleaner.merge_same_data_models()
    