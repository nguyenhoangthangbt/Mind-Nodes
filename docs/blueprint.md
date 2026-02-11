# LeadLocal — System Architecture Blueprint

> The technical architecture document defining how LeadLocal is built, what services it integrates, and how all components interact.

---

## 1. Architectural Overview

### 1.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                   │
│  Browser (React/Next.js)  │  Mobile Browser  │  Chrome Extension  │
└──────────────┬───────────────────────────────────┬───────────────┘
               │            HTTPS                   │
┌──────────────▼───────────────────────────────────▼───────────────┐
│                     REVERSE PROXY (Nginx/Caddy)                   │
│                     SSL Termination + Rate Limiting                │
└──────────────┬───────────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                          │
│  Auth Middleware │ Rate Limiter │ Request Validation │ CORS        │
├──────────────────────────────────────────────────────────────────┤
│                     APPLICATION SERVICES                          │
│  SearchService │ LeadService │ PipelineService │ UserService      │
│  ReminderService │ ExportService │ AnalyticsService               │
│  BillingService │ TeamService │ IntegrationService                │
├──────────────────────────────────────────────────────────────────┤
│                     DATA ACCESS LAYER                             │
│  SQLAlchemy ORM │ Repository Pattern │ Migration (Alembic)        │
└───────┬────────────────────┬─────────────────────┬───────────────┘
        │                    │                     │
┌───────▼───────┐  ┌────────▼────────┐  ┌────────▼────────┐
│  PostgreSQL   │  │     Redis       │  │   Object Store  │
│  (Primary DB) │  │  (Cache + Queue)│  │  (S3/Cloudflare)│
└───────────────┘  └─────────────────┘  └─────────────────┘

External API Integrations:
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Google Places│  Yelp Fusion │  Foursquare  │  Hunter.io   │
│     API      │     API      │  Places API  │  (Email)     │
└──────────────┴──────────────┴──────────────┴──────────────┘
                                                     │
