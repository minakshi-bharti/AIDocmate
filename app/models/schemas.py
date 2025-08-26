from typing import List, Optional
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
	request_id: str
	filename: Optional[str]
	text: str


class SimplifyRequest(BaseModel):
	text: str = Field(..., min_length=1, description="Raw text extracted from the document")
	language: str = Field(default="en", min_length=2, max_length=10, description="Language for simplified output (e.g., 'en' or 'hi')")
	reading_level: str = Field(default="basic", description="Reading level: basic, intermediate, advanced")
	use_bullets: bool = Field(default=True, description="Return bullet-point summary")


class SimplifyResponse(BaseModel):
	language: str
	reading_level: str
	text: str


class TranslateRequest(BaseModel):
	text: str = Field(..., min_length=1)
	target_language: str = Field(..., min_length=2, max_length=10, description="Target language code, e.g., 'hi' or 'mr'")


class TranslateResponse(BaseModel):
	text: str
	target_language: str
	provider: str


class ChecklistRequest(BaseModel):
	text: str = Field(..., min_length=1)
	document_type: Optional[str] = Field(default=None, description="e.g., 'PAN Application', 'Scholarship Form'")
	context: Optional[str] = Field(default=None, description="User context: student, farmer, job seeker, etc.")


class ChecklistItem(BaseModel):
	name: str
	description: Optional[str] = None
	mandatory: bool = True
	source: Optional[str] = None
	copies: int = 1
	notes: Optional[str] = None


class ChecklistResponse(BaseModel):
	items: List[ChecklistItem]
	raw: Optional[str] = None


class ExplainNoticeRequest(BaseModel):
	text: str = Field(..., min_length=1)
	language: str = Field(default="en", min_length=2, max_length=10, description="Target language code for explanation")


class ExplainNoticeResponse(BaseModel):
	language: str
	steps: List[str]
	next_actions: List[str] 