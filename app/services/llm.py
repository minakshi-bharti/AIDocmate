import json
import os
from typing import List, Optional, Tuple

try:
	from openai import OpenAI
	_openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
except Exception:
	OpenAI = None
	_openai_model = "gpt-4o-mini"

_client = None


def _get_openai_client():
	"""Get or create OpenAI client with current API key"""
	global _client
	print(f"[llm] _get_openai_client() called")
	
	# Check if OpenAI module is available
	if OpenAI is None:
		print("[llm] ERROR: OpenAI module not available")
		return None
	
	api_key = os.getenv("OPENAI_API_KEY")
	print(f"[llm] Checking OPENAI_API_KEY: {'SET' if api_key else 'NOT SET'}")
	if api_key:
		print(f"[llm] API key length: {len(api_key)}")
		print(f"[llm] API key preview: {api_key[:10]}...")
		print(f"[llm] API key starts with 'sk-': {api_key.startswith('sk-')}")
	else:
		print("[llm] OPENAI_API_KEY not set")
		print(f"[llm] All environment variables: {list(os.environ.keys())}")
		# Try to find any key that might contain 'openai' or 'api'
		for key in os.environ.keys():
			if 'openai' in key.lower() or 'api' in key.lower():
				print(f"[llm] Found related env var: {key} = {os.environ[key][:10]}...")
		return None
	
	try:
		if _client is None:
			print(f"[llm] Creating new OpenAI client with model: {_openai_model}")
			_client = OpenAI(api_key=api_key)
			print(f"[llm] OpenAI client initialized successfully")
		else:
			print(f"[llm] Using existing OpenAI client")
		return _client
	except Exception as e:
		print(f"[llm] Failed to initialize OpenAI client: {e}")
		print(f"[llm] Error type: {type(e).__name__}")
		print(f"[llm] Error details: {str(e)}")
		_client = None
		return None


from app.prompts import build_simplify_messages, build_checklist_messages, build_explain_notice_messages
from app.models.schemas import SimplifyResponse, ChecklistItem, ChecklistResponse, ExplainNoticeResponse


def _chat(messages: List[dict], response_format: Optional[str] = None, temperature: float = 0.2) -> str:
	client = _get_openai_client()
	if not client:
		# Provide more detailed error information
		api_key = os.getenv("OPENAI_API_KEY")
		error_msg = f"OpenAI client not available. "
		if not api_key:
			error_msg += "OPENAI_API_KEY environment variable is not set."
		elif OpenAI is None:
			error_msg += "OpenAI module failed to import."
		else:
			error_msg += "Client initialization failed."
		
		print(f"[llm._chat] {error_msg}")
		raise RuntimeError(error_msg)
	
	print(f"[llm._chat] invoking OpenAI with {len(messages)} messages")
	print(f"[llm._chat] model: {_openai_model}")
	print(f"[llm._chat] temperature: {temperature}")
	print(f"[llm._chat] first 100 chars of user message: {messages[-1]['content'][:100]}...")
	
	try:
		print(f"[llm._chat] Making OpenAI API call...")
		completion = client.chat.completions.create(
			model=_openai_model,
			messages=messages,
			temperature=temperature,
		)
		content = completion.choices[0].message.content or ""
		print(f"[llm._chat] API call successful!")
		print(f"[llm._chat] response length = {len(content)}")
		print(f"[llm._chat] first 100 chars of response: {content[:100]}...")
		return content
	except Exception as e:
		print(f"[llm._chat] OpenAI API call failed!")
		print(f"[llm._chat] Error type: {type(e).__name__}")
		print(f"[llm._chat] Error message: {e}")
		print(f"[llm._chat] Full error details: {str(e)}")
		
		# Try with a fallback model if the main one fails
		if "gpt-4o-mini" in _openai_model and "gpt-3.5-turbo" not in _openai_model:
			print(f"[llm._chat] Trying fallback model: gpt-3.5-turbo")
			try:
				completion = client.chat.completions.create(
					model="gpt-3.5-turbo",
					messages=messages,
					temperature=temperature,
				)
				content = completion.choices[0].message.content or ""
				print(f"[llm._chat] Fallback model successful!")
				print(f"[llm._chat] response length = {len(content)}")
				return content
			except Exception as fallback_error:
				print(f"[llm._chat] Fallback model also failed: {fallback_error}")
		
		raise


def simplify_text_with_llm(text: str, language: str = "en", reading_level: str = "basic", use_bullets: bool = True) -> SimplifyResponse:
	if not text or not text.strip():
		print("[llm.simplify] No text provided")
		return SimplifyResponse(language=language, reading_level=reading_level, text="No text available for processing.")
	
	print(f"[llm.simplify] input length = {len(text)}")
	print(f"[llm.simplify] first 100 chars: {text[:100]}...")
	
	try:
		messages = build_simplify_messages(text=text, language=language, reading_level=reading_level, use_bullets=use_bullets)
		content = _chat(messages)
		result = SimplifyResponse(
			language=language,
			reading_level=reading_level,
			text=(content or "").strip(),
		)
		print(f"[llm.simplify] success - result length: {len(result.text)}")
		return result
	except Exception as e:
		error_msg = f"OpenAI API failed: {type(e).__name__} - {str(e)}"
		print(f"[llm.simplify] {error_msg}")
		return SimplifyResponse(language=language, reading_level=reading_level, text=f"AI processing failed: {type(e).__name__}. Please check your API key and try again.")