Payment + Auth:                                      │
┌──────────────┬──────────────┐                      │
│   Stripe     │  SendGrid /  │                      │
│  (Billing)   │  Resend.com  │                      │
│              │  (Email)     │                      │
└──────────────┴──────────────┘
```

### 1.2 Key Architecture Decisions

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | **Python + FastAPI** backend | Fast development, async support, excellent for API integrations, your existing Python expertise |
| ADR-002 | **Next.js 14** frontend | SSR for SEO (landing page), React ecosystem, Vercel deployment, App Router for modern patterns |
| ADR-003 | **PostgreSQL** primary database | Reliable, great JSON support (for caching API responses), full-text search, free on Supabase/Neon |
| ADR-004 | **Redis** for caching + task queue | Cache Google Places results (reduce API costs), background job queue for reminders |
| ADR-005 | **Stripe** for billing | Industry standard, excellent Python SDK, handles subscriptions/trials/invoices/webhooks |
| ADR-006 | **JWT + Magic Links** for auth | Passwordless option reduces friction; JWT for stateless API auth |
| ADR-007 | **Google Places API (official)** not scraping | Legal compliance, reliable data, no cease-and-desist risk. Key selling point |
| ADR-008 | **Monolith-first** architecture | Single FastAPI app, not microservices. Faster to build, deploy, debug. Split later if needed |
| ADR-009 | **Railway/Render** for backend hosting | Simple deployment, managed PostgreSQL, affordable at early scale. Migrate to AWS/GCP later |
| ADR-010 | **Vercel** for frontend hosting | Free tier, automatic deployments, edge CDN, perfect for Next.js |

---

## 2. Technology Stack

### 2.1 Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Runtime | Python | 3.12+ | API server |
| Framework | FastAPI | 0.110+ | REST API with automatic OpenAPI docs |
| ORM | SQLAlchemy | 2.0+ | Database access with async support |
| Migrations | Alembic | 1.13+ | Schema migration management |
| Validation | Pydantic | 2.5+ | Request/response validation |
| Task Queue | Celery + Redis | 5.3+ | Background jobs (reminders, exports) |
| Caching | Redis | 7+ | API response cache, rate limiting, sessions |
| HTTP Client | httpx | 0.27+ | Async calls to external APIs |
| Auth | PyJWT + passlib | - | JWT tokens, password hashing |
| Email | resend (SDK) | - | Transactional emails (magic links, reminders) |
| Payments | stripe (SDK) | - | Subscription management |

### 2.2 Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Next.js | 14+ | React SSR/SSG + App Router |
| UI Library | shadcn/ui + Tailwind CSS | - | Pre-built components + utility CSS |
| State | Zustand | 4+ | Lightweight client state management |
| Data Fetching | TanStack Query | 5+ | API data fetching with cache/retry |
| Forms | React Hook Form + Zod | - | Form handling with validation |
| Maps | react-leaflet or @vis.gl/react-google-maps | - | Map view of leads |
| Charts | Recharts | 2+ | Analytics dashboard charts |
| Auth UI | Custom (magic link + password) | - | Login/signup pages |
| Toast/Notifications | sonner | - | User notifications |

### 2.3 Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend hosting | Railway or Render | FastAPI + PostgreSQL + Redis |
| Frontend hosting | Vercel | Next.js deployment |
| Object storage | Cloudflare R2 or AWS S3 | User uploads (future), export files |
| DNS + CDN | Cloudflare | DNS, SSL, edge caching, DDoS protection |
| Monitoring | Sentry | Error tracking (free tier) |
| Analytics | PostHog | Product analytics, funnels, retention (free tier) |
| Uptime | BetterUptime | Uptime monitoring + status page (free tier) |
| Email delivery | Resend.com | Transactional email (3K/mo free) |

### 2.4 External APIs (Data Sources)

| API | Free Tier | Data Provided | Priority |
|-----|-----------|--------------|----------|
| **Google Places API (New)** | $200/mo credit (~10K searches) | Name, address, phone, website, rating, reviews, hours, photos, categories | **MVP — Primary** |
| **Yelp Fusion API** | 5,000 calls/day free | Name, address, phone, rating, reviews, categories, photos | **Post-MVP** |
| **Foursquare Places API** | 200K calls/mo free | Name, address, categories, hours, popularity, tips | **Post-MVP** |
| **Hunter.io** | 25 searches/mo free | Business email addresses | **Post-MVP** |

### 2.5 Cost Structure (Monthly at Launch)

| Service | Free Tier | At 100 Users | At 1000 Users |
|---------|-----------|-------------|--------------|
| Google Places API | $200 credit | ~$50 | ~$400 |
| Railway (backend) | $5/mo | $15 | $50 |
| Vercel (frontend) | Free | Free | $20 |
| Redis (Upstash) | Free | Free | $10 |
| PostgreSQL (Neon/Supabase) | Free | Free | $25 |
| Resend (email) | Free (3K/mo) | Free | $20 |
| Sentry | Free | Free | Free |
| PostHog | Free (1M events) | Free | Free |
| Cloudflare | Free | Free | Free |
| Stripe fees | 2.9% + $0.30/tx | ~$50 | ~$400 |
| **Total** | **~$5/mo** | **~$115/mo** | **~$925/mo** |

At 1000 users paying $30 avg = $30,000 MRR → $925 costs = **97% gross margin**.

---

## 3. Component Architecture

### 3.1 Backend Services

```
src/leadlocal/
├── api/              ← FastAPI route handlers
│   ├── auth.py       ← Login, signup, magic link, token refresh
│   ├── search.py     ← Business search (Google Places + cache)
│   ├── leads.py      ← CRUD for saved leads
│   ├── notes.py      ← CRUD for lead notes
│   ├── reminders.py  ← CRUD for follow-up reminders
│   ├── pipeline.py   ← Pipeline status management
│   ├── tags.py       ← Lead tagging
│   ├── export.py     ← CSV/JSON export
│   ├── billing.py    ← Stripe webhook handler, subscription management
│   ├── users.py      ← Profile, settings, team management
│   └── analytics.py  ← Dashboard stats
│
├── services/         ← Business logic (testable without HTTP)
│   ├── search_service.py     ← Orchestrates multi-source search
│   ├── lead_service.py       ← Lead CRUD + validation
│   ├── pipeline_service.py   ← Status transitions + analytics
│   ├── reminder_service.py   ← Reminder scheduling + notifications
│   ├── billing_service.py    ← Subscription enforcement + usage tracking
│   ├── export_service.py     ← CSV/JSON generation
│   ├── email_service.py      ← Transactional email sending
│   ├── team_service.py       ← Team invites, permissions
│   └── analytics_service.py  ← Metrics computation
│
├── integrations/     ← External API clients
│   ├── google_places.py   ← Google Places API client
│   ├── yelp.py            ← Yelp Fusion API client
│   ├── foursquare.py      ← Foursquare Places client
│   ├── hunter.py          ← Hunter.io email finder client
│   └── stripe_client.py   ← Stripe subscription management
│
├── models/           ← SQLAlchemy ORM models
│   ├── user.py
│   ├── lead.py
│   ├── note.py
│   ├── reminder.py
│   ├── tag.py
│   ├── subscription.py
│   ├── search_cache.py
│   └── team.py
│
├── schemas/          ← Pydantic request/response schemas
│   ├── auth.py
│   ├── search.py
│   ├── lead.py
│   ├── note.py
│   ├── reminder.py
│   ├── billing.py
│   └── analytics.py
│
├── core/             ← Cross-cutting concerns
│   ├── config.py     ← Environment config (pydantic-settings)
│   ├── database.py   ← SQLAlchemy engine + session
│   ├── security.py   ← JWT encoding/decoding, password hashing
│   ├── cache.py      ← Redis client wrapper
│   ├── dependencies.py ← FastAPI dependency injection
│   ├── exceptions.py ← Custom exception classes
│   ├── rate_limit.py ← Rate limiting middleware
│   └── middleware.py  ← CORS, logging, error handling
│
├── tasks/            ← Celery background tasks
│   ├── reminders.py  ← Check & send reminder notifications
│   ├── export.py     ← Generate CSV exports
│   └── cleanup.py    ← Cache cleanup, stale data removal
│
└── migrations/       ← Alembic migration files
    └── versions/
