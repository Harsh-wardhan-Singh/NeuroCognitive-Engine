from engines.quiz_engine.adaptive_logic import determine_difficulty
from engines.quiz_engine.quiz_selector import select_concept
def generate_next_question(concepts, risks, session_state):
    selected_concept, reason = select_concept(concepts, risks, session_state)
    selected_risk = risks[selected_concept["concept_id"]]
    difficulty = determine_difficulty(selected_concept, selected_risk, session_state)
    return {
        "concept_id": selected_concept["concept_id"],
        "difficulty": difficulty,
        "reason": reason,
    }