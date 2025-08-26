import io
import pytest
from PIL import Image


@pytest.fixture()
def sample_text() -> str:
    return "This is a sample document containing instructions for citizens."


@pytest.fixture()
def sample_png_bytes() -> bytes:
    img = Image.new("RGB", (60, 20), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue() 