```

### 3.2 Frontend Structure

```
src/
├── app/                    ← Next.js App Router pages
│   ├── (marketing)/        ← Public pages (SSR for SEO)
│   │   ├── page.tsx        ← Landing page
│   │   ├── pricing/page.tsx
│   │   └── blog/           ← SEO content pages
│   ├── (auth)/             ← Auth pages
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   └── verify/page.tsx ← Magic link verification
│   ├── (dashboard)/        ← Protected app pages
│   │   ├── layout.tsx      ← Dashboard layout with sidebar
│   │   ├── page.tsx        ← Dashboard home (stats + due reminders)
│   │   ├── search/page.tsx ← Business search interface
│   │   ├── leads/page.tsx  ← Saved leads list/grid
│   │   ├── leads/[id]/page.tsx ← Single lead detail + notes
│   │   ├── pipeline/page.tsx   ← Kanban pipeline board
│   │   ├── reminders/page.tsx  ← Upcoming reminders
│   │   ├── analytics/page.tsx  ← Charts and conversion stats
│   │   ├── settings/page.tsx   ← User profile + preferences
│   │   ├── billing/page.tsx    ← Subscription management
│   │   └── team/page.tsx       ← Team members (Pro/Agency)
│   ├── api/                ← Next.js API routes (minimal, proxy)
│   └── layout.tsx          ← Root layout
│
├── components/
│   ├── ui/                 ← shadcn/ui components
│   ├── search/             ← Search form, result cards, map view
│   ├── leads/              ← Lead cards, lead detail, notes list
│   ├── pipeline/           ← Kanban board, status badges
│   ├── dashboard/          ← Stat cards, reminder list
│   ├── billing/            ← Pricing table, upgrade modal
│   └── layout/             ← Sidebar, topbar, mobile nav
│
├── lib/
│   ├── api.ts              ← API client (fetch wrapper)
│   ├── auth.ts             ← Auth helpers (token management)
│   └── utils.ts            ← Shared utilities
│
├── stores/
│   └── app-store.ts        ← Zustand global state
│
└── types/
    └── index.ts            ← TypeScript type definitions
