# AI Engineering — Agent Design Patterns

## ReAct (Reason + Act)

```python
REACT_AGENT = {
    'pattern': 'Thought → Action → Observation → Thought → ... → Answer',
    'prompt_template': '''
Answer the following question. You can use these tools: {tools}

Format:
Question: the input question
Thought: what to do
Action: the action to take (one of [{tool_names}])
Action Input: input to the action
Observation: result of the action
... (repeat as needed)
Thought: I now know the final answer
Final Answer: the answer

Question: {input}
{agent_scratchpad}
''',
    'max_iterations': 10,
    'early_stopping': 'force',
}
```

## Plan-and-Execute

```python
PLAN_EXECUTE_AGENT = {
    'architecture': {
        'planner':     'LLM that generates multi-step plan',
        'executor':    'LLM that executes one step at a time',
        'synthesizer': 'LLM that combines results into final answer',
    },
    'planner_prompt': '''
Break this task into steps:
Task: {task}

Provide numbered steps. Each step must be:
1. Executable by a single tool call
2. Independent (no dependencies on future steps)
3. Have clear success criteria
''',
    'executor_prompt': '''
Execute this step:
Step: {step}
Available tools: {tools}
Action: <tool>
Action Input: <input>
''',
    'max_plans': 5,
    'adaptive_replanning': True,
}
```

## Reflection / Self-Correction

```python
REFLECTION_AGENT = {
    'pattern': 'Generate → Critique → Revise → Output',
    'critic_prompt': '''
Review this response for errors:
Query: {query}
Response: {response}

Check for: factual errors, logical inconsistencies, missing info, unclear reasoning.
List issues (or "No issues"):
''',
    'reviser_prompt': '''
Revise to fix identified issues:
Original: {response}
Issues: {critique}
Revised:
''',
    'max_reflection_cycles': 3,
    'stop_on_no_issues': True,
}
```

## Multi-Agent Debate

```python
DEBATE_AGENT = {
    'architecture': {
        'proponent': 'Argues for initial answer',
        'opponent':  'Finds flaws and counterarguments',
        'judge':     'Evaluates arguments and selects winner',
    },
    'debate_rounds': 3,
    'opponent_prompt': '''
Find flaws in this argument:
Answer: {answer}
Argument: {proponent_argument}

Identify: logical fallacies, unsupported claims, alternative explanations, gaps.
''',
    'judge_prompt': '''
Evaluate:
Proponent: {proponent_argument}
Opponent: {opponent_argument}

Which is more convincing? What is the correct answer?
''',
}
```

## Tool Routing

```python
TOOL_ROUTING = {
    'routing_methods': {
        'prompt_based': {
            'prompt': 'Given: {task}, which tool is best? Options: {tool_descriptions}',
            'model': 'fast_llm',
        },
        'embedding_based': {
            'method': 'Encode task + tool descriptions, find nearest neighbor',
            'embedding_model': 'all-MiniLM-L6-v2',
        },
        'fine_tuned': {
            'model': 'tool_classifier_v1',
            'accuracy': 0.94,
        },
    },
    'fallback': 'Ask user for clarification if confidence < 0.7',
}
```
