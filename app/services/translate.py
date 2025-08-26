import os
from typing import Tuple

_target_location = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")
_project_id = os.getenv("GOOGLE_PROJECT_ID")
_use_fallback = os.getenv("USE_TRANSLATE_FALLBACK", "false").lower() in {"1", "true", "yes"}

try:
	from google.cloud import translate
	_has_translate = True
except Exception:
	_has_translate = False

try:
	from googletrans import Translator as _GTTranslator  # type: ignore
	_has_googletrans = True
except Exception:
	_has_googletrans = False


def translate_text_with_provider(text: str, target_language: str) -> Tuple[str, str]:
	# Prefer GCP Translate if credentials/project are configured
	if _has_translate and _project_id:
		client = translate.TranslationServiceClient()
		parent = f"projects/{_project_id}/locations/{_target_location}"
		response = client.translate_text(
			request={
				"parent": parent,
				"contents": [text],
				"mime_type": "text/plain",
				"target_language_code": target_language,
			}
		)
		translated_text = "".join([t.translated_text for t in response.translations])
		return translated_text, "google-cloud-translate"

	# Optional fallback: googletrans (no API key) - not guaranteed accuracy
	if _use_fallback and _has_googletrans:
		translator = _GTTranslator()
		translated = translator.translate(text, dest=target_language)
		return translated.text, "googletrans"

	raise RuntimeError("Translation provider not configured. Set GOOGLE_PROJECT_ID for Google Cloud or enable USE_TRANSLATE_FALLBACK=true.") 