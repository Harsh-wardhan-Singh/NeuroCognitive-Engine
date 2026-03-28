# 🧠 RISK ENGINE — FULL SPECIFICATION

NeuroCognitive Engine v2

---

# 🎯 1. PURPOSE (CRITICAL CONTEXT)

The Risk Engine predicts:

> ❗ **Probability that a student will answer a concept incorrectly**

This is NOT:

* rule-based ❌
* heuristic-only ❌

This IS:

* feature-based prediction system ✅
* deterministic (for now) ✅
* ML-ready (future upgrade) ✅

---

# 🔄 2. INPUT (FROM COGNITIVE ENGINE)

Input is a structured object per concept:

```json
{
  "concept_id": "fractions_basic",
  "mastery": 0.72,
  "confidence": 0.41,
  "last_seen_timestamp": 1710000000,
  "attempts": 5,
  "correct_attempts": 3
}
```

---

# 📤 3. OUTPUT

```json
{
  "concept_id": "fractions_basic",
  "p_error": 0.63,
  "risk_level": "HIGH",
  "features_used": {
    "mastery": 0.72,
    "confidence": 0.41,
    "recency": 0.28,
    "accuracy": 0.60
  }
}
```

---

# 🧩 4. FEATURE ENGINEERING (MOST IMPORTANT PART)

All prediction depends on features.

---

## 🔹 4.1 Accuracy

```python
accuracy = correct_attempts / attempts
```

Edge case:

* if attempts == 0 → accuracy = 0.5 (neutral prior)

---

## 🔹 4.2 Recency (TIME DECAY FEATURE)

```python
time_diff = current_time - last_seen_timestamp
recency = exp(-lambda * time_diff)
```

Recommended:

```python
lambda = 0.001
```

---

## 🔹 4.3 Mastery

Directly from cognitive engine.

---

## 🔹 4.4 Confidence

Directly from cognitive engine.

---

# 🧠 5. FEATURE VECTOR

Final vector:

```python
X = [
    mastery,
    confidence,
    recency,
    accuracy
]
```

---

# ⚙️ 6. MODEL (DETERMINISTIC VERSION)

We simulate a logistic regression manually.

---

## 🔹 6.1 Weights (INITIAL — HARDCODED)

```python
weights = {
    "mastery": -2.0,
    "confidence": -1.5,
    "recency": -1.0,
    "accuracy": -2.5
}

bias = 1.5
```

---

## 🔹 6.2 Linear Combination

```python
z = (
    mastery * -2.0 +
    confidence * -1.5 +
    recency * -1.0 +
    accuracy * -2.5 +
    1.5
)
```

---

## 🔹 6.3 Sigmoid Function

```python
p_error = 1 / (1 + exp(-z))
```

---

# 🔥 7. RISK LEVEL CLASSIFICATION

Use tolerance-aware comparisons.

```python
if p_error > 0.7:
    risk = "HIGH"
elif p_error > 0.4:
    risk = "MEDIUM"
else:
    risk = "LOW"
```

---

# 📁 8. FILE STRUCTURE

```
risk_engine/
│
├── feature_extractor.py
├── risk_model.py
├── predictor.py
├── utils.py
└── tests/
    ├── test_features.py
    ├── test_model.py
    └── test_predictor.py
```

---

# 📄 9. FILE RESPONSIBILITIES

---

## 📁 feature_extractor.py

### Responsibility:

Convert raw input → feature vector

### Functions:

```python
def compute_accuracy(attempts, correct_attempts)

def compute_recency(current_time, last_seen_timestamp)

def build_feature_vector(data, current_time)
```

---

## 📁 risk_model.py

### Responsibility:

Pure model logic

### Functions:

```python
def linear_combination(features)

def sigmoid(z)

def predict_probability(features)
```

---

## 📁 predictor.py

### Responsibility:

End-to-end wrapper

### Functions:

```python
def predict_risk(concept_data, current_time)
```

Returns full output JSON.

---

## 📁 utils.py

### Responsibility:

Shared helpers

```python
def is_close(a, b, tol=1e-5)
```

---

# 🧪 10. TEST CASES (MANDATORY)

---

## 🔹 Feature Tests

* accuracy calculation
* recency decay behavior
* zero-attempt handling

---

## 🔹 Model Tests

* sigmoid correctness
* monotonicity:
  higher mastery → lower p_error

---

## 🔹 Predictor Tests

Input:

```json
mastery = 0.8, confidence = 0.7, recency = high, accuracy = high
```

Expected:

```plaintext
LOW risk
```

---

# 🔒 FLOAT PRECISION RULES

* NEVER use direct float comparison (==)
* ALWAYS use tolerance-based comparison

Use helper:

def is_close(a, b, tol=1e-5)

For thresholds:

* Use small buffers (e.g., 1e-5)

All test cases must use tolerance:
assert abs(output - expected) < tolerance

---

# 🚀 12. IMPLEMENTATION STRATEGY (VERY IMPORTANT)

The agent MUST follow this order:

---

## STEP 1 — feature_extractor.py

* implement all features
* test independently

---

## STEP 2 — risk_model.py

* implement sigmoid + linear model
* verify with manual values

---

## STEP 3 — predictor.py

* combine everything

---

## STEP 4 — tests

* validate entire pipeline

---

## STEP 5 — sanity checks

* monotonic behavior
* edge cases

---

# 🧠 13. FUTURE UPGRADE PATH

Later replace:

```python
weights → trained logistic regression
```

But keep:

* feature_extractor unchanged
* predictor unchanged

---

# ⚠️ 14. STRICT RULES

* NO randomness
* NO LLM usage
* FULL determinism
* SMALL modular functions only
* NO hidden state

---

# 🧠 FINAL NOTE TO AGENT

Before writing code:

1. Understand each feature mathematically
2. Validate edge cases
3. Write tests FIRST (preferred)

Then implement.

---
