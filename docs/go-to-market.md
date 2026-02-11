# LeadLocal — Go-to-Market Strategy

> The commercialization playbook covering launch strategy, marketing channels, conversion optimization, pricing experiments, growth loops, and retention tactics.

---

## 1. Pre-Launch (Weeks 1-5, While Building)

### 1.1 Build in Public

Start marketing **before the product is finished.** Every week of building is a marketing opportunity.

| Platform | Action | Frequency |
|----------|--------|-----------|
| **Twitter/X** | Share build progress, screenshots, decisions, struggles | 3-5 posts/week |
| **LinkedIn** | Professional updates targeting sales professionals | 2 posts/week |
| **Indie Hackers** | Weekly milestone updates in a build log | Weekly |
| **Reddit** (r/SaaS, r/startups) | Share learnings, ask for feedback | Biweekly |

**Content formula for build-in-public posts:**
```
Week 1: "I'm building a tool that finds local businesses and tracks your outreach. Here's why."
Week 2: "Got Google Places API working. Here's how much it costs per search."  [screenshot]
Week 3: "Built the Kanban pipeline. Drag a lead from 'New' to 'Contacted'."  [gif]
Week 4: "Adding Stripe billing. Here's my pricing and why."  [pricing table]
Week 5: "MVP is live. First 50 users get lifetime 50% off."  [link]
```

### 1.2 Waitlist Landing Page (Week 1)

Before the product is ready, launch a simple landing page:

```
Headline: "Find Local Businesses. Close Them. One Tool."
Subheadline: "Stop juggling Google Maps and spreadsheets.
              Search → Save → Track → Close."
CTA: "Join the Waitlist — Get Early Access"
Email capture → store in a simple list (Resend audience or Google Sheet)
```

**Goal:** 200+ emails on the waitlist before launch.

### 1.3 Early Access / Beta Program (Week 4)

- Invite 20-30 people from the waitlist for beta testing
- Offer: "Free Pro plan for 3 months in exchange for feedback"
- Weekly 15-minute feedback calls with 5-10 beta users
- Create a private Slack/Discord channel for beta testers
- **Goal:** 5+ testimonials and 20+ bug reports before public launch

---

## 2. Launch Strategy (Week 5-6)

### 2.1 Launch Day Checklist

```
Pre-launch (day before):
□ Final QA pass on all critical flows
□ Prepare Product Hunt launch assets (logo, screenshots, video, tagline)
□ Write announcement posts for all channels
□ Pre-notify waitlist: "Launching tomorrow — be first!"
□ Set up Stripe in live mode
□ Enable PostHog analytics tracking

Launch day:
□ 12:01 AM PT: Product Hunt submission goes live
□ 7:00 AM: Tweet announcement + LinkedIn post
□ 8:00 AM: Indie Hackers "Show IH" post
□ 9:00 AM: Reddit posts (r/SaaS, r/Entrepreneur, r/sales, r/smallbusiness)
□ 10:00 AM: Email waitlist with launch link + early-bird offer
□ All day: Respond to every PH comment, tweet, and question
□ All day: Monitor Sentry for errors, PostHog for funnels

Post-launch (day after):
□ Thank everyone who upvoted/commented
□ Share launch results and learnings
□ Fix any critical bugs discovered
□ Send personal thank-you to first paying customers
```

### 2.2 Product Hunt Launch

| Asset | Specification |
|-------|--------------|
| **Tagline** | "Find local businesses and track your outreach — no spreadsheets" |
| **Description** | 3-paragraph story: problem → solution → how it works |
| **Screenshots** | 4-5 high-quality product screenshots: search, lead detail, pipeline, dashboard |
| **Video** | 60-second demo showing: search → save → note → pipeline (Loom or screen recording) |
| **Maker comment** | Personal story: why you built this, what makes it different |
| **First comment** | Ask a question to encourage discussion: "What's your current local prospecting workflow?" |

