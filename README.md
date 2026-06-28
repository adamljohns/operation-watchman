# Operation Watchman — 90-Day Men's Formation

A Progressive Web App (PWA) for tracking daily readings and disciplines during the 90-day Operation Watchman formation challenge.

## Features

- **Day Counter** — tracks Day X of 90 from your start date
- **5 Daily Readings** — Morning Wisdom, Husband's Post, Father's Charge, Citizen's Stand, Evening Peace, each a full 90-day curated scripture arc
- **6 Daily Disciplines** — Cold Shower, Fasting, No Alcohol, No Screens After 9PM, Morning Prayer, Evening Prayer
- **Nightly Reflection** — a daily examination prompt, authored in 13 weekly blocks themed to that week's LBCF 1689 confession anchor
- **Weekly Confession Anchor** — a chapter of the 1689 Baptist Confession each week (13 chapters across the 90 days)
- **Anchor Prayer** — name the one petition you carry across all 90 days; it sits atop the journal every night
- **Streak Counter** — consecutive days, with one weekly *grace day* so a single miss doesn't zero a long run (liberty, not license — LBCF 21)
- **Lord's Day** — Sundays are marked for corporate worship, family worship, and rest
- **Onboarding & Graduation** — a Day 0 covenant (means of grace, not merit) and a Day 91 debrief with stats and journal export
- **Journal** — per-day entries, autosaved, exportable to Markdown
- **Multiple Plans** — switch between Operation Watchman (90) and Proverbs in 31
- **Offline Support** — works without internet after first load
- **Installable** — add to home screen on mobile

## Curriculum

The 90-day plan content lives in `content/plans/watchman-90.json` and is **generated**, not hand-edited. Edit the curated arrays in `scripts/build-watchman-90.js` and re-run:

```
node scripts/build-watchman-90.js
```

Days 1–7 reproduce the original hand-authored sample week; each reading track is a curated arc of ~45 passages that re-reads its cornerstone texts across the 90 days.

## Tech

- Vanilla HTML/CSS/JS (no framework)
- localStorage for all data persistence
- Service Worker for offline caching
- Web App Manifest for installability
- Dark theme with gold accents matching usmcmin.org

## Colors

- Background: `#000000` / `#0a0a0a`
- Gold Accent: `#D4AF37`
- Font: Playfair Display (headers), Open Sans (body)

## Data Storage

All data is stored locally in `localStorage`, namespaced per plan as
`ow_plan_<planId>_*`:
- `ow_plan_<id>_start_date` — the date you started the plan
- `ow_plan_<id>_daily_YYYY-MM-DD` — daily check state (JSON)
- `ow_plan_<id>_journal_YYYY-MM-DD` — journal entry text
- `ow_plan_<id>_anchor` — your anchor prayer
- `ow_plan_<id>_best_streak` — best streak reached (graduation stat)
- `ow_plan_<id>_last_checked` — for completion toast deduplication
- `ow_active_plan` — currently selected plan id
- `ow_onboarded_v05` — one-time onboarding flag

Legacy unprefixed keys (v0.1–v0.3) are migrated into the `watchman-90`
namespace on first load and left in place for rollback safety.

## Deployment

Serve from any static host (GitHub Pages, Netlify, Vercel, etc.)

---

*Stand your post. Hold the line. 90 days.*
