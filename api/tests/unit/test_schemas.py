"""Unit tests for Pydantic schemas — validation and serialization."""

import uuid

import pytest
from pydantic import ValidationError

from leadlocal.schemas.auth import LoginRequest, SignupRequest
from leadlocal.schemas.lead import LeadCreate, LeadUpdate, PipelineStats
from leadlocal.schemas.note import NoteCreate
from leadlocal.schemas.reminder import ReminderCreate
from leadlocal.schemas.search import SearchRequest, SearchResult


class TestAuthSchemas:
    def test_signup_valid(self):
        data = SignupRequest(
            email="user@test.com",
            password="strongpassword",
            full_name="John Doe",
            company="ACME",
        )
        assert data.email == "user@test.com"

    def test_signup_invalid_email(self):
        with pytest.raises(ValidationError):
            SignupRequest(
                email="not-an-email",
                password="pass123",
                full_name="Test",
            )

    def test_login_valid(self):
        data = LoginRequest(email="user@test.com", password="mypass")
        assert data.password == "mypass"


class TestLeadSchemas:
    def test_lead_create_minimal(self):
        data = LeadCreate(business_name="Test Biz")
        assert data.pipeline_stage == "new"
        assert data.source == "manual"
        assert data.tag_ids == []

    def test_lead_create_full(self):
        tag_id = uuid.uuid4()
        data = LeadCreate(
            business_name="Pizza Place",
            google_place_id="ChIJ123",
            address="123 Main St",
            phone="+1234567890",
            email="info@pizza.com",
            rating=4.5,
            tag_ids=[tag_id],
        )
        assert data.rating == 4.5
        assert data.tag_ids == [tag_id]

    def test_lead_update_partial(self):
        data = LeadUpdate(pipeline_stage="contacted")
        dumped = data.model_dump(exclude_unset=True)
        assert dumped == {"pipeline_stage": "contacted"}

    def test_pipeline_stats_defaults(self):
        stats = PipelineStats()
        assert stats.new == 0
        assert stats.won == 0


class TestSearchSchemas:
    def test_search_request_defaults(self):
        data = SearchRequest(query="restaurants")
        assert data.radius_meters == 5000
        assert data.source == "google_places"

    def test_search_result(self):
        result = SearchResult(business_name="Joe's", source="google_places")
        assert result.already_saved is False


class TestNoteSchemas:
    def test_note_create(self):
        data = NoteCreate(content="Follow up next week")
        assert data.content == "Follow up next week"


class TestReminderSchemas:
    def test_reminder_create(self):
        data = ReminderCreate(title="Call back", due_at="2025-03-01T10:00:00Z")
        assert data.title == "Call back"
