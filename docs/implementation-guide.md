# LeadLocal — Implementation Guide

> The phased development plan with both technical and commercial milestones. Each phase produces a deployable increment and moves toward the first paying customer.

---

## 1. Development Principles

### 1.1 Speed to Revenue

The #1 priority is getting to a paying customer as fast as possible. Every feature decision asks: "Does this help us get paid sooner?"

### 1.2 Phase Dependencies

```
Phase 0 (Bootstrap)                 ← Week 1
    │
Phase 1 (Backend Core)             ← Weeks 1-2
    │
Phase 2 (Frontend Core)            ← Weeks 2-3
    │
Phase 3 (CRM Features)             ← Weeks 3-4
    │
Phase 4 (Billing + Limits)         ← Week 4
    │
Phase 5 (Launch Prep)              ← Week 5
    │
█████ MVP LAUNCH █████             ← Week 5-6
    │
Phase 6 (Post-Launch Iteration)    ← Weeks 6-8
    │
Phase 7 (Growth Features)          ← Weeks 8-12
    │
Phase 8 (Scale + Optimize)         ← Months 3-6
```

### 1.3 Testing Strategy

| Type | Tool | When | Coverage Target |
|------|------|------|----------------|
| Unit tests | pytest | Every phase | 80% on services, integrations |
| Integration tests | pytest + httpx | Phases 1-4 | All API endpoints |
| E2E tests | Playwright | Phase 5+ | Critical user flows (signup, search, save, pay) |
| Load tests | Locust | Phase 5 | Ensure 100 concurrent users |
| Manual QA | Checklist | Every phase | All user-facing features |

---

## 2. Phase 0 — Project Bootstrap (Week 1, Days 1-2)

**Goal:** Set up both backend and frontend projects with tooling, CI, and deployment pipelines.

### 2.1 Backend Tasks

1. Initialize Python project:
   ```
   mkdir leadlocal-api && cd leadlocal-api
   python -m venv .venv
   ```
2. Create `pyproject.toml` with dependencies (FastAPI, SQLAlchemy, Alembic, Pydantic, httpx, etc.)
3. Create `src/leadlocal/` package structure (see [skeleton.md](skeleton.md))
4. Set up FastAPI app with health check endpoint: `GET /health → { status: "ok" }`
5. Set up SQLAlchemy + Alembic for database migrations
6. Set up Redis connection
7. Create `.env.example` with all required environment variables
8. Set up `ruff` + `mypy` + `pytest` configuration
9. Create `Dockerfile` for deployment
10. Set up GitHub Actions CI: lint → type-check → test on push

### 2.2 Frontend Tasks

1. Initialize Next.js 14 project with App Router:
   ```
   npx create-next-app@latest leadlocal-web --typescript --tailwind --app
   ```
2. Install shadcn/ui components + Zustand + TanStack Query
3. Create layout structure: `(marketing)`, `(auth)`, `(dashboard)` route groups
4. Create landing page placeholder at `/`
5. Set up ESLint + Prettier
6. Deploy to Vercel (auto-deploy on push)

### 2.3 Infrastructure Tasks

1. Create Railway project → deploy FastAPI + PostgreSQL + Redis
2. Set up Cloudflare DNS for `leadlocal.io`
3. Connect Vercel frontend to custom domain
4. Set up Sentry for error tracking (both frontend and backend)

### 2.4 Verification

```bash
# Backend
curl https://api.leadlocal.io/health  → { "status": "ok" }
pytest tests/ → all green
ruff check src/ && mypy src/ → clean

# Frontend
https://leadlocal.io → landing page placeholder loads
```

### 2.5 Commercial Milestone

Domain registered. Basic landing page live. Can start collecting email signups.

---

## 3. Phase 1 — Backend Core (Week 1-2)

**Goal:** Implement user auth, Google Places search, and lead CRUD API.

### 3.1 Tasks

