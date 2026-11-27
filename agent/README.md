# MainStay — channel operating system

MainStay keeps `@mainstay` alive across surfaces. It is an entertainment and
culture curation channel, not a music channel with a manager attached. Music
is part of the programming, while the editorial identity can also cover other
stories, media, and moments that fit MainStay's point of view.

## What it is now
- One account, several surfaces: TikTok, Instagram, WhatsApp.
- One voice across those surfaces — captions read like the channel, not like
  a template with a handle pasted in.
- One weekly music ritual: the Top-3, an editorial pick of the tracks and
  artists that mattered this week.
- A roster it currently presents (Delah Dube, GOLIDE) and the content folders
  that belong to those artists. The roster lives under the channel, not the
  other way around; music promotion is a programming stream, not the whole
  concept.

## What it is not
- Not a personal artist page. The channel is the brand; the artists are
  programmed, not the homepage.
- Not a one-off posting script. The doc, the DB seed, and the operating rules
  are meant to outlast any single week's content.

## Structure
```
agent/
├── mainstay.db          → SQLite database (posts, assets, captions, analytics)
├── init-db.sql          → Database schema (run once to initialize)
├── reports/             → Weekly Top-3 markdown reports
├── schedules/           → Weekly posting calendar exports
└── screenshots/         → Publish confirmation screenshots
```

## Quick Start

### 1. Initialize the database
```cmd
sqlite3 agent/mainstay.db < agent/init-db.sql
```
If you don't have sqlite3 installed: https://sqlite.org/download.html

### 2. Ask the agent to scan content
> "Scan Content-data and build the asset inventory"

### 3. Generate this week's schedule
> "Generate the posting schedule for this week with captions"

### 4. Publish today's posts
> "Publish today's scheduled posts"

### 5. Get the weekly report
> "Compile the weekly Top-3 report"

## Weekly YouTube Top 3 (YouTube-only)

MainStay also runs a weekly Top 3 music feature that publishes one video to
YouTube only. The workflow is user-triggered via
`.kiro/hooks/weekly-youtube-top3.json` and uses the existing SQLite schema
(`weekly_top3_packages`, `weekly_top3_tracks`, `weekly_top3_clearances`,
`youtube_publication_attempts`).

Requirements:
- Exactly three distinct, ordered, editor-selected tracks with non-Spotify
  editorial sources.
- A finished video, title, description, and thumbnail, plus confirmed
  publication rights for all included media.
- Explicit editor approval before submission.
- The editor completes the final YouTube publish action (browser-assisted;
  no YouTube API or unattended public publishing).
- `published` is recorded only after YouTube visibly confirms and returns a
  video reference.
- Rejected or uncertain submissions are recorded as `rejected` or `unresolved`
  and are reconciled against the channel before any retry.
- No Spotify Platform data or Spotify Content is used.

## Platforms

| Platform | Handle |
|----------|--------|
| TikTok | @mainstay |
| Instagram | @mainstay |
| WhatsApp | MainStay channel |

Automation for each surface is Playwright (browser) when a surface allows it;
when a surface blocks automation, the agent outputs a manual guide with a
copy-paste caption instead of pretending it posted.

## Brand & voice
`@mainstay` is one identity across surfaces. The name stays; the voice is the
channel speaking as the channel. The concept can broaden without changing the
handle, artist records, or database schema. If the actual social handles ever
change, update this platform table; artist handles in the DB are separate.

## Roster
The current roster is seed data in `agent/init-db.sql` and content folders
under `Content-data/`. Each artist keeps their own folder of media. The agent
never moves assets out of `Content-data/`. The roster can grow or change as
MainStay's editorial coverage broadens.

## Operating rules
- All media assets live in `Content-data/` — never move them
- The channel will not post the same content to the same surface within 48 hours
- WhatsApp is broadcast-only — max 2 posts per week
- If a surface blocks automation, the agent outputs a manual guide with a
  copy-paste caption
- The weekly Top-3 is the channel's signature music feature within its broader editorial mix, not an afterthought

## Notes
- If the roster changes, update `Content-data/` folders and `init-db.sql` seed
  together; the channel name and handles are separate from the roster
- The DB schema, posts, captions, and analytics carry the surface and the
  asset — not the channel name directly — so most of the machine survives a
  roster or concept change intact
