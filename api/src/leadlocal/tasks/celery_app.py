"""Celery application configuration."""

from celery import Celery

from leadlocal.core.config import settings

celery_app = Celery(
    "leadlocal",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    beat_schedule={
        "send-reminder-emails": {
            "task": "leadlocal.tasks.reminders.send_due_reminders",
            "schedule": 300.0,  # every 5 minutes
        },
    },
)
