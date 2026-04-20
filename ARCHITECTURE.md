# Operation Watchman — Architecture & Roadmap

> Stand your post. Hold the line. 90 days.

This doc sketches the path from the current single-file PWA to a full
protestant-framed 90-day formation app in the spirit of (and competing with)
Exodus 90.

Written in a session where only this repo was reachable — the main website
(`usmcmin.org` / `usmcmin.com`), the blog, the Proverbs reading plan, and
Pops's Boaz formation guide were not available. Treat curriculum specifics
here as placeholders to be replaced with real content once those sources are
in reach.

---

## 1. Vision

**Operation Watchman** is a 90-day formation app for Protestant men. It is
scripture-centered, explicitly Reformed-compatible (no apocrypha, no
Mariology, no sacramental assumptions), and built around four pillars:

| Pillar       | What it is                                                   |
| ------------ | ------------------------------------------------------------ |
| Word         | Daily scripture reading across five tracks                   |
| Discipline   | Daily ascetic + spiritual practices (cold, fast, prayer, …)  |
| Fraternity   | Accountability groups of 4–10 men checking in daily          |
| Reflection   | A written examination each evening, private or shared        |

The voice is watchman / post / line. Masculine, disciplined, grave.
Never cringe, never bro-y, never soft.

---

## 2. Existing shape (v0.1)

What's here today:

- Single `index.html` with styles + vanilla JS inline
- `sw.js` service worker, cache-first
- `manifest.json` PWA manifest
- `icons/` 192 + 512
- All state in `localStorage`:
  - `ow_start_date`
  - `ow_daily_YYYY-MM-DD` — JSON of checked items for a date
  - `ow_streak` — cached streak count (currently recomputed every render)
  - `ow_last_checked` — dedupe key for completion toast
- 5 readings × 6 disciplines = 11 daily items
- Reading keys: `morning_wisdom`, `husbands_post`, `fathers_charge`,
  `citizens_stand`, `evening_peace`
- Discipline keys: `cold_shower`, `fasting`, `no_alcohol`, `no_screens`,
  `prayer_morning`, `prayer_evening`

Limits to address:

- Zero content — the five readings are labels, not actual scripture plans
- No journaling, reflection, or text capture
- No cross-device sync, no account
- No fraternity / accountability mechanism
- Streak logic walks up to 90 prior days of localStorage on every render

---

## 3. Product phases

### v0.2 — Content layer (this week, doable offline-only)

Goal: the app becomes data-driven. The five readings show today's actual
scripture reference, pulled from a JSON plan file in the repo.

- Add `content/plans/watchman-90.json` with a day-by-day curriculum
- Morning Wisdom = Proverbs cycled 3× (31 + 31 + 28 days) — Billy Graham's
  classic protestant rhythm
- Other four readings: stubs for days 1–7, placeholders for 8–90 (to be
  filled from the real Proverbs plan and Boaz guide)
- `index.html` fetches the plan at load, shows today's ref under each item
- Backwards-compatible: if `plan.json` fails to load, UI falls back to the
  current theme labels

### v0.3 — Reflection & journaling

- Tap any completed day → opens an evening reflection pane
- Free-text journal stored in `localStorage` under `ow_journal_YYYY-MM-DD`
- Suggested prompts per day (pulled from plan)
- Export to `.md` file for backup before there's a real backend
- Swipe between days, read-only for past days

### v0.4 — Multiple formation tracks

