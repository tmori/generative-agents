# generative-agents
Experimenting with an agent that searches documents and asks questions repeatedly in response to the main question, automatically determining the optimal answer from the current documents or recognizing when there is no answer.

## Architecture

![image](https://github.com/tmori/generative-agents/assets/164193/2274d26e-0145-41d1-9c07-267f19109b42)


Referring to the generative agent mentioned in the reference document.

## Actions
### Planner

### Tactical Planning
The purpose of `TacticalPlanning` is to refer to all the information in the Plan and create detailed sub-questions for the target document.

The procedure is as follows:
1. Refer to the information in the `Plan` and select the highest priority (with the smallest PlanID) among the ones that are not investigated or under investigation. (In the case of both being under investigation or not investigated, the one under investigation takes priority.)
2. Refer to the purpose and perspectives of the target document in the investigation data and create matching questions.
3. Repeat step 2 for each target document.
4. Output the target documents and questions as a list.

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

## refs
* https://arxiv.org/abs/2304.03442
