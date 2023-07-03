#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import traceback
from data_model_accessor import DataModelAccessor
from reflection_data_model import ReflectionDataModel

class ReflectionDataCleaner:
    def __init__(self, accessor: DataModelAccessor):
        self.accessor = accessor

    def clean_empty_data_models(self):
        clean_names = []
        for name in self.accessor.get_filelist():
            filepath = self.accessor.get_data_model_filepath(name)
            model = ReflectionDataModel.load_json_file(filepath)
            data_model = model.get_model()
            if data_model.is_empty_content() == True:
                print(f"INFO: REMOVING EMPTY MODEL({data_model.get_name()})")
                clean_names.append(name)
        self.accessor.remove_models(clean_names)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: <dir>")
        sys.exit(1)
    dir = sys.argv[1]
    accessor = DataModelAccessor(dir)

    cleaner = ReflectionDataCleaner(accessor)
    cleaner.clean_empty_data_models()
    