1. **Database models** — Create all SQLAlchemy models from [artifacts.md](artifacts.md) Section 1:
   - `User`, `Subscription`, `Lead`, `Note`, `Reminder`, `Tag`, `LeadTag`, `Team`, `TeamMember`, `SearchLog`
   - Run `alembic revision --autogenerate` → initial migration

2. **Auth system** (`api/auth.py`, `core/security.py`):
   - `POST /api/auth/signup` — create user + free subscription + send verification email
   - `POST /api/auth/login` — validate credentials, return JWT tokens
   - `POST /api/auth/magic-link` — send passwordless login link
   - `GET /api/auth/verify` — verify email or magic link token
   - `POST /api/auth/refresh` — refresh access token
   - JWT middleware that extracts and validates tokens on protected routes

3. **Google Places integration** (`integrations/google_places.py`):
   - `GooglePlacesClient` class with async httpx
   - `nearby_search(query, lat, lng, radius)` → list of places
   - `place_details(place_id)` → full business details
   - `text_search(text_query)` → list of places
   - Response parsing and normalization to `UnifiedLead` schema
   - Error handling: quota exceeded, invalid API key, network errors

4. **Search service** (`services/search_service.py`):
   - Orchestrates Google Places calls
   - Redis caching (24h TTL for search results, 7d for place details)
   - Usage tracking (increment searches_used per user per month)
   - Limit enforcement (return 402 if over tier limit)

5. **Search API** (`api/search.py`):
   - `POST /api/search` — full search endpoint with caching and limits

6. **Lead CRUD** (`api/leads.py`, `services/lead_service.py`):
   - `POST /api/leads` — save a business from search results
   - `GET /api/leads` — list saved leads with filters, pagination, full-text search
   - `GET /api/leads/{id}` — lead detail with notes and reminders
   - `PATCH /api/leads/{id}` — update status, priority, contact info
   - `DELETE /api/leads/{id}` — remove saved lead
   - Duplicate detection (by google_place_id per user)
   - Lead count enforcement per tier

7. **Notes CRUD** (`api/notes.py`):
   - `POST /api/leads/{id}/notes` — add note
   - `GET /api/leads/{id}/notes` — list notes (newest first)
   - `PATCH /api/leads/{id}/notes/{note_id}` — edit note
   - `DELETE /api/leads/{id}/notes/{note_id}` — delete note

8. **Reminders CRUD** (`api/reminders.py`):
   - `POST /api/leads/{id}/reminders` — create reminder
   - `GET /api/reminders` — list all reminders (with upcoming filter)
   - `GET /api/reminders/due-today` — today's reminders
   - `PATCH /api/reminders/{id}` — mark complete, reschedule
   - Background task: check for due reminders → send email notification

### 3.2 Verification

```bash
# Run full test suite
pytest tests/ -v

# Manual API testing
# 1. Signup → verify email → login → get token
# 2. Search "restaurants in Austin TX" → get results
# 3. Save a lead → add note → set reminder → change status
# 4. Search again → same results (from cache, no API call)
# 5. Check usage limits work (10 searches on free tier)
```

---

## 4. Phase 2 — Frontend Core (Weeks 2-3)

**Goal:** Build the web UI for search, lead management, and basic dashboard.

### 4.1 Tasks

1. **Auth pages** (`(auth)/`):
   - Signup page with email + password form
   - Login page with email/password + magic link option
   - Email verification page
   - Token management (store in httpOnly cookie via API)

2. **Dashboard layout** (`(dashboard)/layout.tsx`):
   - Sidebar navigation: Dashboard, Search, Leads, Pipeline, Reminders, Settings
   - Top bar with user avatar, plan badge, notifications bell
   - Mobile responsive: sidebar collapses to hamburger menu

3. **Search page** (`(dashboard)/search/page.tsx`):
   - Search form: category input, location input (with Google Autocomplete), radius slider
   - Results grid: business cards showing name, rating, address, phone, website, [Save] button
   - Loading skeleton states
   - "X of Y searches used this month" indicator
   - Empty state: "Search for your first leads"

