import json
import os
from typing import List, Optional, Tuple

try:
	from openai import OpenAI
	_openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
	_client = None
	if os.getenv("OPENAI_API_KEY"):
		try:
			_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
		except Exception:
			_client = None
except Exception:
	OpenAI = None
	_client = None


from app.prompts import build_simplify_messages, build_checklist_messages, build_explain_notice_messages
from app.models.schemas import SimplifyResponse, ChecklistItem, ChecklistResponse, ExplainNoticeResponse


def _chat(messages: List[dict], response_format: Optional[str] = None, temperature: float = 0.2) -> str:
	if not _client:
		raise RuntimeError("OpenAI client not available. Set OPENAI_API_KEY environment variable.")
	completion = _client.chat.completions.create(
		model=_openai_model,
		messages=messages,
		temperature=temperature,
	)
	return completion.choices[0].message.content or ""


def simplify_text_with_llm(text: str, language: str = "en", reading_level: str = "basic", use_bullets: bool = True) -> SimplifyResponse:
	messages = build_simplify_messages(text=text, language=language, reading_level=reading_level, use_bullets=use_bullets)
	content = _chat(messages)
	return SimplifyResponse(
		language=language,
		reading_level=reading_level,
		text=content.strip(),
	)


def generate_checklist_with_llm(text: str, document_type: Optional[str] = None, context: Optional[str] = None) -> ChecklistResponse:
	messages = build_checklist_messages(text=text, document_type=document_type, context=context)
	content = _chat(messages)
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
		return ChecklistResponse(items=items, raw=content)
	except Exception:
		# Fallback: wrap the entire content as one item
		items.append(ChecklistItem(name="Checklist", description=content.strip(), mandatory=True, copies=1))
		return ChecklistResponse(items=items, raw=content)


def explain_notice_with_llm(text: str, language: str = "en") -> ExplainNoticeResponse:
	messages = build_explain_notice_messages(text=text, language=language)
	content = _chat(messages)
	# Heuristic parse into steps and next actions
	lines = [line.strip("-• ").strip() for line in content.splitlines() if line.strip()]
	steps: List[str] = []
	actions: List[str] = []
	in_actions = False
	for line in lines:
		lower = line.lower()
		if lower.startswith("next steps") or lower.startswith("what to do") or lower.startswith("actions"):
			in_actions = True
			continue
		if in_actions:
			actions.append(line)
		else:
			steps.append(line)
	return ExplainNoticeResponse(language=language, steps=steps, next_actions=actions) 