**Expected results:** 100-500 signups, 3-20 paying customers in first week.

### 2.3 Early-Bird Pricing

| Offer | Duration | Discount |
|-------|----------|----------|
| Waitlist subscribers | First 7 days | 50% off first 3 months |
| Product Hunt launch day | 24 hours | 30% off first year (annual only) |
| First 100 paying customers | Until filled | Locked at launch price forever (even if prices increase later) |

**Psychology:** Urgency + exclusivity + fear of price increase.

---

## 3. Customer Acquisition Channels

### 3.1 Channel Priority Matrix

| Channel | Cost | Time to Results | Scalability | Priority |
|---------|------|----------------|-------------|----------|
| **SEO / Content** | Low ($0) | 3-6 months | High | **#1 long-term** |
| **Build-in-public / Social** | Low ($0) | 1-2 months | Medium | **#1 short-term** |
| **Product Hunt / IH** | Low ($0) | Immediate | One-time spike | **Launch only** |
| **Word of mouth / Referral** | Low ($0) | 2-4 months | High | **#2 long-term** |
| **Cold outreach to agencies** | Low ($0) | 1-2 weeks | Low | **Quick wins** |
| **Google Ads** | Medium ($200-500/mo) | Immediate | Medium | **After PMF** |
| **Content partnerships** | Low ($0) | 1-3 months | Medium | **Month 3+** |
| **Affiliate program** | Medium (20-30% rev share) | 2-3 months | High | **Month 6+** |

### 3.2 SEO Content Strategy (Primary Long-Term Channel)

**Target keywords and content:**

| Keyword Cluster | Monthly Search Volume | Content Type | Conversion Intent |
|----------------|----------------------|-------------|-------------------|
| "how to find local business leads" | 500-1,000 | Blog post + tool mention | High |
| "local business prospecting tools" | 300-500 | Comparison post (us vs others) | Very high |
| "google maps for lead generation" | 1,000-2,000 | How-to guide | High |
| "cold email templates for [industry]" | 2,000-5,000 per industry | Template library | Medium |
| "CRM for freelancers" | 1,000-2,000 | Review/comparison | High |
| "how to sell to local businesses" | 500-1,000 | Strategy guide | Medium |
| "sales prospecting for insurance agents" | 300-500 | Niche guide | Very high |
| "marketing agency client acquisition" | 500-1,000 | Playbook | Very high |

**Content calendar (first 3 months):**

| Month | Posts | Focus |
|-------|-------|-------|
| Month 1 | 4 posts | Product-led: "How to use Google Places API for lead gen", "Best tools for local prospecting 2026" |
| Month 2 | 4 posts | Persona-led: "How insurance agents find local business clients", "Agency owner's guide to cold outreach" |
| Month 3 | 4 posts | Template-led: "50 cold email templates for local businesses", "Follow-up sequence that gets replies" |

**Each post:** 1,500-2,500 words, includes product screenshots, ends with CTA to sign up.

### 3.3 Direct Outreach to Agencies (Quick Wins)

**Week 6-8:** Personally contact 50 digital marketing agencies:

```
Subject: Found a tool that might save your team 5 hrs/week on prospecting

Hi [Name],

I noticed [Agency Name] does SEO/web design for local businesses.

I just launched LeadLocal — it lets you search for businesses by
category and location (like "restaurants in [city]"), then track
your outreach with notes and follow-ups. No more spreadsheets.

Would love your feedback. I'll give you free Pro access for 3 months.

[Link to app]

Best,
[Your name]
```

