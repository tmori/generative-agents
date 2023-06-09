#!/usr/bin/python
# -*- coding: utf-8 -*-

from plan import Plan
from db_manager import get_qa
from prompt_template import PromptTemplate

class TacticalPlanning:
    def __init__(self, plan: Plan, db_dir: str, summary_template_path: str):
        self.plan = plan
        self.db_dir = db_dir
        self.summary_template_path = summary_template_path

    def generate_question(self, prompt_templates):
        prioritized_plan = self._prioritize_plan()
        if (len(prioritized_plan) == 0):
            return None
        
        row = prioritized_plan.head(1)
        plan_id = row["PlanID"][0]
        self.plan.update_status_doing(plan_id)

        document_id = row["DocumentID"][0]
        purpose = row["InvestigationPurpose"][0]
        perspectives = row["InvestigationPerspectives"][0]

        return (row["PlanID"][0], document_id, self._generate_document_question(prompt_templates, document_id, purpose, perspectives))

    def _prioritize_plan(self):
        plan_data = self.plan.get_data()
        prioritized_plan = plan_data.sort_values(by=["PlanID"], ascending=True)
        prioritized_plan = prioritized_plan.loc[prioritized_plan["InvestigationStatus"].isin(["Doing", "None"])]
        return prioritized_plan

    def _generate_document_question(self, prompt_template_path, document_id, purpose, perspectives):
        if document_id == "summary":
            prompt_query_template = PromptTemplate(self.summary_template_path)
            query = prompt_query_template.get_prompt(document_id=document_id, purpose=purpose, perspectives=perspectives)
            return query
        else:
            qa = get_qa(self.db_dir, document_id)
            prompt_query_template = PromptTemplate(prompt_template_path)
            query = prompt_query_template.get_prompt(document_id=document_id, purpose=purpose, perspectives=perspectives)
            print({"question": query})
            reply = qa({"question": query})
            return reply["answer"]

if __name__ == "__main__":
    from query import Query
    from memory_stream import MemoryStream
    plan = Plan()
    plan.load_from_json("./test/plan.json")
    db_dir = "../tutorial_langchain/dbs"
    tactical_planning = TacticalPlanning(plan, db_dir, "./prompt_templates/ptemplate_subq_summary.txt")

    ret = tactical_planning.generate_question("./prompt_templates/ptemplate_subq_detail.txt")

    plan_id = ret[0]
    doc_id = ret[1]
    question = ret[2]
    qa = get_qa(db_dir, doc_id)
    memory_stream = MemoryStream()
    prompt_template_path = "./prompt_templates/ptemplate_query.txt"
    query = Query(doc_id, question, memory_stream, qa)
    memory_id = query.run(prompt_template_path, question)
    print("REPLY: " + memory_stream.get_reply())
    print("POINT: " + str(memory_stream.get_point()))
    memory_stream.save_to_json("test/memory.json")

    plan.update_status_done(plan_id, memory_id)
    plan.save_to_json("./test/updated_plan.json")

