# generative-agents
Experimenting with an agent that searches documents and asks questions repeatedly in response to the main question, automatically determining the optimal answer from the current documents or recognizing when there is no answer.

# Assumed environment, etc

* Operating environment
  * Windows10/11 WSL2, Ubuntu, Mac
* Install
  * Python 3 can be used
* OpenAI
  * OpenAPI key can be used

# What you can do

* You can input multiple existing documents
* You can ask questions about the documents you input
* It speculates questions from various angles, reads the necessary documents, and provides answers

## Types of supported documents

LangChain has loaders that support various documents, but as of now, it can load the following documents.

* PDF
* CSV
* PPTX
* URL
* JSON

# Install

Please install the following

```
pip3 install openai
pip3 install chromadb 
pip3 install tiktoken
pip3 install pypdf
pip3 install langchain
pip3 install unstructured
pip3 install tabulate
```

Please set the OpenAPI API key as an environment variable.

```
export OPENAI_API_KEY=<APIキー>
```

Clone the repository

```
git clone https://github.com/tmori/generative-agents.git
```

# Place the existing documents

Please create a `documents` directory on the same directory level as `generative-agents`.

```
mkdir documents
```

```
$ ls
documents generative-agents
```

Then, create the following two directories under `documents`.

```
mkdir documents/docs
mkdir documents/dbs
```

Please place the PDF files you want to load under `documents/docs`.
Placement example: PDFs of my own Qiita article

```
ls documents/docs/
'ChatGPTのAPI使って、Unity上の箱庭ロボットを動かしてみた！ - Qiita.pdf'
'Mac＋Unity＋Pythonで箱庭ロボットを強化学習できるようにするための手順書 - Qiita.pdf'
'Python使ってUnity上の箱庭ロボットのカメラデータを取得してみよう - Qiita.pdf'
'Ubuntuでも箱庭で機械学習するやつを動かそう - Qiita.pdf'
'Unity + Python + 箱庭でロボットを強化学習させてみよう！ - Qiita.pdf'
'Unity 内の箱庭ロボットを動かすPython API仕様書 - Qiita.pdf'
'Unity＋Python＋箱庭で自作ドローンを動かしてみる！ - Qiita.pdf'
'Windows＋Unity＋Pythonで箱庭ロボットを強化学習できるようにするための手順書 - Qiita.pdf'
```

After completing the placement, please execute the following command.


```
bash generative-agents/tools/create_doclist.bash 
```

If successful, logs like this will be output.

```
DB_DIR =tmp/DB
DOC_DIR=tmp
INFO: Loading document=ChatGPTのAPI使って、Unity上の箱庭ロボットを動かしてみた！ - Qiita.pdf
INFO: Storing Vector DB:tmp/DB
:
DB_DIR =tmp/DB
DOC_DIR=tmp
INFO: Loading document=Windows＋Unity＋Pythonで箱庭ロボットを強化学習できるようにするための手順書 - Qiita.pdf
INFO: Storing Vector DB:tmp/DB
```

# To ask a question

The way to ask questions to the document is as follows.

```
bash tools/query.bash "<Question content>"
```

Please note that the response from OpenAPI is slow, so it may take a few minutes for the answer to appear. For difficult questions, it's worth the wait, but for simpler ones, it's better to ask questions to individual documents.

## Note
Please note that the answers to questions will be in Japanese. If you want the answer in English, please remove `in Japanease` from the prompt in the following file.

https://github.com/tmori/generative-agents/blob/36a528b56c4fd64f01fc9cd2807268dc1431d73d/prompt_templates/ptemplate_evaluate.txt#L13

# Demo

Let's ask a question about the sandbox right away.

```
bash tools/query.bash "Windows版の箱庭上でロボットを強化学習させようとしていますが、シミュレーション開始してもロボットが動きません。手順、ファイアウォール、設定等、考えられる原因を教えてください"
```

Question:
> I'm trying to train a robot using reinforcement learning on the Windows version of Hakoniwa (a simulator for robotics), but the robot doesn't move even after starting the simulation. Can you please provide me with the possible causes, such as steps, firewall, settings, or any other considerations?

Answer:
> Several reasons could cause your robot to not move in the Hakoniwa simulator.
> 1. Firewall Settings: One of the important things to check, as mentioned in the document "ReinforcementLearning-RobotSimulation-WindowsUnityPython-SetupGuide-UnityVersionCompatibility", is to ensure that the Unity Editor is allowed through your Windows Defender Firewall. If the Unity Editor is blocked, you need to alter the settings and allow it. It won't function properly if it's not checked in the "Allowed apps and features" section.
> 2. Unity Editor Settings: The Unity Editor settings must be correctly configured as per the guidelines provided in document "Programming-Unity-Python-DroneControl-HakoniwaEnvironment". It covers the step-by-step setup of the Hakoniwa simulator environment in Unity and Python. 
> 3. Reinforcement Learning Algorithm Implementation: These issues could also emerge from incorrect implementation of your reinforcement learning algorithm as detailed in "Unity-Python-Robotics-ReinforcementLearning-Implementation". It explains how the interaction between the Unity simulator and Python scripts operates and how to devise a reward system, observe the state, execute the robot's motor operations, and handle the number of observed states and actions.
> 4. Python Scripting and Module Usage: If there are errors in Python scripting or incorrect use of the Python API modules (hako_env, hako_robomodel_any, and hako modules) for controlling robots in Unity, as per the "Unity-PythonAPI-RobotControl-hako_env-hako_robomodel_any-hako" document, they might inhibit the robot's behavior in the simulation.
> Please cross-verify each of these aspects to identify and resolve the issue.


# Design information

## Tool chain for creating document TITLE and DB

![image](https://github.com/tmori/generative-agents/assets/164193/b0e200b6-a178-4d08-afb9-6d7d7c3088a1)

## Architecture

![image](https://github.com/tmori/generative-agents/assets/164193/da5d59f2-15c9-4d95-bc4c-dac31523e105)


### Reflection Process

![image](https://github.com/tmori/generative-agents/assets/164193/4af2583f-aa1f-4bf1-bd30-902ba24a9c12)


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


### Knowledge/Concept
The output data of Reflection consists of the following two components:

- Knowledge (Needs)
  - refers to the necessary knowledge/concepts required to answer the question.
- Knowledge (Definition)
  - represents the understanding of that knowledge/concept.

## refs
* https://arxiv.org/abs/2304.03442
