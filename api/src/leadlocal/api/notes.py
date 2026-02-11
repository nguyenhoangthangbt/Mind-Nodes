"""Notes API routes — per-lead follow-up notes."""

import uuid

from fastapi import APIRouter

from leadlocal.core.dependencies import CurrentUser, DBSession
from leadlocal.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from leadlocal.services import note_service

router = APIRouter(prefix="/leads/{lead_id}/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(lead_id: uuid.UUID, data: NoteCreate, user: CurrentUser, db: DBSession):
    note = await note_service.create_note(db, user, lead_id, data.content)
    return note


@router.get("", response_model=list[NoteResponse])
async def list_notes(lead_id: uuid.UUID, user: CurrentUser, db: DBSession):
    return await note_service.list_notes(db, user, lead_id)


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: uuid.UUID, data: NoteUpdate, user: CurrentUser, db: DBSession):
    return await note_service.update_note(db, user, note_id, data.content)


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: uuid.UUID, user: CurrentUser, db: DBSession):
    await note_service.delete_note(db, user, note_id)
