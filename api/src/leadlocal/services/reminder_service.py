"""Reminder CRUD service."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from leadlocal.core.exceptions import NotFoundError
from leadlocal.models.reminder import Reminder
from leadlocal.models.user import User
from leadlocal.schemas.reminder import ReminderCreate, ReminderUpdate
from leadlocal.services.lead_service import get_lead


async def create_reminder(
    db: AsyncSession, user: User, lead_id: uuid.UUID, data: ReminderCreate
) -> Reminder:
    await get_lead(db, user, lead_id)
    reminder = Reminder(
        lead_id=lead_id,
        user_id=user.id,
        title=data.title,
        description=data.description,
        due_at=data.due_at,
    )
    db.add(reminder)
    await db.flush()
    return reminder


async def list_reminders(
    db: AsyncSession,
    user: User,
    lead_id: uuid.UUID | None = None,
    upcoming_only: bool = False,
) -> list[Reminder]:
    query = select(Reminder).where(Reminder.user_id == user.id)
    if lead_id:
        query = query.where(Reminder.lead_id == lead_id)
    if upcoming_only:
        query = query.where(
            Reminder.is_completed == False,  # noqa: E712
            Reminder.due_at >= datetime.now(UTC),
        )
    query = query.order_by(Reminder.due_at.asc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_reminder(
    db: AsyncSession, user: User, reminder_id: uuid.UUID, data: ReminderUpdate
) -> Reminder:
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == user.id)
    )
    reminder = result.scalar_one_or_none()
    if not reminder:
        raise NotFoundError("Reminder")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reminder, field, value)
    await db.flush()
    return reminder


async def delete_reminder(db: AsyncSession, user: User, reminder_id: uuid.UUID) -> None:
    result = await db.execute(
        select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == user.id)
    )
    reminder = result.scalar_one_or_none()
    if not reminder:
        raise NotFoundError("Reminder")
    await db.delete(reminder)