4. **Leads list page** (`(dashboard)/leads/page.tsx`):
   - Table/grid view of saved leads
   - Filter bar: status dropdown, search box, sort by (date, name, rating)
   - Status badge (color-coded: New=gray, Contacted=blue, Meeting=yellow, Proposal=orange, Won=green, Lost=red)
   - Quick actions: change status, delete
   - Pagination

5. **Lead detail page** (`(dashboard)/leads/[id]/page.tsx`):
   - Business info card (name, address, phone, website, rating, map pin)
   - Status selector + priority selector
   - Contact info section (editable: contact name, email, phone)
   - Notes timeline (newest first) with add-note form
   - Reminders list with add-reminder form
   - Tags section

6. **Dashboard home** (`(dashboard)/page.tsx`):
   - Stat cards: Total leads, Due today, Won this month, Conversion rate
   - Today's reminders list (with "mark done" checkboxes)
   - Recent activity feed
   - Quick search shortcut

7. **Settings page** (`(dashboard)/settings/page.tsx`):
   - Profile: name, email, company, avatar
   - Password change
   - Notification preferences
   - Account deletion

### 4.2 Verification

```
Manual testing checklist:
□ Sign up with email → verify → land on dashboard
□ Search "plumbers in Denver" → see 20 results
□ Save 3 leads → appear in Leads list
□ Open a lead → add note → set reminder → change to "Contacted"
□ Dashboard shows correct stats and today's reminders
□ Mobile responsive: all pages usable on phone-width browser
□ Settings: change name, change password
```

---

## 5. Phase 3 — CRM Features (Weeks 3-4)

**Goal:** Add pipeline view, tags, bulk actions, and activity timeline.

### 5.1 Tasks

1. **Pipeline (Kanban) view** (`(dashboard)/pipeline/page.tsx`):
   - Drag-and-drop Kanban board with columns: New | Contacted | Meeting | Proposal | Won | Lost
   - Lead cards in each column showing name, rating, next follow-up date
   - Drag card between columns to change status
   - Column counts and totals
   - Library: `@dnd-kit/core` for drag-and-drop

2. **Tags system**:
   - Backend: tags CRUD, lead_tags join table
   - Frontend: tag selector on lead detail, tag filter on leads list
   - Color-coded tag badges
   - Create new tags inline

3. **Bulk actions**:
   - Multi-select checkboxes on leads list
   - Bulk toolbar: "Change status", "Add tag", "Delete" for selected leads
   - Confirmation dialog for destructive actions

4. **Activity timeline** (on lead detail):
   - Chronological list of all events for a lead:
     - Note added
     - Status changed (from → to)
     - Reminder created/completed
     - Tag added/removed
     - Lead saved (created)
   - Backend: `ActivityLog` or derive from existing data timestamps

5. **Reminders page** (`(dashboard)/reminders/page.tsx`):
   - Calendar-style view of upcoming reminders
   - Overdue reminders highlighted in red
   - Quick-complete checkbox
   - Link to lead detail for each reminder

6. **Pipeline analytics** (`api/analytics.py`):
   - `GET /api/pipeline/stats` — counts per status, conversion rate
   - `GET /api/analytics/funnel` — funnel from search → save → contact → win

### 5.2 Verification

```
□ Pipeline Kanban: drag lead from "New" to "Contacted" → status updates
□ Tags: create "hot-lead" tag, assign to 3 leads, filter by tag
□ Bulk: select 5 leads → bulk change to "Contacted" → all update
□ Activity: open lead → see full history of changes
□ Reminders page: see upcoming reminders, mark one complete
□ Analytics: funnel chart shows correct conversion numbers
```

---

## 6. Phase 4 — Billing + Usage Limits (Week 4)

**Goal:** Integrate Stripe, enforce tier limits, and implement upgrade flows.

