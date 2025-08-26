from app.services import llm


def test_simplify_uses_bullets(monkeypatch, sample_text):
    monkeypatch.setattr(llm, "_chat", lambda messages, response_format=None, temperature=0.2: "- Point A\n- Point B")

    resp = llm.simplify_text_with_llm(sample_text, language="en", reading_level="basic", use_bullets=True)
    assert resp.language == "en"
    assert resp.text.startswith("- ")


def test_checklist_parses_json(monkeypatch):
    mocked_json = '{"items":[{"name":"PAN Card","description":"Copy of PAN","mandatory":true,"copies":1,"source":"user"}]}'
    monkeypatch.setattr(llm, "_chat", lambda messages, response_format=None, temperature=0.2: mocked_json)

    resp = llm.generate_checklist_with_llm("text", document_type="Demo", context="student")
    assert len(resp.items) == 1
    item = resp.items[0]
    assert item.name == "PAN Card"
    assert item.mandatory is True
    assert item.copies == 1 