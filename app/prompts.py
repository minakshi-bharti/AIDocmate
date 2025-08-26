from typing import List, Optional


def build_simplify_messages(text: str, language: str = "en", reading_level: str = "basic", use_bullets: bool = True) -> List[dict]:
	style = "bullet points" if use_bullets else "short paragraphs"
	return [
		{
			"role": "system",
			"content": (
				"You are AIDocMate, an assistant that simplifies Indian government and legal documents for citizens. "
				"Explain in plain language, avoid jargon, and keep facts accurate. If there is uncertainty, state it clearly."
			),
		},
		{
			"role": "user",
			"content": (
				f"Simplify the following text for a {reading_level} reader in language code '{language}'. "
				f"Use {style}. Include key actions, deadlines, eligibility, and required fees/documents if present.\n\n{text}"
			),
		},
	]


def build_explain_notice_messages(text: str, language: str = "en") -> List[dict]:
	return [
		{"role": "system", "content": "You explain legal/government notices step-by-step in clear plain language for Indian citizens."},
		{"role": "user", "content": f"Explain this notice step-by-step in '{language}' and list next steps and deadlines:\n\n{text}"},
	]


def build_checklist_messages(text: str, document_type: Optional[str] = None, context: Optional[str] = None) -> List[dict]:
	context_str = f" for {context}" if context else ""
	doc_str = f" ({document_type})" if document_type else ""
	instruction = (
		"Produce a JSON object with an 'items' array. Each item must have: "
		"name (string), description (string), mandatory (boolean), copies (integer), source (string, if applicable), notes (string, optional). "
		"Only output valid JSON."
	)
	return [
		{"role": "system", "content": "You generate precise checklists for Indian government/legal procedures."},
		{"role": "user", "content": f"Create a checklist{context_str}{doc_str}. {instruction} Text:\n\n{text}"},
	] 