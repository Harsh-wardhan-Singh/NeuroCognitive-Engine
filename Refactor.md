# SYSTEM REFACTOR DIRECTIVE (PRODUCTION HARDENING)

You are working on a fully functional adaptive quiz backend system with:

* FastAPI routes
* Orchestrator-driven quiz loop
* PostgreSQL database
* Engines (quiz, cognitive, risk)
* AI question generation
* JWT authentication

Your task is to perform **critical architectural refactors** without breaking existing functionality.

---

# 🚨 GLOBAL RULES (MANDATORY)

1. DO NOT break existing API contracts
2. DO NOT remove working logic — only refactor/move it
3. DO NOT introduce placeholder code — everything must be functional
4. ALL DB access must go through service layer (no exceptions)
5. Maintain backward compatibility with current tests
6. Add minimal, clean, production-grade structure

---

# 🚨 ISSUE 1: REMOVE ORCHESTRATOR → CRUD VIOLATION

## ❌ Problem

`quiz_orchestrator.py` directly calls functions from `crud.py`

## ✅ Required Fix

### Step 1: Create new services

Create:

* `attempt_service.py`
* `mastery_service.py`

### attempt_service.py must include:

* `log_attempt(user_id, concept_id, correct, response_time, confidence)`
* `get_attempts_by_session(session_id)`
* any existing attempt-related CRUD logic moved from orchestrator

### mastery_service.py must include:

* `get_mastery_state(user_id, concept_id)`
* `upsert_mastery_state(...)`

---

### Step 2: Refactor orchestrator

Replace ALL direct `crud.py` usage with:

```python
attempt_service.*
mastery_service.*
session_service.*
user_service.*
```

Strict rule:

❌ No `crud.` import inside orchestrator
✅ Only services allowed

---

# 🚨 ISSUE 2: QUESTION STORAGE STRATEGY (KEEP SESSION-BASED)

Current:

✔ `session_questions` table exists
❌ no global question bank

Decision:

KEEP current session-based system
DO NOT introduce `question_bank` yet

Required:

* Ensure ALL correctness checks use `session_questions.correct_option`
* Ensure every generated question is persisted BEFORE being returned

---

# 🚨 ISSUE 3: REPEAT QUESTION SYSTEM (CRITICAL FIX)

## ❌ Problem:

* Orchestrator uses last 15 questions
* Generator only tracks last 10

## ✅ Required Fix (MANDATORY APPROACH):

REMOVE in-memory tracking from:

* `question_generator.py`

Replace with:
DB-based repetition control ONLY

---

## Implementation:

### In orchestrator:

* Fetch last 15 questions from `session_questions` via `session_service`
* Pass them into generator as:

```
previous_questions: List[str]
```

### In generator:

* REMOVE any internal queue/memory
* Use ONLY input `previous_questions`

---

# 🚨 ISSUE 4: CENTRALIZED CONFIG SYSTEM

## ❌ Problem:

Hardcoded constants across files

## ✅ Required Fix:

Create:

```
config/settings.py
```

Move ALL constants:

Examples:

```
DECAY_RATE = 0.1
LEARNING_RATE = 0.2
SLIP_PROB = 0.1
GUESS_PROB = 0.2
AVG_RESPONSE_TIME = 30
MAX_QUESTION_HISTORY = 15
```

---

## Refactor:

Replace ALL hardcoded values across:

* orchestrator
* cognitive_engine
* utils.py
* risk_engine

Import from:

```
from config.settings import ...
```

---

# 🚨 ISSUE 5: ANALYTICS SERVICE EXTRACTION

## ❌ Problem:

Analytics logic inside orchestrator

## ✅ Required Fix:

Create:

```
analytics_service.py
```

Move logic from orchestrator:

Must include:

* `calculate_accuracy(attempts)`
* `calculate_streak(attempts)`
* `get_weak_concepts(user_id)`
* `confidence_trend(attempts)`
* `generate_session_summary(session_id)`

---

## Orchestrator change:

Replace analytics logic with:

```
analytics_service.generate_session_summary(session_id)
```

---

# 🚨 ISSUE 6: CONCEPT SYSTEM (CONTROLLED TEMPORARY STATE)

Current:

* Concepts come from `utils.py`

## ✅ Required:

DO NOT replace system yet

Add clear abstraction:

Create:

```
concept_service.py
```

### Responsibilities:

* `get_concepts(subject, topic)`

### Internally:

* still use `utils.py`

### Purpose:

Future migration to DB without touching orchestrator

---

# 🚨 ISSUE 7: AUTH HARDENING (PHASE 1)

Current:

* JWT basic auth exists

---

## Required Improvements:

### 1. Move secret to ENV

* Remove fallback secret
* Must use `.env`

### 2. Add password validation:

* min length
* at least 1 number

### 3. Add token expiration enforcement

* Ensure expiry is checked on every request

### 4. Add placeholder for future:

```
def revoke_token(token: str):
    pass
```

---

# 🧪 TESTING REQUIREMENTS

After refactor:

* Start session works
* Submit answer works
* Mastery updates correctly
* Confidence updates correctly
* No repeated questions (last 15)
* Session completes correctly
* JWT auth still protects routes

---

# 🧾 OUTPUT FORMAT

Return:

* List of files modified
* List of files created
* Summary of changes per issue
* Any assumptions made
* Any remaining risks

---

# 🚀 FINAL OBJECTIVE

After this refactor:

* System must follow CLEAN ARCHITECTURE
* DB access must be fully abstracted
* Logic must be modular and scalable
* Ready for frontend integration
