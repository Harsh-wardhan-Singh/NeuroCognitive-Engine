# 🗄️ DATABASE LAYER IMPLEMENTATION SPEC
NeuroCognitive Engine v2

This document defines the database layer required to support:
- Retention decay (time-aware)
- Confidence calibration
- Attempt tracking
- Future analytics & risk modeling

---

# 🎯 OBJECTIVE

Build a minimal but production-grade PostgreSQL-backed persistence layer.

The system must:
- Persist user attempts
- Maintain current mastery + confidence state
- Track timestamps for decay
- Be cleanly integrated with existing engines

---

# 📁 FOLDER STRUCTURE

backend/
└── db/
    ├── database.py        # DB connection + session
    ├── models.py          # ORM models (SQLAlchemy)
    ├── schemas.py         # Pydantic schemas
    ├── crud.py            # DB operations
    └── init_db.py         # Table creation script

---

# 🧱 TECH STACK

- PostgreSQL
- SQLAlchemy (ORM)
- psycopg2 (driver)
- Pydantic (validation)
- python-dotenv (env loading)

---

# 🔐 ENVIRONMENT VARIABLES (.env)

The system MUST load DB credentials from `.env`.

Required variables:

DATABASE_URL=postgresql://username:password@localhost:5432/neurodb

Example:
DATABASE_URL=postgresql://postgres:1234@localhost:5432/neurodb

---

# 🚫 .gitignore UPDATE

Ensure the following are ignored:

.env
__pycache__/
*.pyc

---

# 🧠 DATABASE SCHEMA

## 1. USERS TABLE

Purpose:
Identify each learner

Columns:
- user_id (Primary Key, UUID or INT)
- created_at (timestamp)

---

## 2. ATTEMPTS TABLE

Purpose:
Store every question attempt

Columns:
- attempt_id (Primary Key)
- user_id (Foreign Key → users)
- concept_id (string)
- question_id (string)
- correct (boolean)
- reported_confidence (float)
- response_time (float, seconds)
- timestamp (timestamp)

---

## 3. MASTERY_STATE TABLE

Purpose:
Store latest cognitive state per concept

Columns:
- user_id (Foreign Key)
- concept_id (string)
- mastery (float)
- confidence (float)
- last_seen_timestamp (timestamp)

Composite Key:
(user_id, concept_id)

---

# ⚙️ FILE RESPONSIBILITIES

---

## database.py

Responsibilities:
- Load DATABASE_URL from .env
- Create SQLAlchemy engine
- Create SessionLocal
- Provide get_db() dependency

Output:
- DB session object

---

## models.py

Responsibilities:
- Define ORM models for:
  - User
  - Attempt
  - MasteryState

Constraints:
- Proper primary + foreign keys
- Use timestamps correctly
- Ensure composite key for mastery_state

---

## schemas.py

Responsibilities:
- Define Pydantic schemas for:
  - AttemptCreate
  - MasteryUpdate
  - UserCreate

Used for:
- Validation between API ↔ DB

---

## crud.py

Responsibilities:

### create_user(db)
→ returns user_id

---

### log_attempt(db, attempt_data)
Input:
- user_id
- concept_id
- question_id
- correctness
- reported_confidence
- response_time

→ inserts into attempts table

---

### get_mastery_state(db, user_id, concept_id)
→ returns mastery, confidence, last_seen_timestamp

---

### upsert_mastery_state(db, data)
If exists:
  update mastery, confidence, last_seen_timestamp

Else:
  insert new row

---

## init_db.py

Responsibilities:
- Import models
- Create all tables

Used once during setup

---

# 🔁 INTEGRATION WITH EXISTING ENGINES

After each question:

1. Log attempt → log_attempt()
2. Update mastery → existing mastery_update logic
3. Update confidence → confidence model
4. Update DB → upsert_mastery_state()

---

# ⏱️ RETENTION DECAY REQUIREMENT

The system MUST use:

last_seen_timestamp

Future retention_decay will compute:

decay = f(current_time - last_seen_timestamp)

---

# ✅ REQUIREMENTS

- Code must be modular and clean
- No business logic inside DB layer
- No hardcoded credentials
- All DB access via Session
- Ready for FastAPI integration

---

# 🚀 SUCCESS CRITERIA

- Tables created successfully
- Can insert attempts
- Can update mastery_state
- Data persists across runs
- Ready for integration with engines