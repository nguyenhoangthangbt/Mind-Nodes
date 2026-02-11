# LeadLocal

**Local business lead discovery + mini CRM for agencies and freelancers.**

Search Google Places, save leads, add notes & reminders, track your sales pipeline, and analyze conversion — all in one SaaS tool.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2 |
| Frontend | Next.js 14, React 18, TailwindCSS, TanStack Query, Zustand |
| Database | PostgreSQL 16, Redis 7 |
| Background Jobs | Celery + Redis |
| Payments | Stripe (subscriptions + webhooks) |
| Email | Resend |
| Monitoring | Sentry (errors), structured logging |
| CI/CD | GitHub Actions |
| Deployment | Railway (API) + Vercel (Web) |

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose

### 1. Start Infrastructure

```bash
docker compose up -d postgres redis
```

### 2. Backend

```bash
cd api
cp .env.example .env        # Edit with your API keys
pip install -e ".[dev]"
alembic upgrade head         # Run database migrations
uvicorn leadlocal.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd web
cp .env.example .env.local   # Edit with your config
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### All-in-one (Docker)

```bash
docker compose up
```

## API Documentation

When running in development mode (`DEBUG=true`), interactive API docs are available at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Key Features

- **Search**: Find local businesses via Google Places API (+ Yelp, Foursquare)
- **Save**: One-click save search results as leads
- **Pipeline**: Track leads through stages (New → Contacted → Won)
- **Notes**: Add follow-up notes to any lead
- **Reminders**: Schedule follow-up reminders with email notifications
- **Tags**: Organize leads with color-coded tags
- **Analytics**: Pipeline funnel, source breakdown, rating distribution, conversion rate
- **Map View**: Visualize leads on Google Maps, color-coded by pipeline stage
- **Export**: Download leads as CSV for offline analysis
- **Billing**: Stripe-powered subscription tiers (Free, Starter, Pro, Agency)

## Testing

```bash
cd api
python -m pytest tests/ -v --cov=leadlocal
```

## Project Structure

```
├── api/                          # FastAPI backend
│   ├── src/leadlocal/
│   │   ├── api/                  # Route handlers
│   │   ├── core/                 # Config, DB, security, middleware
│   │   ├── integrations/         # Google Places, Yelp, Hunter.io
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic request/response models
│   │   ├── services/             # Business logic layer
│   │   ├── tasks/                # Celery background tasks
│   │   └── migrations/           # Alembic DB migrations
│   └── tests/                    # pytest test suite
├── web/                          # Next.js frontend
│   └── src/
│       ├── app/                  # App Router pages
│       ├── components/           # React components
│       ├── hooks/                # Custom React hooks
│       ├── stores/               # Zustand state management
│       ├── lib/                  # API client, utilities
│       └── types/                # TypeScript type definitions
├── docs/                         # Design & commercialization docs
├── docker-compose.yml
└── Makefile
```

## Pricing Tiers

| Plan | Price | Leads | Searches/mo |
|------|-------|-------|-------------|
| Free | $0 | 50 | 10 |
| Starter | $19/mo | 500 | 50 |
| Pro | $39/mo | 2,000 | 200 |
| Agency | $79/mo | 10,000 | Unlimited |

## License

Proprietary — All rights reserved.