**Expected response rate:** 10-20% (because it's genuinely useful for them).
**Goal:** 5-10 agency users → 2-3 paying Agency tier customers ($79/mo each).

### 3.4 Referral Program (Month 3+)

```
How it works:
- Every user gets a unique referral link
- When a referred user upgrades to paid: referrer gets 1 month free
- Referred user gets 20% off first month
- Tracked via referral code in signup URL

Implementation:
- Add referral_code field to users table
- Generate unique codes on signup
- Track conversions in analytics
- Apply credits automatically via Stripe coupons
```

---

## 4. Conversion Optimization

### 4.1 Signup-to-Active Funnel

```
Target funnel:
  Visit landing page          100%
  → Click "Start Free"         15-25%     (landing page conversion)
  → Complete signup             60-80%     (of those who click)
  → Verify email                70-85%     (of signups)
  → First search                80-90%     (of verified)
  → Save first lead             60-70%     (of searchers)
  → Add first note              30-40%     (of savers) ← "activated"
  → Return next day             40-50%     (of activated)
```

### 4.2 Activation Tactics

**Goal:** Get every new user to the "aha moment" as fast as possible.

The aha moment = **user searches → sees real businesses → saves one → adds a note.**

| Tactic | Implementation |
|--------|---------------|
| **Auto-search on first visit** | If user allows location: auto-search "popular businesses near you" on first dashboard load |
| **Guided onboarding** | 3-step tooltip: "1. Search for a business type" → "2. Save a lead" → "3. Add a note" |
| **Pre-filled search** | Show popular searches: "Try: Restaurants, Dentists, Plumbers, Real Estate Agents" |
| **Empty state messaging** | On empty leads list: "You haven't saved any leads yet. Search now!" with big CTA |
| **24-hour follow-up email** | If user signed up but didn't search: "Welcome! Here's how to find your first leads in 30 seconds" |
| **72-hour nudge** | If user searched but didn't save: "You found 20 businesses near you. Save your top picks before they're buried!" |

### 4.3 Free-to-Paid Conversion Tactics

**Target:** > 5% of free users convert to paid within 30 days.

| Tactic | Trigger | Message |
|--------|---------|---------|
| **Soft limit warning** | 40 of 50 leads used | Yellow banner: "10 leads remaining on Free plan" |
| **Hard limit block** | 50 of 50 leads used | Modal: "You've saved 50 leads. Upgrade to keep growing your pipeline." |
| **Feature gate** | User tries to export CSV | Lock icon: "CSV export available on Starter plan. Upgrade for $19/mo." |
| **Usage summary email** | Weekly (Mondays) | "This week: 3 leads contacted, 1 meeting booked. Upgrade to manage 500+ leads." |
| **Trial offer** | After 14 days on free | "Try Pro free for 7 days — full access, no credit card." |
| **Annual discount highlight** | On billing page | "Save 17% with annual billing — that's 2 months free!" |

### 4.4 Pricing Page Optimization

```
Psychological principles applied:

1. Anchor with Agency ($79/mo) — makes Pro ($39/mo) look reasonable
2. Highlight Pro as "Most Popular" — social proof badge
3. Show monthly price crossed out next to annual price — loss aversion
4. Feature comparison table — shows free is limited
5. "Start Free" on every tier — low friction entry
6. Money-back guarantee: "Cancel anytime, no questions"
7. Social proof: "Trusted by 500+ sales professionals"
```

---

## 5. Retention Strategy

### 5.1 Retention Metrics Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Day 1 retention | > 60% | % who return the day after signup |
| Day 7 retention | > 40% | % who return within first week |
| Day 30 retention | > 25% | % active in first month |
| Monthly churn (paid) | < 5% | % paid users who cancel per month |
| Net Revenue Retention | > 100% | Revenue from existing customers (including upgrades) |

### 5.2 Retention Tactics

| Tactic | Implementation |
|--------|---------------|
| **Daily reminder emails** | "You have 3 follow-ups due today" — brings users back |
| **Weekly pipeline summary** | Monday email: "Last week: 5 contacted, 2 meetings. This week: 3 follow-ups due." |
| **Streak tracking** | "You've been prospecting for 12 days straight!" — gamification |
| **Milestone celebrations** | "Congrats! You've saved 100 leads!" — email + in-app toast |
| **Feature discovery** | Contextual tooltips for features users haven't tried: "Did you know you can tag leads?" |
| **Integration stickiness** | Email integration (Phase 7) makes switching painful |
| **Data lock-in** | Users' notes, pipeline history, and contact info are irreplaceable |

### 5.3 Churn Prevention

| Warning Signal | Intervention |
|---------------|-------------|
| No login for 7 days | Email: "Your pipeline is waiting — 2 follow-ups overdue" |
| No login for 14 days | Email: "We miss you! Here are 5 new businesses matching your last search" |
| No login for 30 days | Email: personal note from founder asking what went wrong |
| Cancellation initiated | Exit survey + offer: "Stay for 50% off next month?" |
| Payment failed | 3 retry emails over 7 days + grace period before downgrade |

---

## 6. Growth Loops

### 6.1 Viral Loop: Shared Reports (Phase 8)

```
Agency user generates prospect report for a client
→ Report has "Powered by LeadLocal" footer
→ Client's contact sees LeadLocal branding
→ Contact signs up to try LeadLocal
→ Becomes a user → generates their own reports
→ Repeat
```

### 6.2 Content Loop: SEO Flywheel

```
Publish blog post targeting "[industry] prospecting tips"
→ Google indexes → organic traffic arrives
→ Readers sign up for free account
→ Some convert to paid
→ Revenue funds more content
→ More content → more traffic → more signups
→ Repeat (compounds over months)
```

### 6.3 Referral Loop

```
User has success (books meeting, wins deal)
→ Happy moment → prompt: "Share LeadLocal with a colleague?"
→ Referral link shared
→ Colleague signs up and gets 20% off
→ Original user gets 1 month free
→ Both users are more engaged
→ Repeat
```

### 6.4 Data Network Effect (Long-term)

```
More users save leads and track outcomes
→ Aggregate data: "Restaurants in Austin: 15% contact-to-meeting rate"
→ Show anonymized benchmarks to all users
→ Benchmarks make the product more valuable
→ More users join for the intelligence layer
→ Better data → better benchmarks
→ Repeat
```

---

## 7. Financial Projections

### 7.1 Conservative Scenario

| Month | Free Users | Paid Users | ARPU | MRR | Cumulative Revenue |
|-------|-----------|-----------|------|-----|-------------------|
| 1 | 50 | 3 | $25 | $75 | $75 |
| 2 | 150 | 12 | $27 | $324 | $399 |
| 3 | 300 | 30 | $28 | $840 | $1,239 |
| 4 | 450 | 55 | $29 | $1,595 | $2,834 |
| 5 | 600 | 80 | $30 | $2,400 | $5,234 |
| 6 | 800 | 110 | $30 | $3,300 | $8,534 |
| 9 | 1,500 | 220 | $32 | $7,040 | $26,654 |
| 12 | 2,500 | 400 | $33 | $13,200 | $65,054 |

### 7.2 Optimistic Scenario (Strong Product-Market Fit)

| Month | Free Users | Paid Users | ARPU | MRR |
|-------|-----------|-----------|------|-----|
| 3 | 500 | 50 | $30 | $1,500 |
| 6 | 2,000 | 250 | $33 | $8,250 |
| 12 | 5,000 | 800 | $35 | $28,000 |

### 7.3 Break-Even Analysis

```
Fixed costs (monthly):
  Hosting (Railway + Vercel + Redis):     $50
  Google Places API:                      ~$200 (at 500 users)
  Email (Resend):                         $20
  Domain + Cloudflare:                    $15
  Monitoring (Sentry, PostHog):           $0 (free tiers)
  Total fixed:                            ~$285/mo

Variable costs per paid user:
  Google API (~5 searches/user/day):      ~$3/user/mo
  Stripe fees (2.9% + $0.30):            ~$1.20/user/mo
  Total variable:                         ~$4.20/user/mo

Break-even:
  At $30 ARPU, margin per user = $30 - $4.20 = $25.80
  Fixed costs / margin = $285 / $25.80 = ~11 paid users

  → Break-even at approximately 11 paying customers.
```

---

## 8. Key Metrics Dashboard

Track these metrics weekly:

### 8.1 Acquisition

| Metric | How to Measure |
|--------|---------------|
| Website visitors | PostHog / Vercel Analytics |
| Signup rate | Signups / visitors |
| Signups this week | PostHog event: `signup` |
| Activation rate | % who save first lead within 24h |
| Source attribution | UTM parameters on signup |

### 8.2 Revenue

| Metric | How to Measure |
|--------|---------------|
| MRR | Stripe dashboard |
| New MRR (this month) | New subscriptions × price |
| Churn MRR (this month) | Canceled subscriptions × price |
| Net MRR change | New MRR - Churn MRR |
| ARPU | MRR / paid users |
| Free-to-paid conversion | Paid conversions / free signups (30-day window) |

### 8.3 Engagement

| Metric | How to Measure |
|--------|---------------|
| DAU / WAU / MAU | PostHog unique users |
| Searches per user per week | PostHog event: `search` |
| Leads saved per user per week | PostHog event: `lead_saved` |
| Notes added per user per week | PostHog event: `note_added` |
| Pipeline moves per week | PostHog event: `status_changed` |

### 8.4 Retention

| Metric | How to Measure |
|--------|---------------|
| Day 1 / 7 / 30 retention | PostHog retention analysis |
| Weekly active rate (paid) | Active paid users / total paid users |
| Monthly churn rate | Cancellations / starting paid users |
| NPS score | Quarterly survey (PostHog or Typeform) |

---

## 9. Competitive Response Playbook

### 9.1 If LeadSwift Adds CRM Features

**Response:** Lean into simplicity and legal data.
- Message: "LeadSwift scrapes data. We use official APIs. Your business deserves legal, reliable data."
- Differentiate: pipeline view, notes, follow-ups — features they bolted on vs. our core design
- Speed: ship vertical-specific features (insurance, agencies) faster than they can

### 9.2 If a CRM Adds Google Places Search

**Response:** Lean into purpose-built simplicity.
- Message: "HubSpot is built for enterprises. LeadLocal is built for you."
- Differentiate: our entire UX is optimized for the search→save→close workflow
- Price: undercut by 3-5x

### 9.3 If a New Competitor Copies Us

**Response:** Accelerate on moats.
- Data moat: aggregate outreach intelligence nobody else has
- Integration moat: email, Zapier, Chrome extension increase switching cost
- Community moat: build-in-public followers become advocates
- Speed: keep shipping faster

---

## 10. 90-Day Action Plan Summary

| Week | Marketing Action | Product Milestone |
|------|-----------------|------------------|
| 1-2 | Waitlist landing page + build-in-public posts | Backend core + Google Places integration |
| 3-4 | Beta invites (20 users) + collect testimonials | Frontend + CRM features + pipeline |
| 5 | Prepare PH launch assets + email waitlist | Billing integration + launch polish |
| 6 | **LAUNCH:** Product Hunt + IH + Reddit + Twitter | Fix launch-day bugs |
| 7-8 | Direct outreach to 50 agencies + publish 2 blog posts | Ship top 3 user requests |
| 9-10 | SEO: publish 4 blog posts + guest post outreach | CSV export + multi-source search |
| 11-12 | Referral program launch + pricing experiment | Team features + email integration |

---

## 11. Document Cross-References

| Topic | Document |
|-------|----------|
| Pricing tiers and unit economics | [constitution.md](constitution.md) Section 4 |
| Technical architecture | [blueprint.md](blueprint.md) |
| API specs for billing/analytics | [artifacts.md](artifacts.md) |
| Build phases and timeline | [implementation-guide.md](implementation-guide.md) |
| Project structure | [skeleton.md](skeleton.md) |
