# 🧠 Cognitive Engine Specification — NeuroCognitive Engine v2

## 🎯 Objective

Implement the Cognitive Engine responsible for:

* Mastery tracking (BKT)
* Retention decay
* Confidence modeling
* Dependency propagation

This engine must be PURE LOGIC:

* No API
* No database
* No external dependencies

---

# 📁 FILE STRUCTURE

engines/cognitive_engine/

```
mastery_update.py  
retention_decay.py  
confidence_model.py  
dependency_propagation.py  
```

---

# 🔥 GLOBAL RULES

* All functions must be deterministic
* No randomness
* No external API calls
* Use only built-in Python libraries
* Inputs and outputs must EXACTLY match specification

---

# 📄 FILE 1: mastery_update.py

## PURPOSE

Update concept mastery using Bayesian Knowledge Tracing (BKT)

---

## FUNCTION

def update_mastery(
prior_mastery: float,
is_correct: bool,
slip: float,
guess: float,
learn: float
) -> float

---

## LOGIC

1. Compute posterior based on correctness:

If correct:
posterior = (prior_mastery * (1 - slip)) /
(prior_mastery * (1 - slip) + (1 - prior_mastery) * guess)

If incorrect:
posterior = (prior_mastery * slip) /
(prior_mastery * slip + (1 - prior_mastery) * (1 - guess))

---

2. Apply learning transition:

new_mastery = posterior + (1 - posterior) * learn

---

## RETURN

float between 0 and 1

---

## TEST CASE

input:
prior_mastery = 0.5
is_correct = True
slip = 0.1
guess = 0.2
learn = 0.1

expected output ≈ 0.86 (allow small float tolerance)

---

---

# 📄 FILE 2: retention_decay.py

## PURPOSE

Reduce mastery over time

---

## FUNCTION

def apply_decay(
mastery: float,
last_seen_timestamp: float,
current_time: float,
decay_rate: float
) -> float

---

## LOGIC

time_diff = current_time - last_seen_timestamp

decayed_mastery = mastery * e^(-decay_rate * time_diff)

---

## RETURN

float

---

## TEST CASE

input:
mastery = 0.8
time_diff = 10
decay_rate = 0.05

expected output ≈ 0.48

---

---

# 📄 FILE 3: confidence_model.py

## PURPOSE

Track calibration between perceived and actual performance

---

## FUNCTION

def update_confidence(
previous_confidence: float,
reported_confidence: float,
correctness: bool
) -> float

---

## LOGIC

If correct:
target = 1
Else:
target = 0

error = target - reported_confidence

new_confidence = previous_confidence + 0.1 * error

Clamp between 0 and 1

---

## TEST CASE

input:
prev = 0.5
reported = 0.8
correctness = False

expected output ≈ 0.42

---

---

# 📄 FILE 4: dependency_propagation.py

## PURPOSE

Propagate mastery to dependent concepts

---

## FUNCTION

def propagate_mastery(
concept_id: str,
mastery: float,
concept_graph: dict
) -> dict

---

## INPUT FORMAT

concept_graph:

{
"A": ["B", "C"],
"B": ["D"],
"C": [],
"D": []
}

---

## LOGIC

* For each dependent node:
  reduce mastery by factor (e.g., 0.8)
* Return updated dict

---

## OUTPUT

{
"B": 0.8 * mastery,
"C": 0.8 * mastery,
...
}

---

## TEST CASE

input:
concept_id = "A"
mastery = 0.9

expected:
B = 0.72
C = 0.72

---

---

# 🧪 VALIDATION RULES

After each file:

1. Run test function
2. Print:

print("Expected:", expected)
print("Got:", output)

3. If mismatch:
   fix immediately

---

# 🚫 FAILURE CONDITIONS

If ANY of the following happen, STOP:

* Function signature mismatch
* Missing return value
* Extra parameters added
* Output not matching test

---

# ✅ COMPLETION CRITERIA

All 4 files:

* Implemented
* Tested
* Outputs verified

---

# 🧠 FINAL STEP

After completing all files:

Create a summary:

* What each file does
* Inputs/outputs verified
* Any assumptions made

Then STOP.
