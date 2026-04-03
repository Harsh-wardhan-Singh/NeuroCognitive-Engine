import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
MAX_RETRIES = 3
REQUEST_TIMEOUT_SECONDS = 30
def _extract_raw_text(response_json):
	if isinstance(response_json, dict):
		choices = response_json.get("choices")
		if isinstance(choices, list) and len(choices) > 0:
			first_choice = choices[0]
			if isinstance(first_choice, dict):
				message = first_choice.get("message")
				if isinstance(message, dict):
					content = message.get("content")
					if isinstance(content, str):
						return content
	if isinstance(response_json, str):
		return response_json
	if isinstance(response_json, list) and len(response_json) > 0:
		first_item = response_json[0]
		if isinstance(first_item, dict):
			generated_text = first_item.get("generated_text")
			if isinstance(generated_text, str):
				return generated_text
	if isinstance(response_json, dict):
		generated_text = response_json.get("generated_text")
		if isinstance(generated_text, str):
			return generated_text
	raise ValueError("Unexpected LLM response format.")
def generate_text(prompt, temperature, max_tokens):
	api_key = os.getenv("HF_API_KEY")
	if not api_key:
		raise ValueError("Missing HF_API_KEY in environment.")
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json",
	}
	payload = {
		"model": HF_MODEL,
		"messages": [
			{
				"role": "user",
				"content": prompt,
			}
		],
		"temperature": temperature,
		"max_tokens": max_tokens,
		"stream": False,
	}
	last_error = None
	for attempt in range(MAX_RETRIES):
		try:
			response = requests.post(
				HF_API_URL,
				headers=headers,
				json=payload,
				timeout=REQUEST_TIMEOUT_SECONDS,
			)
			response.raise_for_status()
			response_json = response.json()
			return _extract_raw_text(response_json)
		except Exception as error:
			last_error = error
			if attempt < MAX_RETRIES - 1:
				time.sleep(0.2)
	raise RuntimeError(f"LLM API request failed after {MAX_RETRIES} attempts: {last_error}")
