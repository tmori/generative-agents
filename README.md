# generative-agents
Experimenting with an agent that searches documents and asks questions repeatedly in response to the main question, automatically determining the optimal answer from the current documents or recognizing when there is no answer.

Architecture
![image](https://github.com/tmori/generative-agents/assets/164193/7beda2b2-a3ed-4f1f-af08-ab3ae578da74)

Referring to the generative agent mentioned in the reference document.

## Actions
### Plan

### Thought

### Query
Query examines the target document based on the inputs of TargetDocumentId, SubQuestion, and PromptQueryTemplate. It evaluates the answer result by determining the relevance and importance between the MainQuestion and SubQuestion, assigning a score between 0 and 100. It then stores this sequence of information in the MemoryStream.

### Reflection

### History Selector
The HistorySelector class allows selecting data from a MemoryStream based on a specified threshold. It has the following methods:

- `__init__(self, memory_stream)`: Initializes the HistorySelector object with a MemoryStream instance provided as memory_stream.
- `select(self, threshold)`: Selects data from the MemoryStream based on the given threshold. It retrieves data with points greater than or equal to the threshold and stores it in self.history. It returns the selected data.
- `get_history(self)`: Returns the stored history data that has been previously selected.

This class facilitates the selection of data from a MemoryStream instance based on a threshold and provides access to the selected data and the stored history.

## Managed Data

### Plan

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
