import os

import engines.ai_generation.llm_client as llm_client


class MockResponse:
    def __init__(self, json_data, should_raise=False):
        self._json_data = json_data
        self._should_raise = should_raise

    def raise_for_status(self):
        if self._should_raise:
            raise RuntimeError("HTTP error")

    def json(self):
        return self._json_data


def test_generate_text_success_first_try():
    original_post = llm_client.requests.post
    original_key = os.environ.get("HF_API_KEY")

    os.environ["HF_API_KEY"] = "test_key"

    def mock_post(url, headers, json, timeout):
        return MockResponse([{"generated_text": "LLM output"}])

    llm_client.requests.post = mock_post

    output = llm_client.generate_text("Prompt", 0.2, 128)
    expected = "LLM output"

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    llm_client.requests.post = original_post
    if original_key is None:
        del os.environ["HF_API_KEY"]
    else:
        os.environ["HF_API_KEY"] = original_key


def test_generate_text_success_chat_completion_shape():
    original_post = llm_client.requests.post
    original_key = os.environ.get("HF_API_KEY")

    os.environ["HF_API_KEY"] = "test_key"

    def mock_post(url, headers, json, timeout):
        return MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Chat completion output"
                        }
                    }
                ]
            }
        )

    llm_client.requests.post = mock_post

    output = llm_client.generate_text("Prompt", 0.2, 128)
    expected = "Chat completion output"

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    llm_client.requests.post = original_post
    if original_key is None:
        del os.environ["HF_API_KEY"]
    else:
        os.environ["HF_API_KEY"] = original_key


def test_generate_text_retries_then_success():
    original_post = llm_client.requests.post
    original_key = os.environ.get("HF_API_KEY")

    os.environ["HF_API_KEY"] = "test_key"

    call_count = {"value": 0}

    def mock_post(url, headers, json, timeout):
        call_count["value"] += 1
        if call_count["value"] < 3:
            raise RuntimeError("temporary failure")
        return MockResponse([{"generated_text": "Recovered output"}])

    llm_client.requests.post = mock_post

    output = llm_client.generate_text("Prompt", 0.2, 128)
    expected_output = "Recovered output"
    expected_attempts = 3

    print("Expected:", expected_output)
    print("Got:", output)
    assert output == expected_output

    print("Expected:", expected_attempts)
    print("Got:", call_count["value"])
    assert call_count["value"] == expected_attempts

    llm_client.requests.post = original_post
    if original_key is None:
        del os.environ["HF_API_KEY"]
    else:
        os.environ["HF_API_KEY"] = original_key


def test_generate_text_fails_after_three_attempts():
    original_post = llm_client.requests.post
    original_key = os.environ.get("HF_API_KEY")

    os.environ["HF_API_KEY"] = "test_key"

    call_count = {"value": 0}

    def mock_post(url, headers, json, timeout):
        call_count["value"] += 1
        raise RuntimeError("persistent failure")

    llm_client.requests.post = mock_post

    expected_error_type = "RuntimeError"
    actual_error_type = "None"

    try:
        llm_client.generate_text("Prompt", 0.2, 128)
    except Exception as error:
        actual_error_type = type(error).__name__

    print("Expected:", expected_error_type)
    print("Got:", actual_error_type)
    assert actual_error_type == expected_error_type

    expected_attempts = 3
    print("Expected:", expected_attempts)
    print("Got:", call_count["value"])
    assert call_count["value"] == expected_attempts

    llm_client.requests.post = original_post
    if original_key is None:
        del os.environ["HF_API_KEY"]
    else:
        os.environ["HF_API_KEY"] = original_key


def run_all():
    test_generate_text_success_first_try()
    test_generate_text_success_chat_completion_shape()
    test_generate_text_retries_then_success()
    test_generate_text_fails_after_three_attempts()


if __name__ == "__main__":
    run_all()
