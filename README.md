# generative-agents
There are 3 Plans to answer the question for multiple documents using LLM.

In this repository, we are experimenting Plan C using generative-agents.

* Plan A
  * Merging all documents and querying
* Plan B
  * Querying each document individually
* Plan C
  * Extracting "knowledge/concepts" for answering, understanding and extracting that knowledge/concepts as reflection data, and combining it with planning data to generate answers

A discussion of the three proposals follows.

## Plan A: Merging all documents and querying
- Pros:
    1. Since the documents are not divided, there is no risk of information loss.
- Cons:
    1. There is a limit on the number of tokens for the OpenAI API, which can impose an upper limit on the amount of data that can be sent, potentially leading to information loss.

## Plan B: Querying each document individually
- Pros:
    1. Since the documents are divided into meaningful units, if the appropriate document can be identified for the question, the optimal answer can be expected.
- Cons:
    1. Time cost of querying all documents.
    2. Difficulties in constructing answers based on information spanning multiple documents.

## Plan C: Extracting "knowledge/concepts" for answering, understanding and extracting that knowledge/concepts as reflection data, and combining it with planning data to generate answers
- Pros:
    1. It allows focusing on specific knowledge or concepts relevant to the context, enabling concentration on the necessary information while filtering out irrelevant information.
    2. Extracting knowledge or concepts is a good method for gathering information from multiple documents and achieving an integrated understanding, enabling a cross-document perspective.
    3. It enables a deeper understanding of the question's intent and generation of answers based on that understanding, particularly useful for complex questions that require understanding of related information across multiple documents.
- Cons:
    1. Extracting and understanding knowledge or concepts require time and computational resources, so the execution time may be longer compared to other methods.
    2. Integrating information extracted from multiple documents to generate reflection data may require more advanced natural language processing techniques and tools, potentially increasing the implementation difficulty.
    3. Furthermore, extracting and interpreting concepts or knowledge requires careful tuning and optimization to ensure appropriate precision and recall. This becomes prominent, especially when the text contains ambiguous expressions or a large number of domain-specific terms and jargon.

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
bash tools/query.bash "I'm trying to train a robot using reinforcement learning on the Windows version of Hakoniwa (a simulator for robotics), but the robot doesn't move even after starting the simulation. Can you please provide me with the possible causes, such as steps, firewall, settings, or any other considerations?"
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

## Reflection Diagram

I believe that this response largely relies on reflection. As shown in the diagram below, the knowledge (Term) necessary for the question is extracted, and the relationships between these Terms are recognized. Furthermore, these Terms are linked with the documents under investigation, and by examining various documents, it becomes clear that the answers are obtained.

