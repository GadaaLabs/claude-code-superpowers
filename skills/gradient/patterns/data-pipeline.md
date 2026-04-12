# ML Engineering — Data Pipeline Patterns

## Schema Validation

```python
def test_input_schema_matches_expectations():
    expected_columns = {'user_id', 'timestamp', 'features', 'label'}
    assert expected_columns == set(df.columns), \
        f"Schema mismatch: missing {expected_columns - set(df.columns)}"

def test_feature_types_correct():
    assert df['features'].apply(lambda x: isinstance(x, np.ndarray)).all()
    assert df['features'].apply(lambda x: x.shape == (FEATURE_DIM,)).all()

def test_label_distribution_reasonable():
    label_counts = df['label'].value_counts()
    assert len(label_counts) == NUM_CLASSES
    assert (label_counts / len(df)).max() < 0.9  # No class dominates
```

## Distribution Shift Detection

```python
def test_feature_distribution_shift():
    from scipy import stats
    for feature_idx in range(FEATURE_DIM):
        ks_stat, p_value = stats.ks_2samp(
            train_features[:, feature_idx],
            prod_features[:, feature_idx]
        )
        assert p_value > 0.01, \
            f"Feature {feature_idx} drift detected (p={p_value:.4f})"

def test_covariate_shift():
    X = np.vstack([train_features, prod_features])
    y = np.array([0]*len(train_features) + [1]*len(prod_features))
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    auc = roc_auc_score(y_test,
        RandomForestClassifier().fit(X_train, y_train).predict_proba(X_test)[:,1])
    assert auc < 0.7, f"Covariate shift detected (AUC={auc:.3f})"
```

## Null / Edge Case Handling

```python
def test_null_handling():
    df_nulls = df.copy()
    df_nulls.loc[0:10, 'feature_5'] = np.nan
    predictions = model.predict(df_nulls)
    assert not np.any(np.isnan(predictions))
    assert len(predictions) == len(df_nulls)

def test_empty_input():
    empty_df = pd.DataFrame(columns=df.columns)
    predictions = model.predict(empty_df)
    assert len(predictions) == 0

def test_extreme_values():
    df_extreme = df.copy()
    df_extreme.loc[0, 'feature_5'] = 1e10
    predictions = model.predict(df_extreme)
    assert predictions.min() >= 0 and predictions.max() <= 1
```

## Data Leakage Check

```python
def test_no_data_leakage():
    for feature_name in feature_columns:
        correlation = np.corrcoef(
            df[feature_name].values,
            df['label'].shift(-1).values  # Future label
        )[0, 1]
        assert abs(correlation) < 0.1, \
            f"{feature_name} may have data leakage (corr={correlation:.3f})"

def test_feature_computation_reproducible():
    features_1 = compute_features(sample_input)
    features_2 = compute_features(sample_input)
    np.testing.assert_array_equal(features_1, features_2)
```
