import re


def clean_extracted_text(text: str) -> str:
	if not text:
		return ""
	# Normalize whitespace and remove stray hyphenation artifacts common in OCR
	cleaned = text.replace("\r", "")
	cleaned = re.sub(r"[\t\f]+", " ", cleaned)
	cleaned = re.sub(r"\s+-\n\s*", "", cleaned)  # join broken words at line ends
	cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
	cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
	return cleaned.strip() 