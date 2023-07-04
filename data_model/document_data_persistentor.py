#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import traceback
from data_model_accessor import DataModelAccessor
from document_data_model import DocumentDataModel

class DocumentDataPersistentor:
    def __init__(self, accessor: DataModelAccessor):
        self.accessor = accessor

    def save_document_data(self):
        for model in self.models:
            data_model = model.get_model()
            self.accessor.add_data_model(data_model)

    def load_document_data(self, plan_data_path: str):
        try:
            with open(plan_data_path, "r") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            traceback_str = traceback.format_exc()
            error_message = f"ERROR: {str(e)}"
            print(traceback_str + error_message)
            return
        if json_data.get("Plan") is None:
            return
        
        document_ids = []
        for entry in json_data.get("Plan"):
            if entry.get("DocumentID") not in document_ids:
                #print("doc:", entry.get("DocumentID"))
                document_ids.append(entry.get("DocumentID"))

        self.models = []
        for entry in document_ids:
            model = DocumentDataModel.create_from_plans(entry, json_data)
            if model.is_empty() == False:
                self.models.append(model)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: <dir> <filepath>")
        sys.exit(1)
    dir = sys.argv[1]
    filepath = sys.argv[2]
    accessor = DataModelAccessor(dir)

    persistentor = DocumentDataPersistentor(accessor)
    persistentor.load_document_data(filepath)
    persistentor.save_document_data()
    