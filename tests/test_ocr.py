import io
from PIL import Image
from app.services import ocr


def test_extract_text_from_png_tesseract(monkeypatch, sample_png_bytes):
    def fake_image_to_string(image, lang=None):
        return "Hello OCR"

    monkeypatch.setattr(ocr.pytesseract, "image_to_string", fake_image_to_string)

    text = ocr.extract_text_from_file(sample_png_bytes, filename="doc.png", use_vision=False, language_hint="en")
    assert text == "Hello OCR"


def test_extract_text_from_pdf_tesseract(monkeypatch):
    images = [Image.new("RGB", (10, 10), color="white")]
    monkeypatch.setattr(ocr, "_render_pdf_to_images", lambda fb, dpi=240: images)
    monkeypatch.setattr(ocr.pytesseract, "image_to_string", lambda img, lang=None: "Page 1")

    text = ocr.extract_text_from_file(b"%PDF-1.7 fake bytes%", filename="doc.pdf", use_vision=False, language_hint="en")
    assert text == "Page 1" 