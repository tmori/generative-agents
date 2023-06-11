#!/usr/bin/python
# -*- coding: utf-8 -*-

from plan import Plan
from prompt_template import PromptTemplate
from db_manager import get_qa

class TacticalPlanning:
    def __init__(self, plan: Plan, db_dir: str, summary_template_path: str):
        self.plan = plan
        self.db_dir = db_dir
        self.summary_template_path = summary_template_path

    def generate_question(self, prompt_templates):
        prioritized_plan = self._prioritize_plan()
        if (len(prioritized_plan) == 0):
            return None
        
        #print(prioritized_plan)
        row = prioritized_plan.head(1).iloc[0]
        #print(row)
        plan_id = row["PlanID"]
        self.plan.update_status_doing(plan_id)

        document_id = row["DocumentID"]
        purpose = row["Purpose"]
        perspectives = row["Perspectives"]

        return (plan_id, document_id, self._generate_document_question(prompt_templates, document_id, purpose, perspectives))

    def _prioritize_plan(self):
        plan_data = self.plan.get_data()
        prioritized_plan = plan_data.sort_values(by=["PlanID"], ascending=True)
        prioritized_plan = prioritized_plan.loc[prioritized_plan["Status"].isin(["Doing", "None"])]
        return prioritized_plan

    def _generate_document_question(self, prompt_template_path, document_id, purpose, perspectives):
        if document_id == "summary":
            prompt_query_template = PromptTemplate(self.summary_template_path)
            query = prompt_query_template.get_prompt(document_id=document_id, purpose=purpose, perspectives=perspectives)
            return query
        else:
            prompt_query_template = PromptTemplate(prompt_template_path)
            query = prompt_query_template.get_prompt(document_id=document_id, purpose=purpose, perspectives=perspectives)
            return query

if __name__ == "__main__":
    from query import Query
    from memory_stream import MemoryStream
    plan = Plan()
    plan.load_from_json("./test/plan.json")
    db_dir = "../tutorial_langchain/dbs"
    tactical_planning = TacticalPlanning(plan, db_dir, "./prompt_templates/ptemplate_subq_summary.txt")
    memory_stream = MemoryStream()

    while True:
        ret = tactical_planning.generate_question("./prompt_templates/ptemplate_subq_detail.txt")
        if ret == None:
            print("END")
            break
        plan_id = ret[0]
        doc_id = ret[1]
        question = ret[2]
        qa = get_qa(db_dir, doc_id)
        prompt_template_path = "./prompt_templates/ptemplate_query.txt"
        query = Query(doc_id, question, memory_stream, qa)
        memory_id = query.run(prompt_template_path, question)
        if memory_id < 0:
            plan.update_status_done(plan_id, memory_id)
            continue
        print("REPLY: " + memory_stream.get_reply())
        print("POINT: " + str(memory_stream.get_point()))
        memory_stream.save_to_json("test/memory.json")

        plan.update_status_done(plan_id, memory_id)
        plan.save_to_json("./test/updated_plan.json")

