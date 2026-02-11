"""Note CRUD service."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.exceptions import NotFoundError
from leadlocal.models.note import Note
from leadlocal.models.user import User
from leadlocal.services.lead_service import get_lead


async def create_note(
    db: AsyncSession, user: User, lead_id: uuid.UUID, content: str
) -> Note:
    await get_lead(db, user, lead_id)  # Verify ownership
    note = Note(lead_id=lead_id, user_id=user.id, content=content)
    db.add(note)
    await db.flush()
    return note


async def list_notes(db: AsyncSession, user: User, lead_id: uuid.UUID) -> list[Note]:
    await get_lead(db, user, lead_id)
    result = await db.execute(
        select(Note).where(Note.lead_id == lead_id).order_by(Note.created_at.desc())
    )
    return list(result.scalars().all())


async def update_note(
    db: AsyncSession, user: User, note_id: uuid.UUID, content: str
) -> Note:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == user.id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise NotFoundError("Note")
    note.content = content
    await db.flush()
    return note


async def delete_note(db: AsyncSession, user: User, note_id: uuid.UUID) -> None:
    result = await db.execute(
        select(Note).where(Note.id == note_id, Note.user_id == user.id)
    )
    note = result.scalar_one_or_none()
    if not note:
        raise NotFoundError("Note")
    await db.delete(note)
