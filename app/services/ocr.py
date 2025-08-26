import io
import os
from typing import Optional, List

try:
	import fitz  # PyMuPDF
	_has_fitz = True
except Exception:
	fitz = None  # type: ignore
	_has_fitz = False

from PIL import Image
import pytesseract

try:
	from google.cloud import vision
	_has_vision = True
except Exception:
	_has_vision = False


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}


def _get_file_extension(filename: str) -> str:
	return os.path.splitext(filename or "")[1].lower()


def _render_pdf_to_images(file_bytes: bytes, dpi: int = 240) -> List[Image.Image]:
	if not _has_fitz:
		raise RuntimeError("PDF support requires PyMuPDF (fitz), which is not installed.")
	doc = fitz.open(stream=file_bytes, filetype="pdf")
	images: List[Image.Image] = []
	for page_index in range(len(doc)):
		page = doc.load_page(page_index)
		matrix = fitz.Matrix(dpi / 72, dpi / 72)
		pix = page.get_pixmap(matrix=matrix, alpha=False)
		img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
		images.append(img)
	doc.close()
	return images


def _tesseract_ocr_image(image: Image.Image, language_hint: Optional[str]) -> str:
	lang = language_hint or "eng"
	# Map simple language codes to Tesseract traineddata if needed
	lang_map = {
		"en": "eng",
		"hi": "hin",
		"mr": "mar",
		"bn": "ben",
		"ta": "tam",
		"te": "tel",
		"kn": "kan",
		"ml": "mal",
		"gu": "guj",
	}
	lang = lang_map.get(lang, lang)
	return pytesseract.image_to_string(image, lang=lang)


def _vision_ocr_image_bytes(image_bytes: bytes, language_hint: Optional[str]) -> str:
	if not _has_vision:
		raise RuntimeError("google-cloud-vision is not installed/configured")
	client = vision.ImageAnnotatorClient()
	image = vision.Image(content=image_bytes)
	# Use document_text_detection for better results on dense text
	response = client.document_text_detection(image=image, image_context={"language_hints": [language_hint]} if language_hint else None)
	if response.error.message:
		raise RuntimeError(response.error.message)
	return response.full_text_annotation.text or ""


def extract_text_from_file(file_bytes: bytes, filename: str, use_vision: bool = False, language_hint: Optional[str] = None) -> str:
	"""
	Extracts text from an uploaded file. Supports images and PDFs.
	- If use_vision is True and Google Vision is available, uses Vision for OCR.
	- Otherwise, uses Tesseract OCR.
	- For PDFs, pages are rendered with PyMuPDF and OCR is applied per page. If PyMuPDF is not available, PDF OCR is unavailable.
	"""
	ext = _get_file_extension(filename)

	if ext in SUPPORTED_IMAGE_EXTENSIONS:
		image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
		if use_vision:
			try:
				return _vision_ocr_image_bytes(file_bytes, language_hint)
			except Exception:
				# Fallback to Tesseract if Vision fails
				return _tesseract_ocr_image(image, language_hint)
		else:
			return _tesseract_ocr_image(image, language_hint)

	if ext in SUPPORTED_PDF_EXTENSIONS:
		try:
			images = _render_pdf_to_images(file_bytes)
		except Exception:
			# PDF support unavailable or failed
			return ""
		page_texts: List[str] = []
		for img in images:
			if use_vision:
				buf = io.BytesIO()
				img.save(buf, format="PNG")
				try:
					page_texts.append(_vision_ocr_image_bytes(buf.getvalue(), language_hint))
				except Exception:
					page_texts.append(_tesseract_ocr_image(img, language_hint))
			else:
				page_texts.append(_tesseract_ocr_image(img, language_hint))
		return "\n\n".join(page_texts).strip()

	raise ValueError(f"Unsupported file type: {ext}") 