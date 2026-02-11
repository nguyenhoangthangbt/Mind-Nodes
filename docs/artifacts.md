# LeadLocal — Artifacts Specification

> The reference document for all database schemas, external API integration specs, internal API contracts, and payment webhook definitions.

---

## 1. Database Schema (PostgreSQL)

### 1.1 Entity Relationship Overview

```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  users   │────<│subscriptions │     │  teams   │
└────┬─────┘     └──────────────┘     └────┬─────┘
     │                                      │
     │  ┌──────────────┐                    │
     ├─<│ team_members │>───────────────────┘
     │  └──────────────┘
     │
     ├──<┌──────────┐>──<┌──────────┐
     │   │  leads   │    │  notes   │
     │   └────┬─────┘    └──────────┘
     │        │
     │        ├──<┌────────────┐
     │        │   │ reminders  │
     │        │   └────────────┘
     │        │
     │        └──<┌──────────────┐
     │            │  lead_tags   │>──┌──────┐
     │            └──────────────┘   │ tags │
     │                               └──────┘
     │
     └──<┌───────────────┐
         │ search_logs   │
         └───────────────┘
```

### 1.2 Users Table

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255),              -- NULL for magic-link-only users
    full_name       VARCHAR(255),
    company_name    VARCHAR(255),
    avatar_url      VARCHAR(512),
    status          VARCHAR(20) NOT NULL DEFAULT 'pending_verification',
                    -- pending_verification, active, suspended, deleted
    email_verified  BOOLEAN NOT NULL DEFAULT FALSE,
    last_login_at   TIMESTAMPTZ,
    timezone        VARCHAR(50) DEFAULT 'UTC',
    stripe_customer_id VARCHAR(255) UNIQUE,    -- Stripe customer reference
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe_customer ON users(stripe_customer_id);
```

### 1.3 Subscriptions Table

```sql
CREATE TABLE subscriptions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tier                VARCHAR(20) NOT NULL DEFAULT 'free',
                        -- free, starter, pro, agency
    status              VARCHAR(20) NOT NULL DEFAULT 'active',
                        -- active, past_due, canceled, trialing
    stripe_subscription_id VARCHAR(255) UNIQUE,
    stripe_price_id     VARCHAR(255),
    current_period_start TIMESTAMPTZ,
    current_period_end  TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
    -- Usage tracking (reset monthly)
    searches_used       INTEGER NOT NULL DEFAULT 0,
    searches_reset_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
