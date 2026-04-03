from engines.ai_generation.prompt_templates import (
    build_explanation_prompt,
    build_question_prompt,
)


def test_build_question_prompt_contains_required_constraints():
    output = build_question_prompt("Probability", "EASY", [])

    expected = True
    actual = (
        "Concept: Probability" in output
        and "Difficulty: EASY" in output
        and '"question"' in output
        and '"options"' in output
        and '"correct_answer"' in output
        and "ONLY valid JSON" in output
        and "exactly 4 choices" in output
    )

    print("Expected:", expected)
    print("Got:", actual)
    assert actual is expected


def test_build_question_prompt_includes_recent_questions_block():
    recent_questions = [
        "What is the probability of heads in one fair coin toss?",
        "A die is rolled. What is P(rolling an even number)?",
    ]
    output = build_question_prompt("Probability", "MEDIUM", recent_questions)

    expected = True
    actual = (
        "Recent questions (DO NOT repeat or paraphrase these):" in output
        and "- What is the probability of heads in one fair coin toss?" in output
        and "- A die is rolled. What is P(rolling an even number)?" in output
        and "completely new and not similar" in output
    )

    print("Expected:", expected)
    print("Got:", actual)
    assert actual is expected


def test_build_explanation_prompt_contains_required_constraints():
    output = build_explanation_prompt(
        "What is P(A and B) for independent events?",
        "P(A)*P(B)",
    )

    expected = True
    actual = (
        "Question: What is P(A and B) for independent events?" in output
        and "Correct Answer: P(A)*P(B)" in output
        and '"explanation"' in output
        and "ONLY valid JSON" in output
    )

    print("Expected:", expected)
    print("Got:", actual)
    assert actual is expected


def run_all():
    test_build_question_prompt_contains_required_constraints()
    test_build_question_prompt_includes_recent_questions_block()
    test_build_explanation_prompt_contains_required_constraints()


if __name__ == "__main__":
    run_all()