### 6.1 Tasks

1. **Stripe setup**:
   - Create Stripe account and products/prices for all tiers
   - Configure webhook endpoint in Stripe dashboard
   - Set up `stripe` Python SDK

2. **Backend billing** (`api/billing.py`, `services/billing_service.py`):
   - `POST /api/billing/create-checkout-session` — redirect to Stripe Checkout
   - `POST /api/billing/create-portal-session` — Stripe Customer Portal
   - `POST /api/billing/webhook` — handle all Stripe events
   - `GET /api/billing/subscription` — current subscription info
   - On signup: create Stripe customer, associate with user

3. **Usage enforcement middleware** (`core/dependencies.py`):
   - Check lead count against tier limit on `POST /api/leads`
   - Check search count against tier limit on `POST /api/search`
   - Check team member count on team invite
   - Return 402 with upgrade prompt when limit exceeded

4. **Frontend billing** (`(dashboard)/billing/page.tsx`):
   - Current plan card with usage meters (X of Y leads, X of Y searches)
   - Pricing table comparing all tiers
   - "Upgrade" button → Stripe Checkout redirect
   - "Manage Subscription" → Stripe Customer Portal
   - Cancel subscription flow with exit survey

5. **Upgrade prompts** (throughout the app):
   - When saving 45th of 50 leads: yellow banner "5 leads remaining"
   - When hitting limit: modal with pricing and "Upgrade Now"
   - On premium features (export, team): lock icon with "Available on Starter+"
   - Usage progress bars on dashboard

6. **Post-payment flow**:
   - Stripe webhook updates subscription in DB
   - User sees updated limits immediately (Redis cache invalidation)
   - Welcome-to-plan email sent via Resend

### 6.2 Verification

```
□ Free user: can save 50 leads, gets blocked on 51st with upgrade modal
□ Free user: can do 10 searches, gets blocked on 11th
□ Click "Upgrade" → Stripe Checkout → pay $19 → return to app → limits updated
□ Stripe Portal: can change plan, update card, cancel
□ Cancel subscription → downgrade to free (keep existing leads, just can't add more over 50)
□ Webhook: simulate payment_failed → user gets warning email
```

---

## 7. Phase 5 — Launch Preparation (Week 5)

**Goal:** Polish the product, build the landing page, set up analytics, and prepare for public launch.

### 7.1 Marketing Website Tasks

1. **Landing page** (`(marketing)/page.tsx`):
   - Hero: headline + subheadline + CTA ("Start Free") + product screenshot
   - Problem/solution section: "You currently" vs "With LeadLocal"
   - Feature showcase: Search, Save, Track, Close — with screenshots
   - Social proof: testimonials (from beta users or create placeholder)
   - Pricing table: Free / Starter / Pro / Agency with feature comparison
   - FAQ section
   - Footer: links, legal, social media

2. **Pricing page** (`(marketing)/pricing/page.tsx`):
   - Detailed pricing table with all features per tier
   - Monthly/Annual toggle
   - "Start Free" buttons on every tier
   - FAQ about billing

3. **SEO foundation**:
   - Meta titles/descriptions for all pages
   - Open Graph images for social sharing
   - Sitemap.xml and robots.txt
   - Blog section placeholder (for future SEO content)

### 7.2 Analytics + Monitoring

1. **PostHog integration** (frontend):
   - Track key events: `signup`, `search`, `lead_saved`, `status_changed`, `upgrade_clicked`, `payment_completed`
   - Set up funnels: Signup → First Search → First Lead Saved → Upgrade
   - User identification with email
   - Feature flags for gradual rollout

2. **BetterUptime**:
   - Monitor `api.leadlocal.io/health` every 60 seconds
   - Set up status page at `status.leadlocal.io`
   - Alert via email on downtime

3. **Sentry**:
   - Configure for both backend (FastAPI) and frontend (Next.js)
   - Set up alerts for error spike detection

### 7.3 Polish

