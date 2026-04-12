# ML Engineering — Model Training Patterns

## Hyperparameter Search Config

```python
SEARCH_STRATEGY = {
    'method': 'bayesian',       # or 'grid', 'random', 'hyperband'
    'metric': 'validation_auc',
    'direction': 'maximize',
    'n_trials': 50,
    'timeout_hours': 24,
    'search_space': {
        'learning_rate': {'type': 'log_uniform', 'low': 1e-5, 'high': 1e-2},
        'num_layers':    {'type': 'categorical', 'choices': [2, 3, 4, 5]},
        'hidden_dim':    {'type': 'categorical', 'choices': [64, 128, 256, 512]},
        'dropout':       {'type': 'uniform',     'low': 0.0, 'high': 0.5},
        'batch_size':    {'type': 'categorical', 'choices': [32, 64, 128, 256]},
    },
    'pruning': {'enabled': True, 'method': 'median'},
}
```

## Early Stopping

```python
early_stopping = {
    'metric': 'validation_loss',
    'mode': 'min',
    'patience': 10,
    'min_delta': 1e-4,
    'restore_best_weights': True,
}

stopping_rules = [
    'max_epochs: 100',
    'max_runtime_hours: 24',
    'target_metric: validation_auc > 0.95',
    'convergence: gradient_norm < 1e-6',
]
```

## Checkpoint Strategy

```python
CHECKPOINT_CONFIG = {
    'save_every_n_epochs': 1,
    'keep_last_n': 5,
    'save_best_only': True,
    'monitor_metric': 'validation_auc',
    'save_dir': 'checkpoints/',
    'save_metadata': {
        'git_commit': True,
        'config_snapshot': True,
        'data_version': True,
        'training_metrics': True,
    }
}
```

## Ablation Study Template

```markdown
| Variant       | Description              | Expected Impact |
|---------------|--------------------------|-----------------|
| Full model    | All features             | Baseline        |
| - Group A     | Remove feature group A   | -X% accuracy    |
| - Group B     | Remove feature group B   | -Y% accuracy    |
| Simple version| Replace deep net w/ linear| -Z% accuracy   |

Success criteria: Each component adds measurable value.
```
