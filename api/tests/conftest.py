"""Shared test fixtures — in-memory SQLite async database + FastAPI test client."""

import asyncio
import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from leadlocal.core.database import Base, get_db
from leadlocal.core.security import create_access_token, hash_password
from leadlocal.main import app
from leadlocal.models.lead import Lead
from leadlocal.models.user import User

# Use async SQLite for tests (no Postgres needed)
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DB_URL, echo=False)
test_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Create all tables before each test, drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """FastAPI test client with overridden DB dependency."""

    async def _override_db():
        yield db

    app.dependency_overrides[get_db] = _override_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user in the database."""
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash=hash_password("testpassword123"),
        full_name="Test User",
        company="TestCo",
        tier="free",
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user: User) -> dict[str, str]:
    """Authorization headers with a valid access token for test_user."""
    token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def test_lead(db: AsyncSession, test_user: User) -> Lead:
    """Create a test lead in the database."""
    lead = Lead(
        id=uuid.uuid4(),
        user_id=test_user.id,
        business_name="Joe's Pizza",
        google_place_id="ChIJtest123",
        address="123 Main St, New York, NY 10001",
        phone="+1-212-555-0100",
        email="joe@joespizza.com",
        website="https://joespizza.com",
        category="Restaurant",
        rating=4.5,
        review_count=120,
        latitude=40.7128,
        longitude=-74.006,
        pipeline_stage="new",
        source="google_places",
    )
    db.add(lead)
    await db.flush()
    return lead