1. **Email templates** (Resend):
   - Welcome email (with getting-started tips)
   - Email verification
   - Magic link login
   - Reminder notification ("You have a follow-up with Joe's Pizza today")
   - Upgrade nudge ("You've used 80% of your free leads")
   - Payment confirmation
   - Payment failed warning

2. **Loading states and error handling**:
   - Skeleton loading on all data-fetching pages
   - Toast notifications for actions (saved, deleted, updated)
   - Error boundaries with friendly messages
   - Offline/network error handling

3. **Security audit**:
   - CORS configuration (frontend domain only)
   - Rate limiting on all endpoints
   - Input sanitization on all user inputs
   - SQL injection protection (ORM only)
   - Stripe webhook signature verification

### 7.4 Verification — Full E2E Checklist

```
Complete user journey:
□ Visit leadlocal.io → landing page loads fast (< 2s)
□ Click "Start Free" → signup → verify email → dashboard
□ Search "restaurants in Chicago" → see 20 results (< 3s)
□ Save 5 leads → appear in leads list + pipeline
□ Open lead → add note → set reminder for tomorrow
□ Change lead to "Contacted"
□ Pipeline view → drag lead to "Meeting"
□ Dashboard → see stats + today's reminders
□ Settings → change name
□ Hit 50 lead limit → upgrade modal appears
□ Click upgrade → Stripe → pay $19 → limits increased
□ Log out → log back in → all data preserved
□ Mobile: repeat key flows on phone browser
```

### 7.5 Commercial Milestone

**MVP is ready for public launch.** Product is functional, billing works, landing page converts.

---

## 8. Phase 6 — Launch + Iteration (Weeks 5-8)

**Goal:** Launch publicly, acquire first users, gather feedback, iterate.

### 8.1 Launch Channels

| Channel | Action | Expected Result |
|---------|--------|----------------|
| **Product Hunt** | Submit with compelling tagline, screenshots, and video demo | 100-500 signups in first week |
| **Indie Hackers** | Post "Show IH" with MRR updates and learnings | 50-200 signups, community feedback |
| **Reddit** | Post in r/SaaS, r/Entrepreneur, r/sales, r/freelance | 50-100 signups |
| **Twitter/X** | Build-in-public thread, product screenshots | Ongoing awareness |
| **LinkedIn** | Post targeting sales professionals and agency owners | Ongoing B2B signups |
| **Direct outreach** | Email 50 people in target personas personally | 5-10 high-quality beta users |

> Cross-reference: Full launch strategy in [go-to-market.md](go-to-market.md).

### 8.2 Feedback-Driven Iteration

**Week 6-7:** Collect and prioritize user feedback
- In-app feedback widget (PostHog survey or Canny)
- 15-minute user interviews with first 10 users
- Track drop-off points in PostHog funnels
- Identify #1 requested feature

**Week 7-8:** Ship top 3 user requests
- Typical requests expected: CSV export, more search filters, better mobile experience
- Ship fast: 2-3 day iteration cycles
- Announce improvements via email + changelog

### 8.3 Commercial Milestones

| Week | Target |
|------|--------|
| Week 6 | 100+ free signups |
| Week 7 | 5+ paying customers |
| Week 8 | $500+ MRR, < 10% week-over-week churn |

---

## 9. Phase 7 — Growth Features (Weeks 8-12)

**Goal:** Build features that increase retention, conversion, and expansion revenue.

### 9.1 CSV Export (Starter+ tier)

- Backend: `POST /api/export/csv` — generate CSV of saved leads (filtered)
- Frontend: Export button on leads list with filter options
- Async generation → download link via email for large exports
- **Revenue impact:** Key conversion trigger for Free → Starter upgrade

### 9.2 Email Integration (Pro+ tier)

- Connect Gmail/Outlook via OAuth
- Detect emails to/from lead email addresses → auto-log to lead timeline
- Send email from within lead detail page
- **Revenue impact:** Major retention driver for Pro tier