```

### 3.3 Search Service Architecture

The search service is the core differentiator. It orchestrates multiple data sources and caching.

```
User searches "Restaurants in Austin, TX"
  │
  ▼
SearchService.search(query="restaurant", location="Austin, TX", radius=5km)
  │
  ├── Check Redis cache (key = hash(query + location + radius))
  │   ├── Cache HIT → return cached results (TTL: 24 hours)
  │   └── Cache MISS → continue to API calls
  │
  ├── GooglePlacesClient.nearby_search(
  │       query="restaurant",
  │       location=geocode("Austin, TX"),  ← Google Geocoding
  │       radius=5000,
  │       type="restaurant"
  │   )
  │   └── Returns: up to 60 results (3 pages × 20)
  │       Each: place_id, name, address, location, rating,
  │              user_ratings_total, types, business_status,
  │              opening_hours, price_level, photos
  │
  ├── For each result, fetch details (batched):
  │   GooglePlacesClient.place_details(place_id)
  │   └── Returns: phone, website, formatted_address,
  │                reviews (text + rating), full hours
  │
  ├── [Post-MVP] Merge with Yelp / Foursquare data:
  │   YelpClient.business_search(term, location)
  │   FoursquareClient.place_search(query, ll)
  │   └── Match by name + address similarity → merge ratings, photos
  │
  ├── Normalize all results to unified LeadSearchResult schema
  │
  ├── Cache results in Redis (TTL: 24 hours)
  │
  ├── Track usage: increment user's monthly search count
  │   └── If over limit → return 402 (upgrade required)
  │
  └── Return list[LeadSearchResult] to frontend
```

### 3.4 Billing & Usage Enforcement

```
Every API request:
  │
  ▼
BillingMiddleware
  ├── Lookup user's subscription tier (cached in Redis)
  ├── Check feature access:
  │   ├── Free:    max 50 saved leads, 10 searches/mo, 1 user
  │   ├── Starter: max 500 saved leads, 50 searches/mo, 1 user
  │   ├── Pro:     max 2000 saved leads, 200 searches/mo, 3 users
  │   └── Agency:  max 10000 saved leads, unlimited, 10 users
  │
  ├── If within limits → allow request
  └── If over limit → return 402 with upgrade prompt
      {
        "error": "limit_exceeded",
        "message": "You've used 50 of 50 saved leads",
        "upgrade_url": "/billing?plan=starter",
        "current_plan": "free",
        "suggested_plan": "starter"
      }
```

---

## 4. Data Flow Diagrams

### 4.1 User Signup Flow

```
User visits leadlocal.io
  │
  ▼
Landing page (Next.js SSR — SEO optimized)
  │  User clicks "Start Free"
  ▼
Signup form → POST /api/auth/signup { email, password }
  │
  ▼
Backend:
  ├── Create User record (status: pending_verification)
  ├── Hash password with bcrypt
  ├── Create free-tier Subscription record
  ├── Send verification email via Resend
  └── Return { user_id, message: "Check email" }
        │
        ▼
User clicks email link → GET /api/auth/verify?token=...
  │
  ▼
Backend:
  ├── Validate token (JWT with 24h expiry)
  ├── Set user.status = active
  ├── Generate access_token + refresh_token
  └── Redirect to /dashboard
        │
        ▼
Dashboard loads → GET /api/leads/stats
  └── Returns: { saved: 0, limit: 50, searches_used: 0, reminders_due: 0 }
      │
      ▼
  Prompt: "Search for your first leads!" → /search
```

### 4.2 Search → Save → Follow-up Flow

```
User on /search page:
  Types "Dentists" + "Miami, FL" + 10km radius
  │
  ▼
Frontend: POST /api/search { query, location, radius }
  │
  ▼
