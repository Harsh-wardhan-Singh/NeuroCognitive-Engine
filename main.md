# 🧠 ORCHESTRATOR + API LAYER SPEC

NeuroCognitive Engine v2

---

# 🚨 CRITICAL FIRST STEP (MANDATORY)

Before writing ANY code, the agent MUST:

1. Inspect the entire existing codebase:

   * cognitive_engine
   * risk_engine
   * quiz_engine
   * ai_generation
   * db layer (models, crud)

2. Understand:

   * function signatures
   * expected inputs/outputs
   * existing data flow

❗ DO NOT assume anything
❗ DO NOT rewrite existing engines
❗ ONLY integrate

---

# 🎯 OBJECTIVE

Build a **central orchestrator system** that:

* Runs the full adaptive quiz loop
* Connects all engines
* Uses database for persistence
* Exposes FastAPI endpoints
* Is fully compatible with frontend

---

# 🧱 ARCHITECTURE RULES (STRICT)

## 1. Engines must remain PURE

* NO database calls inside engines
* NO API logic inside engines

## 2. Orchestrator is the ONLY place for:

* DB interaction
* Engine coordination
* State management

## 3. FastAPI layer ONLY calls orchestrator

* No direct DB or engine logic in routes

---

# 📁 NEW FOLDER STRUCTURE

```
backend/
└── orchestrator/
    ├── session_manager.py
    ├── quiz_orchestrator.py
    ├── schemas.py
    └── utils.py

backend/
└── api/
    ├── main.py
    └── routes/
        └── quiz.py
```

---

# 🧠 CONCEPT MODEL (UPDATED)

We now use hierarchical concept tracking:

* subject
* topic
* concept

However:

* DB still uses `concept_id` (string)
* Format must be:

```
concept_id = "subject.topic.concept"
```

Example:

```
"math.algebra.linear_equations"
```

---

# 🧠 SESSION SYSTEM (DATABASE-BASED)

## Create NEW TABLE: sessions

Columns:

* session_id (UUID, PK)
* user_id (FK)
* subject (string)
* topic (string)
* total_questions (int)
* questions_answered (int)
* current_concept (string)
* started_at (timestamp)
* updated_at (timestamp)
* is_active (boolean)

---

# ⚙️ ORCHESTRATOR FLOW

## START SESSION

Input:

* subject
* topic
* num_questions (5–20)

Steps:

1. Create user if not exists
2. Create session row
3. Initialize concept (use quiz_engine)
4. Fetch mastery_state from DB
5. Generate first question

---

## QUESTION LOOP (CORE)

For each answer:

### Step 1: Validate input

* selected_option
* reported_confidence
* response_time

---

### Step 2: Compute correctness (BACKEND ONLY)

* Compare selected_option with correct_answer

❗ NEVER trust frontend for correctness

---

### Step 3: Log attempt

Call:

```
log_attempt()
```

---

### Step 4: Fetch current mastery state

Call:

```
get_mastery_state()
```

---

### Step 5: Apply retention decay

Use:

```
time_diff = now - last_seen_timestamp
```

---

### Step 6: Update mastery

Call cognitive_engine

---

### Step 7: Update confidence

Use improved confidence model

---

### Step 8: Compute risk

Call risk_engine

---

### Step 9: Update DB

Call:

```
upsert_mastery_state()
```

---

### Step 10: Select next concept

Use quiz_engine

---

### Step 11: Generate next question

Call AI generator

Must pass:

* concept
* difficulty
* last 15 questions (anti-repetition)

---

### Step 12: Update session

* increment questions_answered
* update current_concept

---

# 🧠 QUESTION MEMORY (IMPORTANT)

Maintain in session:

```
last_questions = [last 15 question_ids or texts]
```

Store in:

* session_service (DB-backed)

---

# 🧠 SESSION END

When:

* questions_answered == total_questions

---

## Compute summary:

* accuracy
* avg confidence
* weak concepts
* strong concepts
* risk insights

---

## Mark session inactive

---

# 🌐 FASTAPI ENDPOINTS

---

## 1. START SESSION

POST `/start-session`

Request:

```json
{
  "user_id": null,
  "subject": "math",
  "topic": "algebra",
  "num_questions": 10
}
```

Response:

```json
{
  "session_id": "...",
  "question": {
    "question_id": "...",
    "text": "...",
    "options": ["A", "B", "C", "D"]
  }
}
```

---

## 2. SUBMIT ANSWER

POST `/submit-answer`

Request:

```json
{
  "session_id": "...",
  "question_id": "...",
  "selected_option": "B",
  "reported_confidence": 0.75,
  "response_time": 4.2
}
```

Response:

```json
{
  "correct": true,
  "explanation": "...",
  "next_question": { ... },
  "is_session_complete": false
}
```

---

## 3. END SESSION

GET `/end-session/{session_id}`

Response:

```json
{
  "summary": {
    "accuracy": 0.7,
    "avg_confidence": 0.65,
    "weak_concepts": [],
    "strong_concepts": []
  }
}
```

---

# ⚠️ IMPORTANT FRONTEND CONTRACT

Frontend MUST send:

* selected_option
* reported_confidence
* response_time

Frontend MUST NOT send:

* correctness ❌

---

# ⚙️ IMPLEMENTATION DETAILS

## session_manager.py

* create_session()
* update_session()
* get_session()

## quiz_orchestrator.py

Main function:

* start_session()
* submit_answer()
* end_session()

## schemas.py

Define:

* StartSessionRequest
* SubmitAnswerRequest
* QuestionResponse
* SessionSummary

## quiz.py (routes)

* connect endpoints → orchestrator functions

## main.py

* initialize FastAPI app
* include routes

---

# 🚀 SUCCESS CRITERIA

* Full quiz loop works
* DB updates correctly
* No engine contains DB logic
* API returns correct responses
* Ready for frontend integration
