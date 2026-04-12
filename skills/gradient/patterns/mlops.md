# ML Engineering — MLOps Patterns

## Model Versioning Config

```python
MODEL_VERSIONING = {
    'format': 'semver',
    'tracking': 'mlflow',
    'metadata_per_version': {
        'git_commit': 'required',
        'data_version': 'required',
        'training_config': 'required',
        'metrics': {
            'train_accuracy': 'required',
            'validation_accuracy': 'required',
            'test_accuracy': 'required',
        },
        'artifacts': ['model_weights', 'preprocessor', 'inference_config'],
    }
}
```

## A/B Test Config

```python
AB_TEST_CONFIG = {
    'variants': {
        'control':   {'model_version': '1.0.0', 'traffic_split': 0.5},
        'treatment': {'model_version': '2.0.0', 'traffic_split': 0.5},
    },
    'metrics': {
        'primary':  'conversion_rate',
        'guardrail': ['latency_p99', 'error_rate'],
    },
    'stopping_criteria': {
        'min_sample_size': 10000,
        'min_duration_days': 7,
        'significance_level': 0.05,
    },
    'rollback_triggers': {
        'metric_degradation': 0.05,
        'error_rate_increase': 0.01,
        'latency_increase': 0.50,
    }
}
```

## Drift Monitoring Config

```python
DRIFT_MONITORING = {
    'data_drift': {
        'method': 'psi',        # Population Stability Index
        'threshold': 0.1,       # PSI > 0.1 = significant drift
        'window': '1 day',
        'alert_channel': 'slack-ml-alerts',
    },
    'concept_drift': {
        'metric': 'prediction_accuracy',
        'method': 'cusum',
        'threshold': 5.0,
        'window': '1 week',
    },
}

ROLLBACK_CONFIG = {
    'automatic_rollback': True,
    'triggers': [
        {'name': 'accuracy_drop',  'condition': 'validation_accuracy < baseline - 0.05'},
        {'name': 'latency_spike',  'condition': 'p99_latency > budget * 2'},
        {'name': 'error_spike',    'condition': 'error_rate > 0.05'},
        {'name': 'drift_detected', 'condition': 'psi_score > 0.25'},
    ],
    'rollback_to': 'previous_stable_version',
    'notify': ['ml-team-slack', 'oncall-pager'],
}
```