Backend SearchService:
  ├── Check usage: user has 3 of 10 free searches used → OK
  ├── Check Redis cache → MISS
  ├── Call Google Places API (Nearby Search)
  │   → 20 results (page 1)
  ├── Call Place Details for each (batched via async)
  ├── Cache in Redis (TTL: 24h)
  ├── Increment search count: 3 → 4
  └── Return 20 LeadSearchResult objects
        │
        ▼
Frontend renders search results as cards:
  ┌─────────────────────────────────────────┐
  │ ★ 4.6  Coral Gables Dental      [Save] │
  │        123 Miracle Mile, Miami          │
  │        📞 (305) 555-0123  🌐 Website   │
  │        Open now · 287 reviews           │
  └─────────────────────────────────────────┘
        │  User clicks [Save]
        ▼
Frontend: POST /api/leads { google_place_id, source_data }
  │
  ▼
Backend LeadService:
  ├── Check limit: user has 12 of 50 free leads → OK
  ├── Check duplicate: not already saved → OK
  ├── Create Lead record (status: "new")
  ├── Store source data snapshot (name, address, phone, etc.)
  └── Return Lead object with id
        │
        ▼
User clicks on saved lead → /leads/{id}
  │  Adds a note: "Called, spoke with Dr. Garcia, interested in SEO"
  │  Sets follow-up: next Tuesday
  │  Changes status: New → Contacted
  ▼
Frontend:
  POST /api/leads/{id}/notes { content: "Called, spoke with..." }
  POST /api/leads/{id}/reminders { due_date: "2026-02-17", note: "Follow up call" }
  PATCH /api/leads/{id} { status: "contacted" }
```

### 4.3 Stripe Billing Flow

```
User hits lead limit (50/50 on free tier):
  │
  ▼
Frontend shows upgrade modal:
  "You've saved 50 of 50 leads. Upgrade to Starter ($19/mo) for 500 leads."
  [Upgrade Now]
  │
  ▼
Frontend: POST /api/billing/create-checkout-session { plan: "starter" }
  │
  ▼
Backend BillingService:
  ├── Create Stripe Checkout Session
  │   stripe.checkout.Session.create(
  │     customer=user.stripe_customer_id,
  │     price=STARTER_PRICE_ID,
  │     mode="subscription",
  │     success_url="/billing?success=true",
  │     cancel_url="/billing?canceled=true",
  │   )
  └── Return { checkout_url }
        │
        ▼
Frontend redirects to Stripe Checkout page
  User enters payment → Stripe processes
  │
  ▼
Stripe sends webhook → POST /api/billing/webhook
  │
  ▼
Backend handles event:
  ├── checkout.session.completed → Create/update Subscription record
  ├── invoice.payment_succeeded → Extend subscription, update tier
  ├── invoice.payment_failed → Send warning email, grace period
  └── customer.subscription.deleted → Downgrade to free tier
        │
        ▼
User's tier updated in DB + Redis cache
  └── Next API request: limits are now 500 leads, 50 searches/mo
```

---

## 5. Caching Strategy

### 5.1 Cache Layers

| Data | Cache Location | TTL | Purpose |
|------|---------------|-----|---------|
| Google Places search results | Redis | 24 hours | Reduce API costs (same search = no API call) |
| Place details | Redis | 7 days | Details change rarely; reduce detail API calls |
| User subscription tier | Redis | 1 hour | Avoid DB query on every request |
| User session/JWT | Redis | 15 min (access) / 7 days (refresh) | Fast auth validation |
| Dashboard stats | Redis | 5 minutes | Avoid expensive aggregate queries |
| Rate limit counters | Redis | 1 minute window | Request rate limiting |

### 5.2 Cache Key Schema

```
search:{hash(query+location+radius)}     → search results JSON
place:{google_place_id}                   → place details JSON
user:tier:{user_id}                       → subscription tier string
user:usage:{user_id}:{year}:{month}       → { searches: N, leads: N }
stats:{user_id}                           → dashboard stats JSON
ratelimit:{user_id}:{endpoint}:{window}   → request count
```

### 5.3 API Cost Optimization

```
Without cache:
  1000 users × 5 searches/day × 30 days = 150,000 API calls/month
  Cost: ~$4,800/month (Google Places)

