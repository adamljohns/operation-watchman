# Operation Watchman — 90-Day Men's Formation

A Progressive Web App (PWA) for tracking daily readings and disciplines during the 90-day Operation Watchman formation challenge.

## Features

- **Day Counter** — tracks Day X of 90 from your start date
- **5 Daily Readings** — Morning Wisdom, Husband's Post, Father's Charge, Citizen's Stand, Evening Peace
- **6 Daily Disciplines** — Cold Shower, Fasting, No Alcohol, No Screens After 9PM, Morning Prayer, Evening Prayer
- **Streak Counter** — consecutive days completed
- **Offline Support** — works without internet after first load
- **Installable** — add to home screen on mobile

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

All data is stored locally in `localStorage`:
- `ow_start_date` — the date you started the challenge
- `ow_daily_YYYY-MM-DD` — daily check state (JSON)
- `ow_streak` — cached streak count
- `ow_last_checked` — for completion toast deduplication

## Deployment

Serve from any static host (GitHub Pages, Netlify, Vercel, etc.)

---

*Stand your post. Hold the line. 90 days.*
