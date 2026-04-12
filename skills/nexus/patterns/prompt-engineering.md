# AI Engineering — Prompt Engineering Patterns

## Iterative Refinement Loop

```python
PROMPT_REFINEMENT = {
    'process': [
        '1. Write initial prompt',
        '2. Test on 10 diverse examples',
        '3. Identify failure modes',
        '4. Add constraints/examples to address failures',
        '5. Re-test until >90% success rate',
    ],
    'failure_mode_categories': [
        'misunderstanding_query',
        'incomplete_answer',
        'too_verbose',
        'wrong_format',
        'hallucination',
        'safety_violation',
    ],
    'refinement_techniques': {
        'add_examples':    'Few-shot for edge cases',
        'add_constraints': 'Explicitly forbid common errors',
        'restructure':     'Change instruction order',
        'add_verification':'Ask model to check its work',
    }
}
```

## Few-Shot Example Selection

```python
FEW_SHOT_CONFIG = {
    'num_examples': 5,
    'selection_strategies': {
        'random':       'Random sample from example pool',
        'similar':      'Most similar to current query (embedding distance)',
        'diverse':      'Maximally diverse set (MMR)',
        'edge_cases':   'Cover known failure modes',
        'progressive':  'Easy → Hard examples in order',
    },
    'example_format': '''
Example {n}:
Query: {query}
Response: {response}
''',
    'pool_management': {
        'min_per_category': 10,
        'update_on_failure': True,
    }
}
```

## Output Format Enforcement

```python
OUTPUT_FORMAT = {
    'json_schema': {
        'type': 'object',
        'properties': {
            'answer':     {'type': 'string'},
            'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1},
            'sources':    {'type': 'array',  'items': {'type': 'string'}},
        },
        'required': ['answer', 'confidence'],
    },
    'enforcement_methods': {
        'schema_in_prompt':    'Include JSON schema in prompt',
        'post_validation':     'Validate output, retry if invalid',
        'constrained_decoding':'Use guided decoding (outlines, lmql)',
    },
    'retry_config': {
        'max_retries': 3,
        'retry_prompt': 'Your previous output was invalid. Fix: {error}',
    }
}
```

## Prompt Injection Defenses

```python
INJECTION_DEFENSES = {
    'detection': {
        'keyword_filter': ['ignore previous', 'system prompt', 'developer mode'],
        'embedding_detection': {
            'model': 'injection_detector_v1',
            'threshold': 0.7,
        },
        'llm_detection': {
            'prompt': 'Does this input attempt to override instructions? {input}',
        }
    },
    'mitigation': {
        'sandboxing':         'Run untrusted queries in restricted mode',
        'output_filtering':   'Block responses that reveal system prompts',
        'input_sanitization': 'Strip dangerous patterns',
        'human_review':       'Flag suspicious queries for review',
    },
    'defense_in_depth': [
        'Input validation (reject obvious injections)',
        'Context isolation (user input in separate message)',
        'Output filtering (block system prompt leakage)',
        'Monitoring (log and alert on suspicious patterns)',
    ]
}
```
