# 🧠 QUIZ ENGINE — FULL SPECIFICATION

NeuroCognitive Engine v2

---

# 🎯 1. PURPOSE (CRITICAL CONTEXT)

The Quiz Engine decides:

> ❗ **What should the student see next?**

This includes:

* which concept
* what difficulty
* whether to explore or reinforce

---

# 🚫 THIS IS NOT

* random question selection ❌
* static quizzes ❌
* LLM-driven decisions ❌

---

# ✅ THIS IS

* deterministic decision system
* data-driven selection
* adaptive behavior engine

---

# 🔄 2. INPUT

Input comes from BOTH engines:

---

## 🔹 2.1 Concept States (Cognitive Engine)

List of:

```json
[
  {
    "concept_id": "fractions_basic",
    "mastery": 0.72,
    "confidence": 0.41,
    "attempts": 5,
    "correct_attempts": 3
  }
]
```

---

## 🔹 2.2 Risk Output (Risk Engine)

```json
{
  "fractions_basic": {
    "p_error": 0.63,
    "risk_level": "HIGH"
  }
}
```

---

## 🔹 2.3 Session State (NEW — VERY IMPORTANT)

```json
{
  "current_streak": 3,
  "last_concept": "fractions_basic",
  "recent_concepts": ["fractions_basic", "ratios_intro"]
}
```

---

# 📤 3. OUTPUT

```json
{
  "concept_id": "ratios_intro",
  "difficulty": "MEDIUM",
  "reason": "low_mastery_explore"
}
```

---

# 🧩 4. CORE COMPONENTS

---

# 🧠 4.1 CONCEPT SELECTION STRATEGY

---

## 🔹 Step 1: Score Each Concept

Define:

```python
priority_score =
    (1 - mastery) * 0.5 +
    p_error * 0.3 +
    (1 - confidence) * 0.2
```

---

## 🔹 Step 2: Sort Concepts

Highest score = highest priority

---

## 🔹 Step 3: Exploration vs Exploitation

Use epsilon-greedy:

```python
epsilon = 0.15
```

---

### Behavior:

* 85% → pick highest priority concept
* 15% → pick random concept (exploration)

---

## 🔹 Step 4: Avoid Repetition

Do NOT select:

```python
last_concept
```

unless:

* it is HIGH risk

---

## 🔹 Step 5: Recent Concepts Penalty

If concept in recent_concepts:

```python
score *= 0.8
```

---

# 🎯 4.2 DIFFICULTY ADAPTATION

---

## 🔹 Inputs:

* current_streak
* mastery
* p_error

---

## 🔹 Rules:

```python
if current_streak >= 3 and mastery > 0.7:
    difficulty = "HARD"

elif current_streak <= 1 or p_error > 0.6:
    difficulty = "EASY"

else:
    difficulty = "MEDIUM"
```

---

# 🔁 4.3 STREAK UPDATE LOGIC (FOR FUTURE USE)

(Not implemented here but must be designed for)

```python
if correct:
    streak += 1
else:
    streak = 0
```

---

# 🧠 4.4 REASON TAGGING (IMPORTANT)

Output MUST include reason:

Possible values:

```plaintext
low_mastery_exploit
high_risk_intervention
exploration
confidence_boost
streak_progression
```

---

# 📁 5. FILE STRUCTURE

```plaintext
quiz_engine/
│
├── quiz_selector.py
├── adaptive_logic.py
├── exploration.py
├── utils.py
└── tests/
    ├── test_selector.py
    ├── test_adaptive.py
    └── test_exploration.py
```

---

# 📄 6. FILE RESPONSIBILITIES

---

## 📁 quiz_selector.py

### Responsibility:

Select concept

### Functions:

```python
def compute_priority_score(concept, risk)

def select_concept(concepts, risks, session_state)
```

---

## 📁 adaptive_logic.py

### Responsibility:

Determine difficulty

```python
def determine_difficulty(concept, risk, session_state)
```

---

## 📁 exploration.py

### Responsibility:

Epsilon-greedy selection

```python
def should_explore(epsilon=0.15)
```

---

## 📁 utils.py

* is_close
* random selection helper

---

# 🧪 7. TEST CASES (MANDATORY)

---

## 🔹 Selector Tests

* lowest mastery gets selected
* high risk overrides repetition rule
* recent concept penalty works

---

## 🔹 Exploration Tests

* simulate multiple runs
* ~15% exploration rate (tolerance allowed)

---

## 🔹 Difficulty Tests

```plaintext
High streak + high mastery → HARD
Low streak → EASY
High risk → EASY
```

---

# 🔒 8. FLOAT PRECISION RULE

Apply tolerance everywhere.

---

# 🚀 9. IMPLEMENTATION STRATEGY

---

## STEP 1 — priority scoring

## STEP 2 — concept selection

## STEP 3 — exploration logic

## STEP 4 — difficulty logic

## STEP 5 — integrate

## STEP 6 — tests

---

# ⚠️ 10. STRICT RULES

* NO randomness without epsilon control
* NO LLM decision making
* PURE functions only
* FULL determinism (except exploration)

---

# 🧠 11. FUTURE EXTENSIONS

* dependency-aware selection
* spaced repetition scheduling
* multi-concept quizzes
* reinforcement learning

---

# 🧠 FINAL NOTE TO AGENT

Before coding:

1. Understand scoring formula deeply
2. Validate edge cases
3. Write tests first
4. Ensure deterministic behavior

---
