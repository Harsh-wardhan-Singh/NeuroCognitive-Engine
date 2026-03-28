import engines.quiz_engine.quiz_selector as quiz_selector


def test_lowest_mastery_gets_selected():
    original_should_explore = quiz_selector.should_explore
    quiz_selector.should_explore = lambda epsilon=0.15: False

    concepts = [
        {"concept_id": "a", "mastery": 0.2, "confidence": 0.6, "attempts": 5, "correct_attempts": 2},
        {"concept_id": "b", "mastery": 0.8, "confidence": 0.6, "attempts": 5, "correct_attempts": 4},
    ]
    risks = {
        "a": {"p_error": 0.5, "risk_level": "MEDIUM"},
        "b": {"p_error": 0.5, "risk_level": "MEDIUM"},
    }
    session_state = {"last_concept": None, "recent_concepts": [], "current_streak": 0}

    selected, reason = quiz_selector.select_concept(concepts, risks, session_state)
    expected = "a"
    output = selected["concept_id"]
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected
    print("Expected:", "low_mastery_exploit")
    print("Got:", reason)
    assert reason == "low_mastery_exploit"

    quiz_selector.should_explore = original_should_explore


def test_high_risk_overrides_repetition_rule():
    original_should_explore = quiz_selector.should_explore
    quiz_selector.should_explore = lambda epsilon=0.15: False

    concepts = [
        {"concept_id": "a", "mastery": 0.5, "confidence": 0.5, "attempts": 5, "correct_attempts": 2},
        {"concept_id": "b", "mastery": 0.6, "confidence": 0.6, "attempts": 5, "correct_attempts": 3},
    ]
    risks = {
        "a": {"p_error": 0.9, "risk_level": "HIGH"},
        "b": {"p_error": 0.2, "risk_level": "LOW"},
    }
    session_state = {"last_concept": "a", "recent_concepts": [], "current_streak": 0}

    selected, reason = quiz_selector.select_concept(concepts, risks, session_state)
    expected = "a"
    output = selected["concept_id"]
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected
    print("Expected:", "high_risk_intervention")
    print("Got:", reason)
    assert reason == "high_risk_intervention"

    quiz_selector.should_explore = original_should_explore


def test_recent_concept_penalty_works():
    original_should_explore = quiz_selector.should_explore
    quiz_selector.should_explore = lambda epsilon=0.15: False

    concepts = [
        {"concept_id": "a", "mastery": 0.2, "confidence": 0.5, "attempts": 5, "correct_attempts": 2},
        {"concept_id": "b", "mastery": 0.3, "confidence": 0.5, "attempts": 5, "correct_attempts": 3},
    ]
    risks = {
        "a": {"p_error": 0.2, "risk_level": "MEDIUM"},
        "b": {"p_error": 0.3, "risk_level": "MEDIUM"},
    }
    session_state = {"last_concept": None, "recent_concepts": ["a"], "current_streak": 0}

    selected, _ = quiz_selector.select_concept(concepts, risks, session_state)
    expected = "b"
    output = selected["concept_id"]
    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    quiz_selector.should_explore = original_should_explore


def run_all():
    test_lowest_mastery_gets_selected()
    test_high_risk_overrides_repetition_rule()
    test_recent_concept_penalty_works()


if __name__ == "__main__":
    run_all()