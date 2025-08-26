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
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		print("[llm] OPENAI_API_KEY not set")
		return None
	
	try:
		if _client is None:
			_client = OpenAI(api_key=api_key)
			print(f"[llm] OpenAI client initialized with model: {_openai_model}")
		return _client
	except Exception as e:
		print(f"[llm] Failed to initialize OpenAI client: {e}")
		_client = None
		return None


from app.prompts import build_simplify_messages, build_checklist_messages, build_explain_notice_messages
from app.models.schemas import SimplifyResponse, ChecklistItem, ChecklistResponse, ExplainNoticeResponse


def _chat(messages: List[dict], response_format: Optional[str] = None, temperature: float = 0.2) -> str:
	client = _get_openai_client()
	if not client:
		raise RuntimeError("OpenAI client not available. Set OPENAI_API_KEY environment variable.")
	
	print(f"[llm._chat] invoking OpenAI with {len(messages)} messages")
	print(f"[llm._chat] first 100 chars of user message: {messages[-1]['content'][:100]}...")
	
	try:
		completion = client.chat.completions.create(
			model=_openai_model,
			messages=messages,
			temperature=temperature,
		)
		content = completion.choices[0].message.content or ""
		print(f"[llm._chat] response length = {len(content)}")
		print(f"[llm._chat] first 100 chars of response: {content[:100]}...")
		return content
	except Exception as e:
		print(f"[llm._chat] OpenAI API call failed: {e}")
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
		print(f"[llm.simplify] OpenAI API failed: {e}")
		return SimplifyResponse(language=language, reading_level=reading_level, text="The AI service could not process this request. Please try again later.")


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
		print(f"[llm.checklist] OpenAI API failed: {e}")
		return ChecklistResponse(items=[ChecklistItem(name="Error", description="The AI service could not process this request. Please try again later.", mandatory=True, copies=1)])


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
		print(f"[llm.explain] OpenAI API failed: {e}")
		return ExplainNoticeResponse(language=language, steps=["The AI service could not process this request. Please try again later."], next_actions=[])


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
		print(f"[llm.translate] OpenAI API failed: {e}")
		return "The AI service could not process this request. Please try again later."