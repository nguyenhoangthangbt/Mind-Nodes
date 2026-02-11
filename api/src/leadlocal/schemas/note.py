"""Note request/response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str


class NoteUpdate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
