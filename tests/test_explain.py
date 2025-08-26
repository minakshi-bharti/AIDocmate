from app.services import llm


def test_explain_notice_parses_steps_and_actions(monkeypatch):
    content = """
    Step 1: Read the notice carefully
    Step 2: Collect documents
    Next steps:
    - Submit by 31 March
    - Visit the nearest office
    """
    monkeypatch.setattr(llm, "_chat", lambda messages, response_format=None, temperature=0.2: content)

    resp = llm.explain_notice_with_llm("text", language="en")
    assert any("Read the notice" in s for s in resp.steps)
    assert any("Submit" in a for a in resp.next_actions) 