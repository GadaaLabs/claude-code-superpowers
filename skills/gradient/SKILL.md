---
name: gradient
description: ML-specific patterns for data pipelines, model training, MLOps, and evaluation — domain expertise for machine learning engineers
type: domain
---

# ML Engineering Patterns

## Overview

**Core principle:** ML systems have unique failure modes — data drift, training-serving skew, silent degradation. Test data and models, not just code.

**Announce at start:** "I'm using the GRADIENT skill for ML-specific patterns."

---

## Entry Point — First 5 Minutes

```
STAGE ASSESSMENT:

"What stage are you at?"
A) Data collection / ingestion
B) Feature engineering / preprocessing
C) Model training / experimentation
D) Model evaluation / validation
E) Model serving / inference
F) Production monitoring / MLOps
G) Debugging an ML failure
```

**Stage → Section mapping:**
- A/B → Data Pipeline Testing (see patterns/data-pipeline.md)
- C → Model Training (see patterns/model-training.md)
- D → ML Evaluation (correctness metrics, calibration)
- E → Model Serving TDD (see patterns/model-serving.md)
- F → MLOps Deployment (see patterns/mlops.md)
- G → Run `hunter` first, then return with evidence

**After identifying stage, ask:**
"What's the primary constraint — accuracy, latency, cost, or reliability?"

---

## Data Pipeline Testing

Load patterns: **`patterns/data-pipeline.md`**

Key tests to implement:
1. **Schema validation** — column set, feature types, label distribution
2. **Distribution shift detection** — KS test per feature, covariate shift AUC
3. **Null / edge case handling** — nulls, empty input, extreme values
4. **Data leakage check** — correlation with future labels, reproducibility

Rule: **Write pipeline tests before writing model code.**

---

## Model Training Checklist

Load patterns: **`patterns/model-training.md`**

Before training complex models:
- [ ] Simple baseline implemented (logistic regression / majority class)
- [ ] Baseline metrics documented (accuracy, F1, AUC-ROC, latency)
- [ ] Hyperparameter search configured (Bayesian preferred; grid only if ≤ 3 params)
- [ ] Early stopping rules defined (patience, min_delta, restore_best_weights)
- [ ] Checkpoint strategy set (save_best_only, monitor_metric, metadata)
- [ ] Ablation study planned (each component justified)

---

## Model Serving TDD

Load patterns: **`patterns/model-serving.md`**

Tests required before deployment:
1. **Input validation** — schema, range, distribution z-score check
2. **Latency** — p99 within budget, throughput at expected QPS
3. **Fallback** — model unavailable → default response, timeout → 504
4. **Output calibration** — confidence bins match actual accuracy ± 5%

---

## MLOps Deployment

Load patterns: **`patterns/mlops.md`**

Required components:
1. **Model versioning** — semver, git commit + data version + metrics in metadata
2. **A/B test config** — traffic split, primary metric, guardrail metrics, stopping criteria
3. **Drift monitoring** — PSI for data drift (threshold 0.1), CUSUM for concept drift
4. **Rollback triggers** — accuracy drop >5%, error rate >1%, latency >2×, PSI >0.25

---

## ML Evaluation Framework

| Task | Metrics |
|------|---------|
| Classification | accuracy, precision, recall, F1, AUC-ROC, AUC-PR |
| Regression | MAE, MSE, RMSE, R², MAPE |
| Ranking | NDCG, MAP, MRR |

Cost/latency budgets (set before training, enforce in CI):
- p99 latency: 100ms
- cost per 1k requests: $1.00

---

## Red Flags

**Never:**
- Deploy without baseline comparison
- Skip drift monitoring in production
- Train without checkpointing
- Use test data for training
- Deploy without rollback plan

**Always:**
- Test data pipelines before model training
- Validate input distribution matches training
- Track model version with data version
- Monitor prediction distribution in production
- Have fallback for model failures

---

## Integration with Superpowers

| Skill | Integration |
|-------|-------------|
| `forge` | Write data tests before pipeline, model tests before training |
| `hunter` | Use for training failures, accuracy drops |
| `sentinel` | Verify metrics before claiming model works |
| `chronicle` | Store patterns from failed experiments |

---

## Final Checklist

- [ ] Data pipeline tests pass (schema, distribution, edge cases)
- [ ] Baseline model established and documented
- [ ] Complex model beats baseline (with ablation study)
- [ ] Input validation tests pass
- [ ] Output calibration verified
- [ ] Latency budget met (p99)
- [ ] Fallback behavior tested
- [ ] Model versioned with metadata
- [ ] Drift monitoring configured
- [ ] Rollback triggers defined
