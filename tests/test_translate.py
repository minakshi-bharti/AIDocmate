from app.services import translate as tr


def test_translate_uses_fallback_googletrans(monkeypatch):
    class _DummyTranslator:
        def translate(self, text, dest=None):
            class R:
                pass
            r = R()
            r.text = "नमस्ते"
            return r

    # Force fallback path
    monkeypatch.setattr(tr, "_has_translate", False, raising=False)
    monkeypatch.setattr(tr, "_use_fallback", True, raising=False)
    monkeypatch.setattr(tr, "_has_googletrans", True, raising=False)
    monkeypatch.setattr(tr, "_GTTranslator", lambda: _DummyTranslator(), raising=False)

    out, provider = tr.translate_text_with_provider("Hello", "hi")
    assert out == "नमस्ते"
    assert provider == "googletrans" 