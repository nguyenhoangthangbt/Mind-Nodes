"""Background tasks for reminder email notifications."""

import asyncio
import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from leadlocal.core.database import async_session_factory
from leadlocal.models.lead import Lead
from leadlocal.models.reminder import Reminder
from leadlocal.models.user import User
from leadlocal.services.email_service import send_reminder_email
from leadlocal.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


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
            # Fetch user and lead for email content
            user_result = await db.execute(select(User).where(User.id == reminder.user_id))
            user = user_result.scalar_one_or_none()

            lead_result = await db.execute(select(Lead).where(Lead.id == reminder.lead_id))
            lead = lead_result.scalar_one_or_none()

            if user and lead:
                sent = await send_reminder_email(
                    to_email=user.email,
                    user_name=user.full_name,
                    reminder_title=reminder.title,
                    lead_name=lead.business_name,
                    due_at=reminder.due_at.strftime("%b %d, %Y at %I:%M %p"),
                )
                if sent:
                    logger.info("Reminder email sent: %s → %s", reminder.title, user.email)
                else:
                    logger.warning(
                        "Reminder email skipped (no Resend key): %s → %s",
                        reminder.title,
                        user.email,
                    )
