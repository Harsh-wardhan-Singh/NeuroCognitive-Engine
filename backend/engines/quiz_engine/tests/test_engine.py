import engines.quiz_engine.quiz_selector as quiz_selector

from engines.quiz_engine.engine import generate_next_question


def test_generate_next_question_combines_outputs():
    original_should_explore = quiz_selector.should_explore
    quiz_selector.should_explore = lambda epsilon=0.15: False

    concepts = [
        {"concept_id": "fractions_basic", "mastery": 0.8, "confidence": 0.7, "attempts": 5, "correct_attempts": 4},
        {"concept_id": "ratios_intro", "mastery": 0.4, "confidence": 0.6, "attempts": 5, "correct_attempts": 2},
    ]
    risks = {
        "fractions_basic": {"p_error": 0.2, "risk_level": "LOW"},
        "ratios_intro": {"p_error": 0.5, "risk_level": "MEDIUM"},
    }
    session_state = {"current_streak": 2, "last_concept": "fractions_basic", "recent_concepts": []}

    output = generate_next_question(concepts, risks, session_state)
    expected = {"concept_id": "ratios_intro", "difficulty": "MEDIUM", "reason": "low_mastery_exploit"}
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    quiz_selector.should_explore = original_should_explore


def test_generate_next_question_high_risk_reason_and_easy():
    original_should_explore = quiz_selector.should_explore
    quiz_selector.should_explore = lambda epsilon=0.15: False

    concepts = [
        {"concept_id": "fractions_basic", "mastery": 0.6, "confidence": 0.5, "attempts": 5, "correct_attempts": 3},
        {"concept_id": "ratios_intro", "mastery": 0.7, "confidence": 0.7, "attempts": 5, "correct_attempts": 4},
    ]
    risks = {
        "fractions_basic": {"p_error": 0.8, "risk_level": "HIGH"},
        "ratios_intro": {"p_error": 0.2, "risk_level": "LOW"},
    }
    session_state = {"current_streak": 2, "last_concept": "fractions_basic", "recent_concepts": ["ratios_intro"]}

    output = generate_next_question(concepts, risks, session_state)
    expected = {"concept_id": "fractions_basic", "difficulty": "EASY", "reason": "high_risk_intervention"}
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    quiz_selector.should_explore = original_should_explore


def run_all():
    test_generate_next_question_combines_outputs()
    test_generate_next_question_high_risk_reason_and_easy()


if __name__ == "__main__":
    run_all()