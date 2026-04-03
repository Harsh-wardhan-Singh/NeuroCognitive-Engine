# 🤖 AI GENERATION ENGINE — FULL IMPLEMENTATION SPEC

This document is for the backend agent to implement the **ai_generation module** completely and correctly.

---

# 🎯 PURPOSE OF THIS MODULE

This module is ONLY responsible for:

1. Generating questions
2. Generating explanations

⚠️ It MUST NOT:

* Make decisions about difficulty
* Select concepts
* Track user state

That logic belongs to:

* quiz_engine
* cognitive_engine
* risk_engine

---

# 📁 FINAL DIRECTORY STRUCTURE

```
ai_generation/
│
├── llm_client.py
├── prompt_templates.py
├── question_generator.py
└── explanation_generator.py
```

---

# 🔐 ENVIRONMENT SETUP

## Create `.env` file (root level)

```
HF_API_KEY=your_huggingface_api_key_here
```

## Add to `.gitignore`

```
.env
```

---

# 📦 DEPENDENCIES

```
pip install requests python-dotenv
```

---

# 🧠 GLOBAL DESIGN RULES (STRICT)

1. LLM is a TOOL, not intelligence
2. All outputs must be structured JSON
3. Every output must be validated
4. Retry on failure
5. No business logic inside this module

---

# 1️⃣ llm_client.py

## 🎯 Responsibility

* Handle HuggingFace API calls
* Retry logic
* Return raw text output

## 📥 Input

* prompt (string)
* temperature (float)
* max_tokens (int)

## 📤 Output

* raw LLM string response

## 🧱 Implementation Requirements

* Use HuggingFace Inference API
* Model: meta-llama/Meta-Llama-3-8B-Instruct
* Use API key from `.env`
* Retry up to 3 times

## ⚠️ Behavior Rules

* If API fails → retry
* If all retries fail → raise exception

---

# 2️⃣ prompt_templates.py

## 🎯 Responsibility

* Store ALL prompts
* No logic

## 📥 Input

* concept (string)
* difficulty (string)
* question (string)
* correct_answer (string)

## 📤 Output

* formatted prompt string

## 🧱 Required Functions

### build_question_prompt(concept, difficulty)

Must:

* Clearly define task
* Force JSON output
* Prevent extra text

### build_explanation_prompt(question, correct_answer)

Must:

* Ask for clear explanation
* Return JSON format

## ⚠️ Rules

* Prompts must be strict
* Must explicitly say "ONLY valid JSON"

---

# 3️⃣ question_generator.py

## 🎯 Responsibility

* Generate question
* Validate output
* Retry if invalid

## 📥 Input

* concept (string)
* difficulty (string)

## 📤 Output

```
{
  "question": string,
  "options": list[string],
  "correct_answer": string
}
```

## 🧱 Logic Flow

1. Build prompt
2. Call LLM
3. Parse JSON
4. Validate structure
5. Retry if invalid

## ✅ Validation Rules

Must contain:

* question
* options (length = 4)
* correct_answer

## ⚠️ Failure Handling

* If JSON parsing fails → retry once
* If still fails → raise error

---

# 4️⃣ explanation_generator.py

## 🎯 Responsibility

* Generate explanation for a question

## 📥 Input

* question (string)
* correct_answer (string)

## 📤 Output

```
{
  "explanation": string
}
```

## 🧱 Logic Flow

1. Build prompt
2. Call LLM
3. Parse JSON
4. Return explanation

## ⚠️ Failure Handling

* If parsing fails → return fallback string

---

# 🔄 DATA FLOW (IMPORTANT)

```
quiz_engine
    ↓
question_generator
    ↓
LLM
    ↓
question JSON
    ↓
frontend
    ↓
user answer
    ↓
explanation_generator
    ↓
LLM
    ↓
explanation
```

---

# ⚠️ COMMON FAILURE CASES

1. Non-JSON output
2. Missing keys
3. Wrong format

## Must handle via:

* strict prompts
* retries
* validation

---

# 🧪 TEST CASES (MANDATORY)

Agent must test:

### Test 1

```
generate_question("Probability", "EASY")
```

### Test 2

```
generate_question("Algebra", "HARD")
```

### Test 3

```
generate_explanation(question, correct_answer)
```

## Expected:

* Valid JSON
* Logical question
* Correct answer matches options

---

# 🚀 SUCCESS CRITERIA

The module is COMPLETE when:

* Questions generate reliably
* JSON is valid most of the time
* Retry handles failures
* Clean separation of concerns maintained

---

# 🔥 OPTIONAL (ONLY IF NEEDED LATER)

DO NOT IMPLEMENT NOW unless required:

* schema_validator.py
* exponential backoff
* response caching

---

# 💥 FINAL NOTE

This module is NOT the brain.

It is ONLY the **content generator layer**.

All intelligence comes from:

* cognitive_engine
* risk_engine
* quiz_engine

Keep this separation STRICT.
