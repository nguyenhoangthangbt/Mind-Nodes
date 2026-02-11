# LeadLocal — Project Skeleton

> The complete project directory structure for both backend (Python/FastAPI) and frontend (Next.js), with every file described, dependency lists, and configuration templates.

---

## 1. Repository Structure

LeadLocal is a **monorepo** with two top-level directories: `api/` (backend) and `web/` (frontend).

```
leadlocal/
├── api/                                    # Python FastAPI backend
│   ├── src/
│   │   └── leadlocal/                      # Main Python package
│   │       ├── __init__.py                 # Package version
│   │       ├── main.py                     # FastAPI app factory, startup/shutdown
│   │       │
│   │       ├── api/                        # Route handlers (thin controllers)
│   │       │   ├── __init__.py
│   │       │   ├── router.py              # Main APIRouter aggregating all routes
│   │       │   ├── auth.py                # Signup, login, magic link, verify, refresh
│   │       │   ├── search.py              # Business search endpoint
│   │       │   ├── leads.py               # Lead CRUD + bulk actions
│   │       │   ├── notes.py               # Notes CRUD per lead
│   │       │   ├── reminders.py           # Reminders CRUD + due-today
│   │       │   ├── tags.py                # Tags CRUD + lead-tag associations
│   │       │   ├── pipeline.py            # Pipeline stats + status transitions
│   │       │   ├── analytics.py           # Funnel stats, conversion metrics
│   │       │   ├── billing.py             # Stripe checkout, portal, webhook
│   │       │   ├── users.py               # Profile update, settings
│   │       │   ├── teams.py               # Team CRUD, invite, roles
│   │       │   └── export.py              # CSV/JSON export
│   │       │
│   │       ├── services/                   # Business logic (framework-free)
│   │       │   ├── __init__.py
│   │       │   ├── auth_service.py        # User creation, verification, token logic
│   │       │   ├── search_service.py      # Multi-source search orchestration + caching
│   │       │   ├── lead_service.py        # Lead CRUD + dedup + limit enforcement
│   │       │   ├── note_service.py        # Note operations
│   │       │   ├── reminder_service.py    # Reminder scheduling + notifications
│   │       │   ├── pipeline_service.py    # Status transitions + analytics computation
│   │       │   ├── billing_service.py     # Stripe operations + tier enforcement
│   │       │   ├── export_service.py      # CSV generation
│   │       │   ├── email_service.py       # Transactional email via Resend
│   │       │   ├── team_service.py        # Team management + invitations
│   │       │   └── analytics_service.py   # Metrics aggregation
│   │       │
│   │       ├── integrations/               # External API clients
│   │       │   ├── __init__.py
│   │       │   ├── google_places.py       # Google Places API (New) client
│   │       │   ├── yelp.py                # Yelp Fusion API client
│   │       │   ├── foursquare.py          # Foursquare Places API client
│   │       │   ├── hunter.py              # Hunter.io email finder client
│   │       │   └── stripe_client.py       # Stripe SDK wrapper
│   │       │
│   │       ├── models/                     # SQLAlchemy ORM models
│   │       │   ├── __init__.py            # Re-exports all models
│   │       │   ├── base.py                # Declarative base + common mixins
│   │       │   ├── user.py                # User model
│   │       │   ├── subscription.py        # Subscription model
│   │       │   ├── lead.py                # Lead model
│   │       │   ├── note.py                # Note model
│   │       │   ├── reminder.py            # Reminder model
│   │       │   ├── tag.py                 # Tag + LeadTag models
│   │       │   ├── team.py                # Team + TeamMember models
│   │       │   └── search_log.py          # SearchLog model
│   │       │
│   │       ├── schemas/                    # Pydantic request/response schemas
│   │       │   ├── __init__.py
│   │       │   ├── auth.py                # SignupRequest, LoginRequest, TokenResponse
│   │       │   ├── search.py              # SearchRequest, LeadSearchResult
│   │       │   ├── lead.py                # LeadCreate, LeadUpdate, LeadSchema, LeadDetail
│   │       │   ├── note.py                # NoteCreate, NoteSchema
│   │       │   ├── reminder.py            # ReminderCreate, ReminderSchema
│   │       │   ├── tag.py                 # TagCreate, TagSchema
│   │       │   ├── billing.py             # CheckoutRequest, SubscriptionSchema
│   │       │   ├── analytics.py           # PipelineStats, FunnelData
│   │       │   ├── team.py                # TeamCreate, TeamInvite, TeamSchema
│   │       │   ├── user.py                # UserUpdate, UserSchema
│   │       │   └── common.py              # PaginatedResponse, ErrorResponse
│   │       │
│   │       ├── core/                       # Cross-cutting infrastructure
│   │       │   ├── __init__.py
│   │       │   ├── config.py              # Settings via pydantic-settings (.env loading)
│   │       │   ├── database.py            # Async SQLAlchemy engine + session factory
│   │       │   ├── redis.py               # Redis client singleton
│   │       │   ├── security.py            # JWT encode/decode, password hashing
│   │       │   ├── dependencies.py        # FastAPI Depends: get_db, get_current_user, check_tier
│   │       │   ├── exceptions.py          # Custom exceptions + error handlers
│   │       │   ├── rate_limit.py          # Redis-based rate limiter middleware
│   │       │   └── middleware.py          # CORS, request logging, error handling
│   │       │
│   │       ├── tasks/                      # Celery background tasks
│   │       │   ├── __init__.py            # Celery app configuration
│   │       │   ├── reminders.py           # Check due reminders → send email
│   │       │   ├── exports.py             # Generate CSV files async
│   │       │   └── cleanup.py             # Purge expired cache, old search logs
│   │       │
│   │       └── migrations/                 # Alembic migrations
│   │           ├── env.py                 # Alembic environment config
│   │           ├── script.py.mako         # Migration template
│   │           └── versions/              # Migration files (auto-generated)
│   │               └── 001_initial.py
│   │
│   ├── tests/                              # Backend test suite
│   │   ├── conftest.py                    # Test fixtures: app, db, client, auth
│   │   ├── test_api/
│   │   │   ├── test_auth.py
│   │   │   ├── test_search.py
│   │   │   ├── test_leads.py
│   │   │   ├── test_notes.py
│   │   │   ├── test_reminders.py
│   │   │   ├── test_billing.py
│   │   │   └── test_pipeline.py
│   │   ├── test_services/
│   │   │   ├── test_search_service.py
│   │   │   ├── test_lead_service.py
│   │   │   ├── test_billing_service.py
│   │   │   └── test_reminder_service.py
│   │   ├── test_integrations/
│   │   │   ├── test_google_places.py     # Mock API responses
│   │   │   └── test_stripe.py            # Mock webhook events
│   │   └── fixtures/
│   │       ├── google_places_response.json
│   │       ├── yelp_response.json
│   │       └── stripe_events.json
│   │
│   ├── pyproject.toml                      # Python project config
│   ├── alembic.ini                         # Alembic config
│   ├── Dockerfile                          # Backend container image
│   ├── docker-compose.yml                  # Local dev: API + Postgres + Redis
│   ├── .env.example                        # Environment variable template
│   └── Makefile                            # Dev commands
│
├── web/                                    # Next.js frontend
│   ├── src/
│   │   ├── app/                            # Next.js App Router
│   │   │   ├── layout.tsx                 # Root layout (fonts, providers)
│   │   │   ├── globals.css                # Tailwind base styles
│   │   │   │
│   │   │   ├── (marketing)/               # Public pages (SSR for SEO)
│   │   │   │   ├── layout.tsx             # Marketing layout (header + footer)
│   │   │   │   ├── page.tsx               # Landing page / homepage
│   │   │   │   ├── pricing/page.tsx       # Pricing comparison
│   │   │   │   └── blog/                  # SEO blog posts (MDX)
│   │   │   │       ├── page.tsx           # Blog index
│   │   │   │       └── [slug]/page.tsx    # Blog post
│   │   │   │
│   │   │   ├── (auth)/                    # Auth pages
│   │   │   │   ├── layout.tsx             # Centered card layout
│   │   │   │   ├── login/page.tsx         # Email + password / magic link
│   │   │   │   ├── signup/page.tsx        # Registration form
│   │   │   │   └── verify/page.tsx        # Email verification handler
│   │   │   │
│   │   │   └── (dashboard)/               # Protected app pages
│   │   │       ├── layout.tsx             # Dashboard layout (sidebar + topbar)
│   │   │       ├── page.tsx               # Dashboard home (stats + reminders)
│   │   │       ├── search/page.tsx        # Business search
│   │   │       ├── leads/
│   │   │       │   ├── page.tsx           # Leads list/grid
│   │   │       │   └── [id]/page.tsx      # Lead detail + notes + reminders
│   │   │       ├── pipeline/page.tsx      # Kanban board
│   │   │       ├── reminders/page.tsx     # Reminders calendar
│   │   │       ├── analytics/page.tsx     # Charts and metrics
│   │   │       ├── settings/page.tsx      # User settings
│   │   │       ├── billing/page.tsx       # Subscription management
│   │   │       └── team/page.tsx          # Team management (Pro/Agency)
│   │   │
│   │   ├── components/
│   │   │   ├── ui/                        # shadcn/ui primitives
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── badge.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   ├── toast.tsx
│   │   │   │   ├── skeleton.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   ├── tabs.tsx
│   │   │   │   └── ... (other shadcn components)
│   │   │   │
│   │   │   ├── layout/
│   │   │   │   ├── sidebar.tsx            # Dashboard sidebar navigation
│   │   │   │   ├── topbar.tsx             # Top bar with user menu
│   │   │   │   ├── mobile-nav.tsx         # Mobile hamburger menu
│   │   │   │   ├── marketing-header.tsx   # Public page header
│   │   │   │   └── marketing-footer.tsx   # Public page footer
│   │   │   │
│   │   │   ├── search/
│   │   │   │   ├── search-form.tsx        # Category + location + radius inputs
│   │   │   │   ├── search-results.tsx     # Results grid
│   │   │   │   ├── business-card.tsx      # Single result card with [Save] button
│   │   │   │   └── search-map.tsx         # Map view of results (Phase 8)
│   │   │   │
│   │   │   ├── leads/
│   │   │   │   ├── leads-table.tsx        # Leads list/table component
│   │   │   │   ├── lead-card.tsx          # Lead summary card
│   │   │   │   ├── lead-detail.tsx        # Full lead detail panel
│   │   │   │   ├── note-list.tsx          # Notes timeline
│   │   │   │   ├── note-form.tsx          # Add/edit note form
│   │   │   │   ├── reminder-list.tsx      # Reminders for a lead
│   │   │   │   ├── reminder-form.tsx      # Add/edit reminder form
│   │   │   │   ├── status-badge.tsx       # Color-coded status indicator
│   │   │   │   ├── tag-selector.tsx       # Tag picker with create
│   │   │   │   └── bulk-actions.tsx       # Bulk action toolbar
│   │   │   │
│   │   │   ├── pipeline/
│   │   │   │   ├── kanban-board.tsx       # Drag-and-drop pipeline board
│   │   │   │   ├── kanban-column.tsx      # Single status column
│   │   │   │   └── kanban-card.tsx        # Lead card in kanban
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── stat-cards.tsx         # KPI summary cards
│   │   │   │   ├── reminders-today.tsx    # Due-today reminder list
│   │   │   │   └── recent-activity.tsx    # Activity feed
│   │   │   │
│   │   │   ├── billing/
│   │   │   │   ├── pricing-table.tsx      # Tier comparison table
│   │   │   │   ├── usage-meter.tsx        # Usage progress bar
│   │   │   │   └── upgrade-modal.tsx      # Upgrade prompt modal
│   │   │   │
│   │   │   └── analytics/
│   │   │       ├── funnel-chart.tsx       # Conversion funnel visualization
│   │   │       ├── leads-by-status.tsx    # Pie/bar chart by status
│   │   │       └── leads-over-time.tsx    # Line chart over time
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts                     # Fetch wrapper with auth headers
│   │   │   ├── auth.ts                    # Token storage, refresh, redirect
│   │   │   ├── utils.ts                   # Shared utilities (formatDate, etc.)
│   │   │   └── constants.ts               # Status colors, tier names, etc.
│   │   │
│   │   ├── hooks/
│   │   │   ├── use-leads.ts               # TanStack Query hooks for leads
│   │   │   ├── use-search.ts              # Search mutation hook
│   │   │   ├── use-reminders.ts           # Reminders query hooks
│   │   │   ├── use-auth.ts                # Auth state hook
│   │   │   └── use-billing.ts             # Subscription info hook
│   │   │
│   │   ├── stores/
│   │   │   └── app-store.ts               # Zustand: UI state, sidebar, modals
│   │   │
│   │   └── types/
│   │       └── index.ts                   # Shared TypeScript types
│   │
│   ├── public/
│   │   ├── og-image.png                   # Open Graph social sharing image
│   │   ├── favicon.ico
│   │   └── screenshots/                   # Product screenshots for landing page
│   │
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── components.json                    # shadcn/ui config
│   └── .env.local.example
│
├── .github/
│   ├── workflows/
│   │   ├── api-ci.yml                     # Backend: lint, type-check, test
│   │   ├── web-ci.yml                     # Frontend: lint, type-check, build
│   │   └── deploy.yml                     # Deploy on push to main
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
│
├── README.md
├── CHANGELOG.md
├── LICENSE                                # Proprietary (or choose license)
└── .gitignore
```

