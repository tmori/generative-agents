# generative-agents
Experimenting with an agent that searches documents and asks questions repeatedly in response to the main question, automatically determining the optimal answer from the current documents or recognizing when there is no answer.

Architecture
![image](https://github.com/tmori/generative-agents/assets/164193/7beda2b2-a3ed-4f1f-af08-ab3ae578da74)

Referring to the generative agent mentioned in the reference document.

## Actions
### Plan

### Thought

### Query

### Reflection

### History Selection

## Managed Data

### Plan

### MemoryStream
MemoryStream manages all memories related to the questions and answers during mission execution.
It is a collection of data sets, with each set consisting of the following information:

- ID
- Target Document ID
- Question
- Reply

### History

### Reflection

## refs
* https://arxiv.org/abs/2304.03442