![image](https://github.com/tmori/generative-agents/assets/164193/314aa4a9-1bae-4025-8826-ce9aeba6fccc)

The above diagram is base on following reflection data:

https://github.com/tmori/generative-agents/blob/main/query_dir/q_2/result/reflection.json

## Comparison

Let's compare it to plan A using LangChain [custom agent](https://github.com/tmori/langchain_tutorial/blob/develop/agent_custom_jp.py).

Answer:
> If your Hakoniwa reinforcement learning robot doesn't move, there could be a few reasons for this issue. Here are some steps you can take to troubleshoot the problem:
> 1. Make sure you have properly installed and set up the required tools and environments. Follow the instructions provided in the Qiita article for Mac or Windows.
> 2. Check if your Python reinforcement learning program is running correctly. Ensure that the Q-table is being updated and the robot is receiving appropriate actions based on the current state.
> 3. Verify that the motor operations are correctly implemented in the Python program. The robot should have three basic operations: move forward (with two-speed levels), turn right (with two-speed levels), and turn left (with two-speed levels).
> 4. Make sure the reward and observation functions are working as expected. The ultrasonic sensor should return values between 0 and 255, and the robot should receive a reward based on these values.
> 5. If you have made any changes to the sample program, double-check your modifications to ensure they are not causing the issue.
>
> If you have followed these steps and the robot still doesn't move, there might be an issue with the specific implementation or a bug in the code. You can try reaching out to the Hakoniwa community for further assistance.

We evaluates theses answers with using OpenAI API.
The Prompt is here:

```
For the Question {MainQuestion}, there are 2 answers.

Answer1: {Result1}
Answer2: {Result2}

Please assess the appropriateness of the answer in Japanease
to each questions by assigning a score between 0 and 100 in the following format 
0-20 points: No information at all is provided about the question.
21-40 points: Basic information about the question is available, but key details are missing.
41-60 points: Information about the question is available, but some important details are missing.
61-80 points: The information about the question is quite detailed, but some details are missing.
81-100 points: The information about the question is very detailed and includes all necessary information.

Let's think step by step.

Answer1's Point: <Answer1 Point>
The Point Reason: <Reason>

Answer2's Point: <Answer2 Point>
The Point Reason: <Reason>
```

Results:

> Plan A's Point: 85
>
> The Point Reason: The answer provides a structured and detailed approach to troubleshoot the issue of the robot not moving in Hakoniwa simulation. It gives a list of steps with reasons that connect directly to the problem, but it does not mention considerations about the Firewall settings, unity editor settings, and details about the python modules.

> Plan C's Point: 100
>
> The Point Reason: This response thoroughly details multiple potential causes for the issue, including Firewall settings, Unity Editor settings, Reinforcement Learning Algorithm Implementation, and Python scripting. It refers to the necessary and detailed part of the Hakoniwa documentations, making it a comprehensive answer.

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

```json
{
  "DetailedStrategy": "<DetailedStrategy>",
    "Plan": [
      {
        "PlanID": "<PlanID>",
        "DocumentID": "<DocumentID>",
        "Purpose": "<Purpose>",
        "Perspectives": "<Perspectives>",
        "ResultID": "<ResultID>"
        "Status": "<Status>"
      }
    ]
}
```

* DetailedStrategy
  * a strategy for investigating multiple documents to answer the main question.
* Plan
  * PlanID
    * plan id
  * DocumentID
    * target document to be investigated
  * Purpose
    * purpose of investigation for the target document ID
  * Perspectives
    * perspectives of investigation for the target document ID
  * ResultID
    * result ID(=MemoryStream ID)
  * Status
    * status of investigation(None, Doing, Done)

Example:

```json
{
    "DetailedStrategy": "  Investigate possible causes like software steps, settings, firewall, and other factors,",
    "Plan": [
        {
            "PlanID": 1,
            "DocumentID": "ReinforcementLearning-RobotSimulation-WindowsUnityPython-SetupGuide-UnityVersionCompatibility",
            "Purpose": "Investigate steps and system requirements for the Windows version of simulator",
            "Perspectives": "Technical, Practical",
            "ResultID": "",
            "Status": "None"
        },
    ]
}
```

### MemoryStream
MemoryStream manages all memories related to the questions and answers during mission execution.
It is a collection of data sets, with each set consisting of the following information:

```json
[
    {
        "ID": "<ID>",
        "TargetDocID": "<TargetDocID>",
        "Question": "<Question>",
        "Reply": "<Reply>",
        "Point": "<Point>"
    }
]
```

* ID
  * memory id
* TargetDocID
  * target document
* Question
  * question for the target document
* Reply
  * answer for the question
* Point
  * importance of the answer. The importance degree depends on GPT's subjectives.

Example:

```json
[
    {
        "ID": 1,
        "TargetDocID": "ReinforcementLearning-RobotSimulation-WindowsUnityPython-SetupGuide-UnityVersionCompatibility",
        "Question": "Please obtain information based on the following purposes and perspectives.\nLet's think step by step.\n\npurpose: Investigate steps and system requirements for the Windows version of simulator\nperspectives: Technical, Practical\n",
        "Reply": "Answer: The steps and system requirements for setting up a sandbox robot simulator using Windows, Unity, and Python are outlined in the provided Qiita articles. \n\n1. Unity Editor should be allowed through the Windows Defender Firewall. If it's not checked in the \"Allowed apps and features\" section, it's blocked. You need to change the settings and check it.\n\n2. Check the incoming rules. If Unity Editor is grayed out, it's blocked. You need to display the properties and allow it.\n\n3. In the Unity Editor, select 'Assets/Scenes/Transport' in the 'Project View' at the bottom left of the screen. If the course is displayed as in the image, it's successful. \n\n4. Click the play button in the Unity Editor. If successful, a robot will appear as shown in the image.\n\nThe technical perspective involves setting up the firewall and Unity Editor settings. The practical perspective involves running the simulation and observing the robot's behavior.\n\nPoint: 85",
        "Point": 85.0
    },
]
```

### Knowledge/Concept
The output data of Reflection consists of the following two components:

* Knowledge (Needs)
* Knowledge (Definition)

#### Knowledge (Needs)
refers to the necessary knowledge/concepts required to answer the question.

```json
{
  "Knowledges": [
    {
      "Term": "<Term>",
      "Reason": "<Reason>"
    },
  ]
}
```

* Term
  * a term which is necessary knowledge/concepts required to answer the question.
* Reason
  * the reason of picking up the Term for answering question.

Example:
```json
    {
      "Term": "Reinforcement Learning",
      "Reason": "You should understand basics of reinforcement learning as this is the method being used to train the robot in question. It will help you understand how the system works and how to properly implement it."
    },
    {
      "Term": "Hakoniwa Simulator",
      "Reason": "This is the specific tool the user is trying to use. Knowledge of its working, settings and system requirements is necessary to solve the issue."
    }
```

#### Knowledge (Definition)
represents the understanding of that knowledge/concept.

```json
{
  "Knowledges": [
    {
      "Term": "<Term>",
      "Reason": "<Reason>"
      "KnownInfos": [
         {
           "KnownInfo": "<KnownInfo>",
           "Point": "<Point>",
           "DocumentIDs": [ "<DocumentID>" ]
         },
      ],
      "UnknownInfo": [ "<UnknownInfo>" ],
      "Relations": [
         {
            "Term": "<Term>",
            "RelationReason": "<RelationReason>"
         },
      ]
    },
  ]
}
```
* KnownInfos
  * KnownInfo
    * acuquired information after investigating the documents which are shown in `DocumentIDs`.
  * Point
    * importance of KnownInfo for answering the main question. The importance degree depends on GPT's subjectives.
  * DocumentID
    * see KnownInfo
* UnknownInfo
  * unknown infromation of the Term which shoud be investigated for answering question.
* Relations
  * Term
    * the related Terms
  * RelationReason
    * the reason of having relationship with the Term

Example:

```json
    {
      "Term": "Reinforcement Learning",
      "Reason": "You should understand basics of reinforcement learning as this is the method being used to train the robot in question. It will help you understand how the system works and how to properly implement it.",
      "KnownInfos": [
        {
          "KnownInfo": "The implementation of reinforcement learning involves using Unity, Python, and a sandbox environment to train a robot. The robot model used is the same as the ET Robocon competition robot, which is capable of carrying goods. The robot uses an ultrasonic sensor that returns values between 0 and 255. When the robot is on a line trace, the value is around 120. The reinforcement learning process involves several components: Reward, State, Action, Number of states and actions.",
          "Point": "85",
          "DocumentIDs": [ "Unity-Python-Robotics-ReinforcementLearning-Implementation" ]
        }
      ],
      "UnknownInfo": [ "The specific reinforcement learning algorithm used and its configuration settings." ],
      "Relations": []
    },
    {
      "Term": "Hakoniwa Simulator",
      "Reason": "This is the specific tool the user is trying to use. Knowledge of its working, settings and system requirements is necessary to solve the issue.",
      "KnownInfos": [
        {
          "KnownInfo": "The Hakoniwa simulator environment is set up in Unity, and it also has settings such as drone movement and camera data retrieval that can be controlled using Python.",
          "Point": "87.5",
          "DocumentIDs": [ "Programming-Unity-Python-DroneControl-HakoniwaEnvironment", "Python-Unity-SandboxRobot-CameraData-Retrieval" ]
        }
      ],
      "UnknownInfo": [ "How to troubleshoot issues with Hakoniwa on Windows." ],
      "Relations": [
        {
          "Term": "Windows OS",
          "RelationReason": "Hakoniwa runs on the Windows OS and understanding how these two interact can help troubleshoot the issue."
        }
      ]
    },
```


## refs
* https://arxiv.org/abs/2304.03442
