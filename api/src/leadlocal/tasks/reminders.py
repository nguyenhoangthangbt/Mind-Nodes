"""Background tasks for reminder email notifications."""

import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from leadlocal.core.database import async_session_factory
from leadlocal.models.reminder import Reminder
from leadlocal.tasks.celery_app import celery_app


@celery_app.task(name="leadlocal.tasks.reminders.send_due_reminders")
def send_due_reminders():
    """Find reminders due within the next 5 minutes and send email notifications."""
    asyncio.get_event_loop().run_until_complete(_send_due_reminders())


async def _send_due_reminders():
    now = datetime.now(UTC)
    window = now + timedelta(minutes=5)

    async with async_session_factory() as db:
        result = await db.execute(
            select(Reminder).where(
                Reminder.is_completed == False,  # noqa: E712
                Reminder.due_at >= now,
                Reminder.due_at <= window,
            )
        )
        reminders = result.scalars().all()

        for reminder in reminders:
            # TODO: Send email via Resend when configured
            # For now, just log
            print(f"[Reminder] Due: {reminder.title} for lead {reminder.lead_id}")