```

**Tier limits (enforced in application code):**

| Tier | Max Saved Leads | Max Searches/Mo | Max Users | CSV Export | Email Integration | API Access |
|------|----------------|----------------|-----------|------------|-------------------|------------|
| free | 50 | 10 | 1 | No | No | No |
| starter | 500 | 50 | 1 | Yes | No | No |
| pro | 2,000 | 200 | 3 | Yes | Yes | No |
| agency | 10,000 | Unlimited | 10 | Yes | Yes | Yes |

### 1.4 Leads Table

```sql
CREATE TABLE leads (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    team_id         UUID REFERENCES teams(id) ON DELETE SET NULL,

    -- Business identity (from Google Places / other sources)
    google_place_id VARCHAR(255),
    yelp_id         VARCHAR(255),
    foursquare_id   VARCHAR(255),

    -- Denormalized business data (snapshot at save time)
    business_name   VARCHAR(500) NOT NULL,
    address         TEXT,
    city            VARCHAR(255),
    state           VARCHAR(100),
    country         VARCHAR(100),
    postal_code     VARCHAR(20),
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    phone           VARCHAR(50),
    website         VARCHAR(512),
    email           VARCHAR(255),              -- From Hunter.io or manual entry
    rating          DECIMAL(2,1),              -- e.g., 4.5
    reviews_count   INTEGER,
    price_level     SMALLINT,                  -- 1-4 (Google's scale)
    categories      TEXT[],                    -- e.g., {"restaurant", "food"}
    business_status VARCHAR(50),               -- OPERATIONAL, CLOSED, etc.
    opening_hours   JSONB,                     -- Structured hours data
    photos          JSONB,                     -- Array of photo references

    -- CRM fields
    status          VARCHAR(20) NOT NULL DEFAULT 'new',
                    -- new, contacted, meeting, proposal, won, lost, archived
    priority        VARCHAR(10) DEFAULT 'medium',
                    -- low, medium, high
    assigned_to     UUID REFERENCES users(id), -- For team features
    contact_name    VARCHAR(255),              -- Manual: decision-maker name
    contact_email   VARCHAR(255),              -- Manual: decision-maker email
    contact_phone   VARCHAR(50),               -- Manual: decision-maker phone

    -- Metadata
    source          VARCHAR(50) NOT NULL DEFAULT 'google_places',
                    -- google_places, yelp, foursquare, manual, import
    last_contacted_at TIMESTAMPTZ,
    next_followup_at  TIMESTAMPTZ,
    won_at          TIMESTAMPTZ,
    lost_at         TIMESTAMPTZ,
    lost_reason     VARCHAR(500),
    deal_value      DECIMAL(12,2),             -- Optional: estimated deal value

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_leads_user ON leads(user_id);
CREATE INDEX idx_leads_team ON leads(team_id);
CREATE INDEX idx_leads_status ON leads(user_id, status);
CREATE INDEX idx_leads_google_place ON leads(user_id, google_place_id);
CREATE INDEX idx_leads_next_followup ON leads(user_id, next_followup_at)
    WHERE next_followup_at IS NOT NULL;
CREATE INDEX idx_leads_search ON leads USING gin(
    to_tsvector('english', business_name || ' ' || COALESCE(address, ''))
);
```

### 1.5 Notes Table

```sql
CREATE TABLE notes (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id     UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content     TEXT NOT NULL,
    -- Optional: track type of interaction
    note_type   VARCHAR(20) DEFAULT 'general',
                -- general, call, email, meeting, other
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notes_lead ON notes(lead_id);
CREATE INDEX idx_notes_user ON notes(user_id);
CREATE INDEX idx_notes_created ON notes(lead_id, created_at DESC);
```

### 1.6 Reminders Table

```sql
CREATE TABLE reminders (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id     UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(500) NOT NULL,
    due_date    TIMESTAMPTZ NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    -- Notification tracking
    notified    BOOLEAN NOT NULL DEFAULT FALSE,
    notified_at TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_reminders_user_due ON reminders(user_id, due_date)
    WHERE is_completed = FALSE;
CREATE INDEX idx_reminders_lead ON reminders(lead_id);
CREATE INDEX idx_reminders_pending ON reminders(due_date, notified)
    WHERE is_completed = FALSE AND notified = FALSE;
```

### 1.7 Tags Table

```sql
CREATE TABLE tags (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name        VARCHAR(100) NOT NULL,
    color       VARCHAR(7) DEFAULT '#6B7280',  -- Hex color
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_tags_user_name ON tags(user_id, name);

CREATE TABLE lead_tags (
    lead_id     UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    tag_id      UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (lead_id, tag_id)
);
```

### 1.8 Teams Table (Pro/Agency Tier)

```sql
CREATE TABLE teams (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    owner_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE team_members (
    team_id     UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role        VARCHAR(20) NOT NULL DEFAULT 'member',
                -- owner, admin, member
    joined_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (team_id, user_id)
);

CREATE INDEX idx_team_members_user ON team_members(user_id);
```

### 1.9 Search Logs Table (Analytics + Usage Tracking)

```sql
CREATE TABLE search_logs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query       VARCHAR(500) NOT NULL,
    location    VARCHAR(500) NOT NULL,
    radius_km   DECIMAL(6,2),
    results_count INTEGER,
    source      VARCHAR(50) DEFAULT 'google_places',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_search_logs_user ON search_logs(user_id, created_at DESC);
```

---

## 2. External API Integration Specs

### 2.1 Google Places API (New)

**Base URL:** `https://places.googleapis.com/v1/places`

#### Nearby Search

```
POST https://places.googleapis.com/v1/places:searchNearby

Headers:
  X-Goog-Api-Key: {GOOGLE_API_KEY}
  X-Goog-FieldMask: places.id,places.displayName,places.formattedAddress,
    places.location,places.rating,places.userRatingCount,places.types,
    places.businessStatus,places.currentOpeningHours,places.priceLevel,
    places.websiteUri,places.nationalPhoneNumber,places.photos

Body:
{
  "includedTypes": ["restaurant"],
  "maxResultCount": 20,
  "locationRestriction": {
    "circle": {
      "center": { "latitude": 30.2672, "longitude": -97.7431 },
      "radius": 5000.0
    }
  }
}

Response (per place):
{
  "id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
  "displayName": { "text": "Joe's Pizza", "languageCode": "en" },
  "formattedAddress": "123 Main St, Austin, TX 78701",
  "location": { "latitude": 30.2672, "longitude": -97.7431 },
  "rating": 4.5,
  "userRatingCount": 287,
  "types": ["restaurant", "food", "point_of_interest"],
  "businessStatus": "OPERATIONAL",
  "currentOpeningHours": { "openNow": true, "weekdayDescriptions": [...] },
  "priceLevel": "PRICE_LEVEL_MODERATE",
  "websiteUri": "https://joespizza.com",
  "nationalPhoneNumber": "(512) 555-0123",
  "photos": [{ "name": "places/ChIJ.../photos/..." }]
}
```

**Pricing:** $32 per 1,000 Nearby Search calls. Place Details (Basic): $17 per 1,000 calls.

**Rate limit:** 6,000 QPM (queries per minute).

#### Text Search (Alternative)

```
POST https://places.googleapis.com/v1/places:searchText

Body:
{
  "textQuery": "dentists in Miami, FL",
  "maxResultCount": 20
}
```

**Pricing:** $32 per 1,000 calls.

### 2.2 Yelp Fusion API

**Base URL:** `https://api.yelp.com/v3`

```
GET /v3/businesses/search?term=restaurant&location=Austin,TX&radius=5000&limit=50

Headers:
  Authorization: Bearer {YELP_API_KEY}

Response (per business):
{
  "id": "north-italia-austin",
  "name": "North Italia",
  "image_url": "https://s3-media3.fl.yelpcdn.com/...",
  "url": "https://www.yelp.com/biz/north-italia-austin",
  "review_count": 1547,
  "rating": 4.0,
  "phone": "+15125551234",
  "display_phone": "(512) 555-1234",
  "location": {
    "address1": "11506 Century Oaks Terrace",
    "city": "Austin",
    "state": "TX",
    "zip_code": "78758"
  },
  "coordinates": { "latitude": 30.40, "longitude": -97.72 },
  "categories": [{ "alias": "italian", "title": "Italian" }],
  "price": "$$"
}
```

**Free tier:** 5,000 API calls/day. **Rate limit:** 5,000/day total.

### 2.3 Foursquare Places API

**Base URL:** `https://api.foursquare.com/v3/places`

```
GET /v3/places/search?query=restaurant&ll=30.2672,-97.7431&radius=5000&limit=50

Headers:
  Authorization: {FOURSQUARE_API_KEY}

Response (per place):
{
  "fsq_id": "4b5bc1e0f964a520e5c728e3",
  "name": "Torchy's Tacos",
  "location": {
    "formatted_address": "1822 S Congress Ave, Austin, TX 78704"
  },
  "geocodes": { "main": { "latitude": 30.247, "longitude": -97.749 } },
  "categories": [{ "id": 13303, "name": "Mexican Restaurant" }],
  "rating": 8.5,
  "hours": { "display": "Mon-Sun 8:00 AM-10:00 PM" }
}
```

**Free tier:** 200,000 regular calls/month. **Rate limit:** 500/min.

### 2.4 Hunter.io (Email Discovery)

**Base URL:** `https://api.hunter.io/v2`

```
GET /v2/domain-search?domain=joespizza.com&api_key={HUNTER_API_KEY}

Response:
{
  "data": {
    "domain": "joespizza.com",
    "emails": [
      {
        "value": "joe@joespizza.com",
        "type": "personal",
        "confidence": 91,
        "first_name": "Joe",
        "last_name": "Smith",
        "position": "Owner"
      }
    ]
  }
}
```

**Free tier:** 25 searches/month. **Paid:** $49/mo for 500 searches.

---

## 3. Internal REST API Contracts

### 3.1 Authentication Endpoints

```
POST /api/auth/signup
  Body: { email: str, password: str, full_name?: str }
  Response 201: { user_id: str, message: "Verification email sent" }
  Response 409: { error: "email_exists" }

POST /api/auth/login
  Body: { email: str, password: str }
  Response 200: { access_token: str, refresh_token: str, user: UserSchema }
  Response 401: { error: "invalid_credentials" }

POST /api/auth/magic-link
  Body: { email: str }
  Response 200: { message: "Magic link sent" }

GET /api/auth/verify?token={jwt}
  Response 302: Redirect to /dashboard (sets cookie)
  Response 401: { error: "invalid_token" }

POST /api/auth/refresh
  Body: { refresh_token: str }
  Response 200: { access_token: str }

POST /api/auth/logout
  Response 200: { message: "Logged out" }
```

### 3.2 Search Endpoints

```
POST /api/search
  Headers: Authorization: Bearer {token}
  Body: {
    query: str,           -- "restaurant", "dentist", "plumber"
    location: str,        -- "Austin, TX" or "10.7731,106.7030"
    radius_km: float,     -- 1.0 to 50.0 (default: 5.0)
    min_rating?: float,   -- 0.0 to 5.0
    open_now?: bool,      -- filter to currently open
    page_token?: str      -- pagination token for next 20 results
  }
  Response 200: {
    results: LeadSearchResult[],
    next_page_token: str | null,
    total_results: int,
    usage: { searches_used: int, searches_limit: int }
  }
  Response 402: { error: "limit_exceeded", upgrade_url: str }
  Response 429: { error: "rate_limited", retry_after: int }
```

**LeadSearchResult schema:**
```json
{
  "google_place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
  "business_name": "Joe's Pizza",
  "address": "123 Main St, Austin, TX 78701",
  "city": "Austin",
  "state": "TX",
  "country": "US",
  "postal_code": "78701",
  "latitude": 30.2672,
  "longitude": -97.7431,
  "phone": "(512) 555-0123",
  "website": "https://joespizza.com",
  "rating": 4.5,
  "reviews_count": 287,
  "price_level": 2,
  "categories": ["restaurant", "pizza"],
  "business_status": "OPERATIONAL",
  "opening_hours": {
    "open_now": true,
    "weekday_text": ["Monday: 11:00 AM – 10:00 PM", "..."]
  },
  "photo_url": "https://places.googleapis.com/...",
  "is_saved": false,
  "saved_lead_id": null
}
```

### 3.3 Leads Endpoints

```
GET /api/leads
  Query params: status?, tag?, search?, sort_by?, page?, per_page?
  Response 200: { leads: LeadSchema[], total: int, page: int, pages: int }

POST /api/leads
  Body: {
    google_place_id?: str,
    source_data: LeadSearchResult,  -- snapshot of business data
    status?: str,                   -- default: "new"
    tags?: str[]
  }
  Response 201: LeadSchema
  Response 402: { error: "limit_exceeded" }
  Response 409: { error: "duplicate_lead" }

GET /api/leads/{id}
  Response 200: LeadDetailSchema (includes notes, reminders, tags, activity)

PATCH /api/leads/{id}
  Body: { status?, priority?, contact_name?, contact_email?, deal_value?, ... }
  Response 200: LeadSchema

DELETE /api/leads/{id}
  Response 204

POST /api/leads/bulk
  Body: { lead_ids: str[], action: "update_status" | "add_tag" | "delete",
          status?: str, tag_id?: str }
  Response 200: { updated: int }
```

**LeadSchema:**
```json
{
  "id": "uuid",
  "business_name": "Joe's Pizza",
  "address": "123 Main St, Austin, TX 78701",
  "phone": "(512) 555-0123",
  "website": "https://joespizza.com",
  "email": "joe@joespizza.com",
  "rating": 4.5,
  "reviews_count": 287,
  "categories": ["restaurant", "pizza"],
  "status": "contacted",
  "priority": "high",
  "contact_name": "Joe Smith",
  "tags": [{ "id": "uuid", "name": "hot-lead", "color": "#EF4444" }],
  "notes_count": 3,
  "next_followup_at": "2026-02-17T09:00:00Z",
  "last_contacted_at": "2026-02-11T14:30:00Z",
  "deal_value": 5000.00,
  "created_at": "2026-02-10T10:00:00Z",
  "updated_at": "2026-02-11T14:30:00Z"
}
```

### 3.4 Notes Endpoints

```
GET /api/leads/{lead_id}/notes
  Response 200: { notes: NoteSchema[] }

POST /api/leads/{lead_id}/notes
  Body: { content: str, note_type?: str }
  Response 201: NoteSchema

PATCH /api/leads/{lead_id}/notes/{note_id}
  Body: { content: str }
  Response 200: NoteSchema

DELETE /api/leads/{lead_id}/notes/{note_id}
  Response 204
```

### 3.5 Reminders Endpoints

```
GET /api/reminders
  Query params: upcoming? (bool), lead_id?, completed?
  Response 200: { reminders: ReminderSchema[] }

POST /api/leads/{lead_id}/reminders
  Body: { title: str, due_date: datetime }
  Response 201: ReminderSchema

PATCH /api/reminders/{id}
  Body: { title?: str, due_date?: datetime, is_completed?: bool }
  Response 200: ReminderSchema

DELETE /api/reminders/{id}
  Response 204

GET /api/reminders/due-today
  Response 200: { reminders: ReminderWithLeadSchema[] }
```

### 3.6 Pipeline/Analytics Endpoints

```
GET /api/pipeline/stats
  Response 200: {
    by_status: { new: 12, contacted: 8, meeting: 3, proposal: 2, won: 5, lost: 4 },
    total_saved: 34,
    total_limit: 500,
    conversion_rate: 14.7,       -- won / (won + lost) %
    avg_time_to_close_days: 12.5,
    total_deal_value: 25000.00
  }

GET /api/analytics/funnel
  Query params: period? (7d, 30d, 90d)
  Response 200: {
    period: "30d",
    searches: 45,
    leads_saved: 28,
    contacted: 15,
    meetings: 5,
    proposals: 3,
    won: 2,
    lost: 1
  }
```

### 3.7 Billing Endpoints

```
POST /api/billing/create-checkout-session
  Body: { plan: "starter" | "pro" | "agency", annual?: bool }
  Response 200: { checkout_url: str }

POST /api/billing/create-portal-session
  Response 200: { portal_url: str }
  -- Stripe Customer Portal for managing subscription

GET /api/billing/subscription
  Response 200: SubscriptionSchema

POST /api/billing/webhook   (Stripe signature verified)
  -- Handles all Stripe webhook events
  Response 200
```

### 3.8 Export Endpoints

```
POST /api/export/csv
  Body: { filters?: { status?, tags?, date_range? } }
  Response 200: { download_url: str, expires_at: datetime }
  Response 402: { error: "export_not_available", required_plan: "starter" }
```

---

## 4. Stripe Webhook Events

### 4.1 Handled Events

| Event | Handler Action |
|-------|---------------|
| `checkout.session.completed` | Create Subscription record, update user tier, send welcome email |
| `invoice.payment_succeeded` | Update subscription period dates, reset monthly usage counters |
| `invoice.payment_failed` | Set subscription status to `past_due`, send payment failed email, start 7-day grace period |
| `customer.subscription.updated` | Sync tier changes (upgrade/downgrade), update limits |
| `customer.subscription.deleted` | Downgrade to free tier, send cancellation email, retain data |

### 4.2 Stripe Price IDs Configuration

```python
STRIPE_PRICES = {
    "starter_monthly": "price_xxxx_starter_monthly",    # $19/mo
    "starter_annual": "price_xxxx_starter_annual",      # $190/yr
    "pro_monthly": "price_xxxx_pro_monthly",            # $39/mo
    "pro_annual": "price_xxxx_pro_annual",              # $390/yr
    "agency_monthly": "price_xxxx_agency_monthly",      # $79/mo
    "agency_annual": "price_xxxx_agency_annual",        # $790/yr
}
```

### 4.3 Webhook Signature Verification

```python
import stripe

@router.post("/api/billing/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    # Process event...
```

---

## 5. Environment Configuration Schema

```bash
# .env file schema (all required unless noted)

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/leadlocal

# Redis
REDIS_URL=redis://host:6379/0

# Auth
JWT_SECRET_KEY=<random-64-char-string>
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
MAGIC_LINK_EXPIRE_MINUTES=15

# Google Places API
GOOGLE_PLACES_API_KEY=AIza...

# Yelp (optional, post-MVP)
YELP_API_KEY=<key>

# Foursquare (optional, post-MVP)
FOURSQUARE_API_KEY=<key>

# Hunter.io (optional, post-MVP)
HUNTER_API_KEY=<key>

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_STARTER_MONTHLY_PRICE_ID=price_...
STRIPE_STARTER_ANNUAL_PRICE_ID=price_...
STRIPE_PRO_MONTHLY_PRICE_ID=price_...
STRIPE_PRO_ANNUAL_PRICE_ID=price_...
STRIPE_AGENCY_MONTHLY_PRICE_ID=price_...
STRIPE_AGENCY_ANNUAL_PRICE_ID=price_...

# Email (Resend)
RESEND_API_KEY=re_...
FROM_EMAIL=hello@leadlocal.io

# App
APP_URL=https://leadlocal.io
API_URL=https://api.leadlocal.io
ENVIRONMENT=production  # development, staging, production

# Sentry (optional)
SENTRY_DSN=https://...@sentry.io/...

# PostHog (optional)
POSTHOG_API_KEY=phc_...
```

---

## 6. Unified Lead Data Schema

When merging data from multiple sources, normalize to this structure:

```python
class UnifiedLead(BaseModel):
    """Normalized business data from any source."""

    # Identity
    google_place_id: str | None = None
    yelp_id: str | None = None
    foursquare_id: str | None = None

    # Core fields
    business_name: str
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    # Contact
    phone: str | None = None
    website: str | None = None
    email: str | None = None  # From Hunter.io or manual

    # Ratings (normalized to 0-5 scale)
    rating: float | None = None  # Google: 0-5, Yelp: 0-5, FSQ: 0-10 → /2
    reviews_count: int | None = None
    price_level: int | None = None  # 1-4

    # Metadata
    categories: list[str] = []
    business_status: str = "OPERATIONAL"
    opening_hours: dict | None = None
    photo_url: str | None = None
    source: str = "google_places"
```

---

## 7. Document Cross-References

| Topic | Document |
|-------|----------|
| Pricing tiers and business model | [constitution.md](constitution.md) Section 4 |
| Architecture and tech stack decisions | [blueprint.md](blueprint.md) |
| Build phases using these schemas | [implementation-guide.md](implementation-guide.md) |
| File locations for these modules | [skeleton.md](skeleton.md) |
| How billing supports GTM strategy | [go-to-market.md](go-to-market.md) |