### 9.3 Multi-Source Search (All tiers)

- Add Yelp Fusion + Foursquare as additional data sources
- Merge results by business name + address similarity
- Show combined rating (average across sources)
- Show review counts from each source
- **Revenue impact:** More data = more value = higher satisfaction

### 9.4 Team Features (Pro/Agency tier)

- Backend: team CRUD, invite-by-email, role management
- Frontend: team settings page, shared pipeline view
- Lead assignment: assign leads to team members
- Activity: see team-wide activity log
- **Revenue impact:** Expansion revenue (per-seat pricing on team plans)

### 9.5 Chrome Extension

- "Save to LeadLocal" button appears when browsing Google Maps, Yelp, any business website
- Click → auto-extract business info → save to LeadLocal pipeline
- **Revenue impact:** Growth through daily active usage + word-of-mouth

### 9.6 Analytics Dashboard (Pro+ tier)

- Conversion funnel: Search → Save → Contact → Meet → Propose → Win
- Charts: leads by status, leads over time, response rates by category
- Benchmarks: "Restaurants in your area have 12% contact-to-meeting rate"
- **Revenue impact:** Pro tier differentiator

---

## 10. Phase 8 — Scale and Optimize (Months 3-6)

### 10.1 Performance Optimization

| Area | Action |
|------|--------|
| Database | Add read replica for search queries, optimize slow queries (pg_stat) |
| Caching | Tune Redis TTLs based on cache hit rates, add local memory cache for hot data |
| API | Profile with py-spy, optimize serialization, add response compression |
| Frontend | Code splitting, image optimization, prefetch dashboard data |
| Search | Pre-warm cache for popular queries (restaurants, dentists in top cities) |

### 10.2 SEO Content Strategy

Publish blog posts targeting long-tail keywords:
- "How to find local businesses to sell to"
- "Best tools for local business prospecting"
- "Cold outreach templates for [insurance/marketing/web design] agencies"
- "Google Places API for lead generation"
- Each article drives organic signups

### 10.3 Advanced Features

- **Territory mapping:** Visual map view of saved leads (color-coded by status)
- **Smart lead scoring:** Auto-score leads by rating, reviews, website quality
- **Email templates:** Pre-built outreach templates per business category
- **Zapier integration:** Connect to 3,000+ tools
- **API access (Agency tier):** REST API for programmatic lead management
- **White-label reports:** Agencies generate branded prospect lists

### 10.4 Commercial Targets

| Metric | Month 3 | Month 6 |
|--------|---------|---------|
| Free users | 500 | 2,000 |
| Paid users | 100 | 400 |
| MRR | $3,000 | $12,000 |
| ARR | $36,000 | $144,000 |
| Churn | < 5% | < 3% |
| NPS | > 30 | > 40 |

---

## 11. Technical Debt Management

| Phase | Expected Debt | Payoff Timeline |
|-------|--------------|----------------|
| Phase 1-2 | Minimal test coverage on UI | Phase 5 (E2E tests) |
| Phase 3 | Activity log derived from timestamps (fragile) | Phase 7 (proper event sourcing) |
| Phase 4 | Stripe webhook handling may miss edge cases | Phase 6 (add retry + dead letter queue) |
| Phase 6 | Rushed iteration may skip tests | Phase 8 (dedicated test sprint) |
| Ongoing | Google Places API coupling | Phase 7 (multi-source abstraction layer) |

**Rule:** No tech debt carries more than 2 phases before payoff.

---

## 12. Document Cross-References

| Topic | Document |
|-------|----------|
| Business model and success criteria | [constitution.md](constitution.md) |
| Architecture and component design | [blueprint.md](blueprint.md) |
| Database schemas and API specs | [artifacts.md](artifacts.md) |
| Project file structure | [skeleton.md](skeleton.md) |
| Marketing and growth strategy | [go-to-market.md](go-to-market.md) |
