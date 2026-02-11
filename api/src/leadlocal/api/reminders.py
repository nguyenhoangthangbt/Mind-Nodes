"""Reminders API routes."""

import uuid

from fastapi import APIRouter, Query

from leadlocal.core.dependencies import CurrentUser, DBSession
from leadlocal.schemas.reminder import ReminderCreate, ReminderResponse, ReminderUpdate
from leadlocal.services import reminder_service

router = APIRouter(tags=["reminders"])


@router.post(
    "/leads/{lead_id}/reminders", response_model=ReminderResponse, status_code=201
)
async def create_reminder(
    lead_id: uuid.UUID, data: ReminderCreate, user: CurrentUser, db: DBSession
):
    return await reminder_service.create_reminder(db, user, lead_id, data)


@router.get("/leads/{lead_id}/reminders", response_model=list[ReminderResponse])
async def list_lead_reminders(lead_id: uuid.UUID, user: CurrentUser, db: DBSession):
    return await reminder_service.list_reminders(db, user, lead_id=lead_id)


@router.get("/reminders", response_model=list[ReminderResponse])
async def list_all_reminders(
    user: CurrentUser,
    db: DBSession,
    upcoming: bool = Query(False),
):
    return await reminder_service.list_reminders(db, user, upcoming_only=upcoming)


@router.patch("/reminders/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: uuid.UUID, data: ReminderUpdate, user: CurrentUser, db: DBSession
):
    return await reminder_service.update_reminder(db, user, reminder_id, data)


@router.delete("/reminders/{reminder_id}", status_code=204)
async def delete_reminder(reminder_id: uuid.UUID, user: CurrentUser, db: DBSession):
    await reminder_service.delete_reminder(db, user, reminder_id)
