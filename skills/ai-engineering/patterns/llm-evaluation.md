# AI Engineering — LLM Evaluation Patterns

## Correctness Metrics

```python
CORRECTNESS_METRICS = {
    'exact_match': {
        'use_case':    'Factual QA, code generation',
        'calculation': 'output == expected',
    },
    'f1_score': {
        'use_case':    'Extractive QA, summarization',
        'calculation': '2 * (precision * recall) / (precision + recall)',
    },
    'semantic_similarity': {
        'use_case':  'Open-ended QA, chatbots',
        'model':     'all-MiniLM-L6-v2',
        'threshold': 0.8,
    },
    'rubric_based': {
        'use_case': 'Complex tasks (analysis, writing)',
        'rubric': {
            'correctness':  'Is the answer factually accurate?',
            'completeness': 'Does it address all parts of the question?',
            'clarity':      'Is the answer easy to understand?',
            'conciseness':  'Is the answer appropriately brief?',
        },
    }
}
```

## Hallucination Detection

```python
HALLUCINATION_DETECTION = {
    'methods': {
        'fact_verification': {
            'process': [
                'Extract atomic claims from output',
                'Search knowledge base for each claim',
                'Flag claims with no supporting evidence',
            ],
            'threshold': 'Any unsupported claim = hallucination',
        },
        'self_consistency': {
            'process': [
                'Generate N outputs for same input (temperature > 0)',
                'Extract key claims from each',
                'Check claim agreement across samples',
            ],
            'threshold': '< 50% agreement = likely hallucination',
        },
        'uncertainty_calibration': {
            'process': [
                'Ask model for confidence score',
                'Bin by confidence level',
                'Check actual accuracy in each bin',
            ],
        },
    }
}
```

## Latency / Cost Tracking

```python
LATENCY_COST_TRACKING = {
    'latency_metrics': {
        'time_to_first_token': 'Latency before streaming starts',
        'generation_time':     'Time to generate all tokens',
        'p50': 'Median',
        'p95': '95th percentile',
        'p99': 'Tail latency (critical for UX)',
    },
    'cost_metrics': {
        'input_tokens':      'Prompt tokens',
        'output_tokens':     'Completion tokens',
        'cost_per_request':  'Average cost per user request',
        'cost_per_correct':  'Cost / correct answers (efficiency)',
    },
    'budgets': {
        'p99_latency_ms':        5000,
        'cost_per_1k_requests':  10.00,
    },
    'optimization_strategies': {
        'prompt_compression':    'Remove unnecessary tokens',
        'caching':               'Cache responses for repeated queries',
        'model_routing':         'Route easy queries to cheaper models',
        'speculative_decoding':  'Draft small model, verify with large',
    }
}
```

## Human Preference Evaluation

```python
HUMAN_PREF_EVAL = {
    'setup': {
        'comparison_type':  'blind',
        'evaluator_count':  3,
    },
    'sampling': {
        'samples_total': 100,
        'diversity':     'Cover all query categories',
        'edge_cases':    'Include known failure modes',
    },
    'question': 'Which response is more helpful and accurate?',
    'options': ['A significantly better', 'A slightly better', 'Tie', 'B slightly better', 'B significantly better'],
    'analysis': {
        'win_rate':           '(A wins + 0.5 * ties) / total',
        'statistical_test':   'binomial test against 0.5',
        'significance_level': 0.05,
    },
    'decision_rule': 'Adopt A if win_rate > 0.55 with p < 0.05',
}
```
