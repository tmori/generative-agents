# generative-agents
Experimenting with an agent that searches documents and asks questions repeatedly in response to the main question, automatically determining the optimal answer from the current documents or recognizing when there is no answer.

## Tool chain for creating document TITLE and DB

![image](https://github.com/tmori/generative-agents/assets/164193/b0e200b6-a178-4d08-afb9-6d7d7c3088a1)

## Architecture

![image](https://github.com/tmori/generative-agents/assets/164193/da5d59f2-15c9-4d95-bc4c-dac31523e105)


### Reflection Process

![image](https://github.com/tmori/generative-agents/assets/164193/14acc921-0e0a-433a-9fef-be3e298ab772)


Referring to the generative agent mentioned in the reference document.

## Actions
### Evaluator
The Evaluator integrates and evaluates the results of the execution of the plan to create an answer to the MainQuestion.

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


### Query
Query examines the target document based on the inputs of TargetDocumentId, SubQuestion, and PromptQueryTemplate. It evaluates the answer result by determining the relevance and importance between the MainQuestion and SubQuestion, assigning a score between 0 and 100. It then stores this sequence of information in the MemoryStream.

### Reflection
Reflection is the process of extracting the necessary knowledge/concepts to answer a question and defining the definitions and relationships of knowledge/concepts based on the results executed by the Planner.

### History Selector
The HistorySelector class allows selecting data from a MemoryStream based on a specified threshold. 

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

### Knowledge/Concept
The output data of Reflection consists of the following two components:

- Knowledge (Needs)
  - refers to the necessary knowledge/concepts required to answer the question.
- Knowledge (Definition)
  - represents the understanding of that knowledge/concept.

## refs
* https://arxiv.org/abs/2304.03442
