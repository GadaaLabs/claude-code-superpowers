# ML Engineering — Model Serving Patterns

## Input Validation

```python
def test_input_schema_validation():
    response = model_server.predict({'user_id': '123'})  # Missing fields
    assert response.status_code == 400
    assert 'missing required field' in response.json()['error']

def test_input_range_validation():
    response = model_server.predict({'age': 500, 'income': -1000})
    assert response.status_code == 400

def test_input_distribution_check():
    input_features = get_features(request)
    z_scores = np.abs((input_features - train_mean) / train_std)
    if np.any(z_scores > 4):
        log_warning(f"Unusual input: z={z_scores.max():.2f}")
```

## Latency Tests

```python
def test_p99_latency_within_budget():
    latencies = []
    for _ in range(1000):
        start = time.time()
        model_server.predict(valid_input)
        latencies.append(time.time() - start)
    p99 = np.percentile(latencies, 99)
    assert p99 < LATENCY_BUDGET_MS, f"P99 {p99:.1f}ms > budget {LATENCY_BUDGET_MS}ms"

def test_throughput_meets_requirements():
    with concurrent.futures.ThreadPoolExecutor(max_workers=EXPECTED_QPS) as ex:
        start = time.time()
        list(ex.map(lambda _: model_server.predict(valid_input), range(EXPECTED_QPS)))
        elapsed = time.time() - start
    assert EXPECTED_QPS / elapsed >= EXPECTED_QPS * 0.9
```

## Fallback Behavior

```python
def test_model_unavailable_fallback():
    with patch('model_server.model', side_effect=ConnectionError()):
        response = model_server.predict(valid_input)
    assert response.status_code == 200
    assert response.json()['fallback_used'] == True
    assert response.json()['prediction'] == DEFAULT_PREDICTION

def test_timeout_handling():
    with patch('model_server.model.predict', side_effect=TimeoutError()):
        response = model_server.predict(valid_input)
    assert response.status_code == 504
```

## Output Calibration

```python
def test_confidence_scores_calibrated():
    for bin_lower in [0.5, 0.6, 0.7, 0.8, 0.9]:
        bin_mask = (confidences >= bin_lower) & (confidences < bin_lower + 0.1)
        if bin_mask.sum() > 0:
            actual_accuracy = np.mean(predictions[bin_mask] == true_labels[bin_mask])
            assert abs(actual_accuracy - bin_lower) < 0.05
```
