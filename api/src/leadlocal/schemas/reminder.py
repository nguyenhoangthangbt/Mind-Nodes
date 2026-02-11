"""Reminder request/response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class ReminderCreate(BaseModel):
    title: str
    description: str | None = None
    due_at: datetime


class ReminderUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_at: datetime | None = None
    is_completed: bool | None = None


class ReminderResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    title: str
    description: str | None
    due_at: datetime
    is_completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}