With 24h cache (80% cache hit rate):
  150,000 × 0.20 = 30,000 API calls/month
  Cost: ~$960/month

Savings: $3,840/month (80% reduction)
```

---

## 6. Security Architecture

### 6.1 Authentication

```
Two auth methods:

1. Email + Password:
   - Password hashed with bcrypt (12 rounds)
   - Email verification required before first login
   - Access token: JWT, 15-minute expiry
   - Refresh token: JWT, 7-day expiry, stored in httpOnly cookie

2. Magic Link (passwordless):
   - User enters email → backend sends login link
   - Link contains signed JWT with 15-minute expiry
   - One-time use (invalidated after click)
   - Ideal for reducing signup friction
```

### 6.2 API Security

| Measure | Implementation |
|---------|---------------|
| Authentication | JWT Bearer token on all /api/* routes (except /auth/*) |
| Rate limiting | 100 req/min per user (Redis sliding window) |
| Input validation | Pydantic schemas validate all request bodies |
| SQL injection | SQLAlchemy ORM (parameterized queries only) |
| XSS | React auto-escapes; CSP headers on responses |
| CORS | Whitelist frontend domain only |
| CSRF | SameSite=Strict cookies + Origin header check |
| Data access | Row-level security: users can only access own leads/notes |
| Stripe webhooks | Signature verification on all webhook endpoints |
| Secrets | Environment variables via pydantic-settings; never in code |

### 6.3 Data Privacy

| Data Type | Privacy Rule |
|-----------|-------------|
| Business data (from Google/Yelp) | Public data, displayed as-is |
| User notes | Private to user (or team). Never shared, never used for analytics |
| User email/password | Encrypted at rest, password bcrypt-hashed |
| Pipeline status | Private to user/team |
| Usage analytics | Anonymized for internal metrics only |
| Stripe payment data | Handled entirely by Stripe; we never store card numbers |

---

## 7. Scalability Considerations

### 7.1 MVP Scale (0–1,000 users)

- Single FastAPI process on Railway ($5-20/mo)
- Single PostgreSQL instance (Neon free tier → $25/mo)
- Single Redis instance (Upstash free tier)
- Vercel free tier for frontend
- **Total cost: $5-50/mo**

### 7.2 Growth Scale (1,000–10,000 users)

- FastAPI with 2-4 Gunicorn workers
- PostgreSQL with read replicas
- Redis cluster for caching
- Celery workers for background jobs (2-4 workers)
- CDN for static assets
- **Total cost: $200-500/mo**

### 7.3 Scale-Up Triggers

| Trigger | Action |
|---------|--------|
| API response time > 500ms (p95) | Add FastAPI workers or upgrade instance |
| Database CPU > 70% | Add read replica for search queries |
| Redis memory > 80% | Upgrade Redis instance or reduce TTLs |
| Celery queue > 1000 pending | Add Celery workers |
| Google API costs > $1000/mo | Increase cache TTLs, add Yelp/Foursquare as alternates |

---

## 8. Monitoring and Observability

| Layer | Tool | What It Tracks |
|-------|------|---------------|
| Error tracking | Sentry | Unhandled exceptions, API errors, stack traces |
| Product analytics | PostHog | User actions, funnels, retention, feature usage |
| Uptime monitoring | BetterUptime | API availability, response times, status page |
| Application logs | stdout → Railway logs | Request logs, business logic events |
| Database | PostgreSQL pg_stat | Query performance, connection pool |
| API costs | Google Cloud Console | Places API usage and billing |
| Business metrics | Internal dashboard | MRR, signups, conversions, churn |

---

## 9. Document Cross-References

| Topic | Document |
|-------|----------|
| Business model and pricing tiers | [constitution.md](constitution.md) Section 4 |
| Database schemas and API contracts | [artifacts.md](artifacts.md) |
| Build phases and deployment steps | [implementation-guide.md](implementation-guide.md) |
| File/directory structure | [skeleton.md](skeleton.md) |
| Marketing and growth strategy | [go-to-market.md](go-to-market.md) |
