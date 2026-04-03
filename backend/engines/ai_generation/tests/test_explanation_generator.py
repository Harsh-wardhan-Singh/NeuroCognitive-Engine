import engines.ai_generation.explanation_generator as explanation_generator


def test_generate_explanation_valid_json():
    original_generate_text = explanation_generator.generate_text

    def mock_generate_text(prompt, temperature, max_tokens):
        return '{"explanation":"Because independent events multiply: P(A and B)=P(A)*P(B)."}'

    explanation_generator.generate_text = mock_generate_text

    question = "How do you compute P(A and B) for independent events?"
    correct_answer = "P(A)*P(B)"

    output = explanation_generator.generate_explanation(question, correct_answer)
    expected = {
        "explanation": "Because independent events multiply: P(A and B)=P(A)*P(B)."
    }

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    explanation_generator.generate_text = original_generate_text


def test_generate_explanation_parse_failure_fallback():
    original_generate_text = explanation_generator.generate_text

    def mock_generate_text(prompt, temperature, max_tokens):
        return "not-json"

    explanation_generator.generate_text = mock_generate_text

    question = "How do you compute P(A and B) for independent events?"
    correct_answer = "P(A)*P(B)"

    output = explanation_generator.generate_explanation(question, correct_answer)
    expected = {"explanation": "Explanation unavailable."}

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    explanation_generator.generate_text = original_generate_text


def run_all():
    test_generate_explanation_valid_json()
    test_generate_explanation_parse_failure_fallback()


if __name__ == "__main__":
    run_all()