- Generalize plan loader to support N tracks
- Ship:
  - **Watchman** (current 90-day)
  - **Boaz** (husband/father formation — Pops's guide, when available)
  - **Proverbs-31** (31-day cycle, standalone)
- Track selection on first launch; user can run multiple in parallel
- Progress per-track, independent start dates

### v1.0 — Backend & sync

First time we leave the browser. Goals: cross-device, survives cache wipe,
prepares for fraternity.

- **Auth**: Supabase Auth (email + Apple/Google OAuth)
- **DB**: Supabase Postgres
- **Hosting**: Cloudflare Pages (static) + Supabase (managed backend)
- **Sync strategy**: localStorage remains source of truth while offline;
  on reconnect, push deltas and pull remote changes. Last-write-wins per
  `(user, day, field)` is fine for this domain — no concurrent editors.
- **Push**: Web Push via service worker for morning reminder + evening
  examination. Native iOS/Android wrap later if needed.

### v1.1 — Fraternity

The Exodus 90 killer feature. Without this we're a habit tracker.

- Groups of 4–10, invite by code or link
- Daily check-in: each member sees who completed today, who broke the fast
- Weekly *examination of conscience* — longer written reflection visible
  to the group (opt-in per reflection)
- In-app chat thread per group (simple, no moderation features v1)
- Admin role per group: can remove members, renew 90-day cycle

### v2.0 — Content platform

- Subscription tier for premium tracks (keep a free core)
- Audio readings (narrated scripture + commentary)
- Pastor/teacher-led cohorts (named 90-day runs led by a real person)
- Web Share Target for journaling from system share sheet
- Native wrappers if needed (Capacitor is the low-friction path for PWA → native)

---

## 4. Data model

### Content (versioned in git)

```
Plan
├── id: "watchman-90"
├── name, description, duration_days
├── readings[]: { key, title, theme }
├── disciplines[]: { key, title, theme }
└── days[]
    ├── day: 1..N
    ├── reflection_prompt: string
    └── readings: { [reading_key]: { ref, note } | null }
```

### Runtime (per-user, synced to Postgres in v1.0)

```
user(id, email, created_at)
user_plan(user_id, plan_id, start_date, status)        -- active | complete | abandoned
user_day(user_id, plan_id, day, items_completed[],      -- array of keys
         reflection_text, reflection_shared, updated_at)
group(id, name, created_by, created_at)
group_member(group_id, user_id, role, joined_at)       -- admin | member
group_post(group_id, user_id, body, created_at)
```

Index hot paths: `user_day` by `(user_id, plan_id, day)`,
`group_post` by `(group_id, created_at DESC)`.

### localStorage keys (current + proposed)

| Key                         | Purpose                                    | Status    |
| --------------------------- | ------------------------------------------ | --------- |
| `ow_start_date`             | ISO date user started                      | existing  |
| `ow_daily_YYYY-MM-DD`       | JSON of checked items for a date           | existing  |
| `ow_streak`                 | Cached streak count                        | existing  |
| `ow_last_checked`           | Dedupe for completion toast                | existing  |
| `ow_plan_id`                | Selected plan (multi-track in v0.4)        | new       |
| `ow_journal_YYYY-MM-DD`     | Free-text reflection per day               | v0.3      |
| `ow_sync_cursor`            | Last sync timestamp                         | v1.0      |

---

## 5. Tech choices

| Layer       | Pick                      | Why                                              |
| ----------- | ------------------------- | ------------------------------------------------ |
| Frontend    | Vanilla JS → Preact       | Keep the no-build simplicity as long as possible. When journaling + multi-track makes inline HTML unwieldy, Preact w/ HTM lets us stay build-light. |
| Styling     | Inline CSS custom props   | Theme already in `:root` vars. No framework needed. |
| Storage     | localStorage → Supabase   | Zero backend until v1.0, then Postgres via Supabase. |
| Auth        | Supabase Auth             | Free tier, OAuth built-in, row-level security covers per-user isolation. |
| Hosting     | Cloudflare Pages          | Free, global edge, GitHub integration, simple. |
| Offline     | Existing service worker   | Already cache-first; extend for plan.json versioning. |
| Push        | Web Push + VAPID          | No native wrapper required. |
| Native      | Capacitor (when/if)       | Reuse the PWA 1:1, publish to App Store. |

Deliberate non-choices:

- No React/Next.js. The bundle and build cost aren't earned here yet.
- No Firebase. Supabase gives us Postgres (relational data fits this domain).
- No custom server. Supabase edge functions are enough for any server-side
  needs (invite codes, scheduled reminders).

---

## 6. Competing with Exodus 90

Where E90 is strong:

- Daily rhythm + asceticism is core to the experience
- Fraternity built into the product, not bolted on
- Brand and voice are disciplined, not self-help

Where a Protestant alternative wins:

- **Scripture-first curriculum** — E90 leans on Catholic devotional sources;
  we lean on the protestant canon and reformed catechisms (Heidelberg,
  Westminster Shorter)
- **No magisterial assumptions** — confession becomes examination, mass
  becomes Sunday worship at your local church, rosary becomes Psalter
- **Flexible fraternity** — E90 ties you to a cohort start date; we support
  both cohort and rolling starts
- **Open content** — plans versioned in git, forkable, so local churches can
  publish their own tracks

Where we must not lose:

- **Grave, serious voice.** No gamification, no confetti, no streaks-as-dopamine
  framing. The streak is a witness, not a reward.
- **No vanity metrics** outside the fraternity. Public leaderboards are
  antithetical to the formation.

---

## 7. Immediate next steps

See the companion v0.2 scaffolding in this PR:

- `content/plans/watchman-90.json` — plan manifest with days array
- `index.html` — loads plan, shows today's ref per reading
- Graceful fallback to current theme labels when plan can't load

After Saturday (when the real content is reachable):

1. Replace placeholder reading refs in `watchman-90.json` with the actual
   curriculum from the website + Boaz guide
2. Add `content/plans/boaz.json` for the husband/father track
3. Draft v0.3 journaling UI in a separate branch