def generate_checklist_with_llm(text: str, document_type: Optional[str] = None, context: Optional[str] = None) -> ChecklistResponse:
	if not text or not text.strip():
		print("[llm.checklist] No text provided")
		return ChecklistResponse(items=[ChecklistItem(name="Info", description="No text available for processing.", mandatory=True, copies=1)])
	
	print(f"[llm.checklist] input length = {len(text)}")
	print(f"[llm.checklist] first 100 chars: {text[:100]}...")
	
	try:
		messages = build_checklist_messages(text=text, document_type=document_type, context=context)
		content = _chat(messages)
		print(f"[llm.checklist] raw response length = {len(content)}")
		
		# Expect JSON; attempt to parse; if fails, return as free text item
		items: List[ChecklistItem] = []
		try:
			payload = json.loads(content)
			for raw in payload.get("items", []):
				items.append(ChecklistItem(
					name=raw.get("name", ""),
					description=raw.get("description"),
					mandatory=bool(raw.get("mandatory", True)),
					source=raw.get("source"),
					copies=int(raw.get("copies", 1)),
					notes=raw.get("notes"),
				))
			result = ChecklistResponse(items=items, raw=content)
			print(f"[llm.checklist] success - parsed {len(items)} items")
			return result
		except Exception as parse_error:
			print(f"[llm.checklist] JSON parse failed, using raw content: {parse_error}")
			# Fallback: wrap the entire content as one item
			items.append(ChecklistItem(name="Checklist", description=(content or "").strip(), mandatory=True, copies=1))
			result = ChecklistResponse(items=items, raw=content)
			print(f"[llm.checklist] fallback success - 1 item")
			return result
	except Exception as e:
		error_msg = f"OpenAI API failed: {type(e).__name__} - {str(e)}"
		print(f"[llm.checklist] {error_msg}")
		return ChecklistResponse(items=[ChecklistItem(name="Error", description=f"AI processing failed: {type(e).__name__}. Please check your API key and try again.", mandatory=True, copies=1)])


def explain_notice_with_llm(text: str, language: str = "en") -> ExplainNoticeResponse:
	if not text or not text.strip():
		print("[llm.explain] No text provided")
		return ExplainNoticeResponse(language=language, steps=["No text available for processing."], next_actions=[])
	
	print(f"[llm.explain] input length = {len(text)}")
	print(f"[llm.explain] first 100 chars: {text[:100]}...")
	
	try:
		messages = build_explain_notice_messages(text=text, language=language)
		content = _chat(messages)
		
		# Heuristic parse into steps and next actions
		lines = [line.strip("-• ").strip() for line in (content or "").splitlines() if line.strip()]
		steps: List[str] = []
		actions: List[str] = []
		in_actions = False
		for line in lines:
			lower = line.strip().lower()
			if lower.startswith("next steps") or lower.startswith("what to do") or lower.startswith("actions"):
				in_actions = True
				continue
			if in_actions:
				actions.append(line)
			else:
				steps.append(line)
		
		result = ExplainNoticeResponse(language=language, steps=steps, next_actions=actions)
		print(f"[llm.explain] success - {len(steps)} steps, {len(actions)} actions")
		return result
	except Exception as e:
		error_msg = f"OpenAI API failed: {type(e).__name__} - {str(e)}"
		print(f"[llm.explain] {error_msg}")
		return ExplainNoticeResponse(language=language, steps=[f"AI processing failed: {type(e).__name__}. Please check your API key and try again."], next_actions=[])


def translate_text_with_llm(text: str, target_language: str = "hi") -> str:
	if not text or not text.strip():
		print("[llm.translate] No text provided")
		return "No text available for processing."
	
	print(f"[llm.translate] input length = {len(text)} target={target_language}")
	print(f"[llm.translate] first 100 chars: {text[:100]}...")
	
	try:
		messages = [
			{"role": "system", "content": "You are a helpful translator. Translate the user's input into the requested target language without adding extra commentary."},
			{"role": "user", "content": f"Translate the following text into {target_language}.\n\n{text}"},
		]
		content = _chat(messages)
		result = (content or "").strip()
		print(f"[llm.translate] success - result length: {len(result)}")
		return result
	except Exception as e:
		error_msg = f"OpenAI API failed: {type(e).__name__} - {str(e)}"
		print(f"[llm.translate] {error_msg}")
		return f"AI processing failed: {type(e).__name__}. Please check your API key and try again."


def test_environment():
	"""Test function to debug environment variable issues"""
	print("=== LLM Environment Test ===")
	print(f"OpenAI module available: {OpenAI is not None}")
	print(f"OpenAI model: {_openai_model}")
	
	api_key = os.getenv("OPENAI_API_KEY")
	print(f"OPENAI_API_KEY set: {bool(api_key)}")
	if api_key:
		print(f"API key length: {len(api_key)}")
		print(f"API key preview: {api_key[:10]}...")
		print(f"API key starts with 'sk-': {api_key.startswith('sk-')}")
	
	# Test client creation
	try:
		client = _get_openai_client()
		if client:
			print("✅ OpenAI client created successfully")
		else:
			print("❌ OpenAI client creation failed")
	except Exception as e:
		print(f"❌ Error creating client: {e}")
	
	print("=== End Test ===")
	return {
		"openai_available": OpenAI is not None,
		"api_key_set": bool(api_key),
		"api_key_length": len(api_key) if api_key else 0,
		"client_created": _get_openai_client() is not None
	}