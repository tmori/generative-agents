# generative-agents
Experimenting with an agent that searches documents and asks questions repeatedly in response to the main question, automatically determining the optimal answer from the current documents or recognizing when there is no answer.

## Architecture

![image](https://github.com/tmori/generative-agents/assets/164193/2274d26e-0145-41d1-9c07-267f19109b42)


Referring to the generative agent mentioned in the reference document.

## Actions
### Planner
The purpose of the Planner is to generate investigation plans for a set of documents based on the given input data.

- Input data:
  - Main Question (natural language question)
  - Mission (natural language mission)
  - Strategy (natural language strategy)
  - Document list (list of documents in natural language)
  - History (history of questions and answers for target documents in natural language)

- Output data:
  - Plan (N plans)
    - Document ID (document ID in natural language)
    - Purpose (purpose of investigating the target document in natural language)
    - Perspectives (perspectives for investigating the target document in natural language)

### Tactical Planning
The objective of `TacticalPlanning` is to utilize the entirety of the information within the Plan to formulate comprehensive sub-questions for the designated document.

The procedure unfolds in the following manner:

1. Examine the Plan's information and prioritize the highest-ranking item based on the smallest PlanID, considering those that have not yet been investigated or are currently under investigation. (If both options are applicable, priority is given to the one under investigation.)
2. Consult the investigation data to ascertain the purpose and perspectives associated with the target document, and subsequently generate corresponding questions.
3. Iterate through Step 2 for each individual target document.
4. Compile the target documents and their respective questions into a cohesive list.

The `TacticalPlanning` class represents a tactical planning system. Here is the description of the class:

- `__init__(self, plan: Plan, db_dir: str, summary_template_path: str)`: 
  - This is the constructor of the class that initializes the `TacticalPlanning` object.
  - It takes three parameters:
    - `plan`: An instance of the `Plan` class that represents the plan data.
    - `db_dir`: A string that specifies the directory of the database.
    - `summary_template_path`: A string that specifies the path of the summary template.

- `generate_question(self, prompt_templates)`: 
  - This method generates a question based on the prioritized plan data.
  - It takes `prompt_templates` as a parameter, which represents the prompt templates for question generation.
  - It retrieves the prioritized plan data, selects the first plan, updates its status to "Doing", and extracts the necessary information such as `plan_id`, `document_id`, `purpose`, and `perspectives`.
  - It then generates a document-specific question using the appropriate prompt template and the extracted information.
  - The method returns a tuple `(plan_id, document_id, question)`.

- `_prioritize_plan(self)`: 
  - This is a private method that prioritizes the plan data based on the plan ID.
  - It retrieves the plan data, sorts it by the plan ID in ascending order, and selects plans with "Doing" or "None" status.
  - It returns the prioritized plan data.

- `_generate_document_question(self, prompt_template_path, document_id, purpose, perspectives)`: 
  - This is a private method that generates a document-specific question based on the provided document ID, purpose, and perspectives.
  - If the document ID is "summary", it uses the summary template to generate the question.
  - Otherwise, it uses the specified prompt template to generate the question.
  - The generated question is returned as a string.

This `TacticalPlanning` class represents a system for tactical planning. It has the ability to generate questions based on a prioritized plan, update the plan status, and generate document-specific questions using prompt templates. It serves as a component within a larger system or application that involves tactical planning and question generation based on plan data.

### Query
Query examines the target document based on the inputs of TargetDocumentId, SubQuestion, and PromptQueryTemplate. It evaluates the answer result by determining the relevance and importance between the MainQuestion and SubQuestion, assigning a score between 0 and 100. It then stores this sequence of information in the MemoryStream.

Here is the translation of the overview of the class:

The `Query` class retrieves information related to a specific document (`target_doc_id`) and a main question (`main_question`) and stores the data in a memory stream called `MemoryStream`. It also loads a database from the specified directory (`db_dir`) to prepare a QA system for answering questions.

The class has the following main methods:

- `__init__(self, target_doc_id: str, main_question: str, memory_stream: MemoryStream, db_dir: str)`:
  - This is the constructor of the class.
  - `target_doc_id` represents the ID of the target document.
  - `main_question` represents the main question.
  - `memory_stream` is a memory stream object used for storing data.
  - `db_dir` specifies the directory of the database.

- `run(self, prompt_template_path: str, sub_question: str)`:
  - This method takes a prompt template path and a sub-question as inputs, generates a question using the template and inputs, and sends it to the QA system.
  - `prompt_template_path` specifies the path of the prompt template.
  - `sub_question` specifies the sub-question.
  - It combines the prompt template with the inputs to generate a question, sends it to the QA system, and retrieves the answer.
  - It extracts the point (a numerical value) from the answer, saves the information in the `MemoryStream`, and returns `True` if the extraction is successful. If it fails, it prints an error message and returns `False`.

- `save(self, sub_question: str, reply: str, point: int)`:
  - This method is used to save information in the memory stream.
  - `sub_question` specifies the sub-question.
  - `reply` specifies the reply (answer).
  - `point` specifies the point (a numerical value).
  - It adds the specified information to the `MemoryStream`.

That concludes the overview of the `Query` class. This class is used to retrieve answers to main questions, store information with points in the `MemoryStream`.

### Reflection
(TODO)

### History Selector
The HistorySelector class allows selecting data from a MemoryStream based on a specified threshold. It has the following methods:

- `__init__(self, memory_stream)`: Initializes the HistorySelector object with a MemoryStream instance provided as memory_stream.
- `select(self, threshold)`: Selects data from the MemoryStream based on the given threshold. It retrieves data with points greater than or equal to the threshold and stores it in self.history. It returns the selected data.
- `get_history(self)`: Returns the stored history data that has been previously selected.

This class facilitates the selection of data from a MemoryStream instance based on a threshold and provides access to the selected data and the stored history.

## Managed Data

### Plan
Plan includes the following information in the order of investigation:

- PlanID
- Document ID to be investigated
- Purpose of investigation for the target document ID
- Perspectives of investigation for the target document ID
- The set of investigation result IDs (MemoryStream IDs)
- Status of investigation(None, Doing, Done)

### MemoryStream
MemoryStream manages all memories related to the questions and answers during mission execution.
It is a collection of data sets, with each set consisting of the following information:

- ID
- Target Document ID
- Question
- Reply
- Point

### History
History is a subset of MemoryStream. It consists of selections that have high points.

### Reflection
(TODO)

## refs
* https://arxiv.org/abs/2304.03442
