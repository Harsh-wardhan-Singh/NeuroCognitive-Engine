from engines.quiz_engine.adaptive_logic import determine_difficulty


def test_high_streak_and_high_mastery_hard():
    concept = {"concept_id": "a", "mastery": 0.8, "confidence": 0.5, "attempts": 4, "correct_attempts": 3}
    risk = {"p_error": 0.3, "risk_level": "LOW"}
    session_state = {"current_streak": 3, "last_concept": None, "recent_concepts": []}
    expected = "HARD"
    output = determine_difficulty(concept, risk, session_state)
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_low_streak_easy():
    concept = {"concept_id": "a", "mastery": 0.9, "confidence": 0.9, "attempts": 4, "correct_attempts": 4}
    risk = {"p_error": 0.1, "risk_level": "LOW"}
    session_state = {"current_streak": 1, "last_concept": None, "recent_concepts": []}
    expected = "EASY"
    output = determine_difficulty(concept, risk, session_state)
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_high_risk_easy():
    concept = {"concept_id": "a", "mastery": 0.9, "confidence": 0.9, "attempts": 4, "correct_attempts": 4}
    risk = {"p_error": 0.7, "risk_level": "HIGH"}
    session_state = {"current_streak": 2, "last_concept": None, "recent_concepts": []}
    expected = "EASY"
    output = determine_difficulty(concept, risk, session_state)
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def run_all():
    test_high_streak_and_high_mastery_hard()
    test_low_streak_easy()
    test_high_risk_easy()


if __name__ == "__main__":
    run_all()