---

## 2. Backend Dependencies

### 2.1 pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "leadlocal"
version = "0.1.0"
description = "Local business lead discovery + mini CRM"
requires-python = ">=3.12"
dependencies = [
    # Web framework
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    # Database
    "sqlalchemy[asyncio]>=2.0.25",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    # Validation
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    # HTTP client (for external APIs)
    "httpx>=0.27.0",
    # Auth
    "PyJWT>=2.8.0",
    "passlib[bcrypt]>=1.7.4",
    # Cache + Queue
    "redis>=5.0.0",
    "celery[redis]>=5.3.0",
    # Payments
    "stripe>=7.0.0",
    # Email
    "resend>=0.7.0",
    # Utilities
    "python-multipart>=0.0.6",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",       # For TestClient
    "pytest-cov>=4.1.0",
    "mypy>=1.8.0",
    "ruff>=0.2.0",
    "pre-commit>=3.6.0",
]

[tool.ruff]
target-version = "py312"
line-length = 100
src = ["src"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "SIM", "RUF"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = ["celery.*", "resend.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

### 2.2 docker-compose.yml (Local Development)

```yaml
version: "3.9"
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db, redis]
    volumes: ["./src:/app/src"]
    command: uvicorn leadlocal.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: leadlocal
      POSTGRES_USER: leadlocal
      POSTGRES_PASSWORD: localdev
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  celery:
    build: .
    env_file: .env
    depends_on: [db, redis]
    command: celery -A leadlocal.tasks worker --loglevel=info

  celery-beat:
    build: .
    env_file: .env
    depends_on: [redis]
    command: celery -A leadlocal.tasks beat --loglevel=info

volumes:
  pgdata:
```

### 2.3 Makefile

```makefile
.PHONY: dev test lint typecheck migrate

dev:
	docker compose up -d db redis
	uvicorn leadlocal.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ --cov=leadlocal --cov-report=html

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

typecheck:
	mypy src/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

migrate:
	alembic upgrade head

migrate-new:
	alembic revision --autogenerate -m "$(msg)"

celery:
	celery -A leadlocal.tasks worker --loglevel=info

celery-beat:
	celery -A leadlocal.tasks beat --loglevel=info
```

---

## 3. Frontend Dependencies

### 3.1 package.json (key dependencies)

```json
{
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.5.0",
    "react-hook-form": "^7.49.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    "recharts": "^2.10.0",
    "@dnd-kit/core": "^6.1.0",
    "@dnd-kit/sortable": "^8.0.0",
    "sonner": "^1.3.0",
    "date-fns": "^3.3.0",
    "lucide-react": "^0.312.0",
    "tailwindcss": "^3.4.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0",
    "prettier": "^3.2.0",
    "prettier-plugin-tailwindcss": "^0.5.0"
  }
}
```

---

## 4. CI/CD Configurations

### 4.1 Backend CI (.github/workflows/api-ci.yml)

```yaml
name: API CI
on:
  push:
    paths: ["api/**"]
  pull_request:
    paths: ["api/**"]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env: { POSTGRES_DB: test, POSTGRES_USER: test, POSTGRES_PASSWORD: test }
        ports: ["5432:5432"]
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -e ".[dev]"
        working-directory: api
      - run: ruff check src/ tests/
        working-directory: api
      - run: mypy src/
        working-directory: api
      - run: pytest tests/ --cov=leadlocal -v
        working-directory: api
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379/0
          JWT_SECRET_KEY: test-secret-key
          GOOGLE_PLACES_API_KEY: test-key
          STRIPE_SECRET_KEY: sk_test_xxx
          STRIPE_WEBHOOK_SECRET: whsec_test
```

### 4.2 Frontend CI (.github/workflows/web-ci.yml)

```yaml
name: Web CI
on:
  push:
    paths: ["web/**"]
  pull_request:
    paths: ["web/**"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: npm ci
        working-directory: web
      - run: npm run lint
        working-directory: web
      - run: npm run build
        working-directory: web
```

---

## 5. Environment Files

### 5.1 api/.env.example

```bash
# Database
DATABASE_URL=postgresql+asyncpg://leadlocal:localdev@localhost:5432/leadlocal

# Redis
REDIS_URL=redis://localhost:6379/0

# Auth
JWT_SECRET_KEY=change-me-to-random-64-char-string
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Google Places
GOOGLE_PLACES_API_KEY=your-api-key

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
RESEND_API_KEY=re_test_...
FROM_EMAIL=hello@leadlocal.io

# App
APP_URL=http://localhost:3000
API_URL=http://localhost:8000
ENVIRONMENT=development
```

### 5.2 web/.env.local.example

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_POSTHOG_KEY=phc_...
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 6. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
.venv/
.mypy_cache/
.pytest_cache/
.coverage
htmlcov/

# Node
node_modules/
.next/
out/

# Environment
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Build
*.log
```

---

## 7. Document Cross-References

| Topic | Document |
|-------|----------|
| Business model and pricing | [constitution.md](constitution.md) |
| Architecture decisions | [blueprint.md](blueprint.md) |
| Database schemas and API specs | [artifacts.md](artifacts.md) |
| Build phases | [implementation-guide.md](implementation-guide.md) |
| Launch and marketing strategy | [go-to-market.md](go-to-market.md) |
