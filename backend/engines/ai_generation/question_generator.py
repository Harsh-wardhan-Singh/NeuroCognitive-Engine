import json
from engines.ai_generation.llm_client import generate_text
from engines.ai_generation.prompt_templates import build_question_prompt

QUESTION_TEMPERATURE = 0.7
QUESTION_MAX_TOKENS = 256
MAX_PARSE_VALIDATION_ATTEMPTS = 2


def _validate_question_payload(payload):
	if not isinstance(payload, dict):
		raise ValueError("LLM output must be a JSON object.")
	if "question" not in payload:
		raise ValueError("Missing 'question' key.")
	if "options" not in payload:
		raise ValueError("Missing 'options' key.")
	if "correct_answer" not in payload:
		raise ValueError("Missing 'correct_answer' key.")
	if not isinstance(payload["question"], str):
		raise ValueError("'question' must be a string.")
	if not isinstance(payload["options"], list):
		raise ValueError("'options' must be a list.")
	if len(payload["options"]) != 4:
		raise ValueError("'options' must have length 4.")
	if not all(isinstance(item, str) for item in payload["options"]):
		raise ValueError("All items in 'options' must be strings.")
	if not isinstance(payload["correct_answer"], str):
		raise ValueError("'correct_answer' must be a string.")
	if payload["correct_answer"] not in payload["options"]:
		raise ValueError("'correct_answer' must match one option.")


def generate_question(concept, difficulty, previous_questions):
	last_error = None
	for _ in range(MAX_PARSE_VALIDATION_ATTEMPTS):
		try:
			prompt = build_question_prompt(concept, difficulty, previous_questions)
			raw_output = generate_text(prompt, QUESTION_TEMPERATURE, QUESTION_MAX_TOKENS)
			parsed_output = json.loads(raw_output)
			_validate_question_payload(parsed_output)
			if parsed_output["question"] in previous_questions:
				raise ValueError("Generated question repeats a recent question.")
			return {
				"question": parsed_output["question"],
				"options": parsed_output["options"],
				"correct_answer": parsed_output["correct_answer"],
			}
		except Exception as error:
			last_error = error
	raise RuntimeError(f"Failed to generate valid question output: {last_error}")
