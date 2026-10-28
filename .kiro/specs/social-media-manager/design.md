# MainStay Curation Agent — Design

MainStay (@mainstay) is an entertainment and culture curation channel. Music
and artist promotion are part of its programming, not the whole concept. This
design describes the existing social publishing workflow; no YouTube/Spotify
account connection or listening-history ingestion is implemented here.

## Architecture Overview

```
MainStay Curation Agent
│
├── MCP Servers (tools layer)
│   ├── filesystem    → read Content-data/, write reports
│   ├── playwright    → browser automation for publishing
│   ├── fetch         → pull trending data, platform metadata
│   ├── memory        → persistent artist/campaign knowledge
│   └── sqlite        → structured post/schedule/analytics data
│
├── Agent Core (Kiro agent with steering)
│   ├── Asset Scanner       → indexes Content-data/
│   ├── Scheduler           → builds weekly calendar
│   ├── Caption Generator   → per-platform copy
│   ├── Publisher           → Playwright-driven or manual guide
│   ├── Top-3 Compiler      → weekly music feature and report generator
│   └── Analytics Logger    → engagement tracking
│
└── Output
    ├── agent/mainstay.db          → SQLite database
    ├── agent/reports/             → weekly markdown reports
    ├── agent/schedules/           → weekly calendar exports
    └── agent/screenshots/         → publish confirmation shots
```

## Database Schema

```sql
-- Artist profiles
CREATE TABLE artists (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  genre TEXT,
  instagram_handle TEXT,
  tiktok_handle TEXT,
  active_campaign BOOLEAN DEFAULT 1,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Content asset inventory
CREATE TABLE assets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artist_id INTEGER REFERENCES artists(id),
  filename TEXT NOT NULL,
  filepath TEXT NOT NULL,
  asset_type TEXT CHECK(asset_type IN ('image','video','audio')),
  duration_seconds INTEGER,
  file_size_kb INTEGER,
  track_name TEXT,
  posted_tiktok BOOLEAN DEFAULT 0,
  posted_instagram BOOLEAN DEFAULT 0,
  posted_whatsapp BOOLEAN DEFAULT 0,
  last_posted_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Scheduled and published posts
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  asset_id INTEGER REFERENCES assets(id),
  artist_id INTEGER REFERENCES artists(id),
  platform TEXT CHECK(platform IN ('tiktok','instagram_reel','instagram_story','instagram_feed','whatsapp')),
  post_type TEXT CHECK(post_type IN ('promo','announcement','top3','story','reel','video')),
  scheduled_date DATE,
  scheduled_time TIME,
  status TEXT CHECK(status IN ('scheduled','published','skipped','failed','manual-required')) DEFAULT 'scheduled',
  published_at DATETIME,
  screenshot_path TEXT,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Generated captions and copy
CREATE TABLE captions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER REFERENCES posts(id),
  platform TEXT,
  hook_line TEXT,
  body_copy TEXT,
  call_to_action TEXT,
  hashtags TEXT,
  full_caption TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Analytics and engagement observations
CREATE TABLE analytics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER REFERENCES posts(id),
  platform TEXT,
  views INTEGER,
  likes INTEGER,
  shares INTEGER,
  comments INTEGER,
  follows_gained INTEGER,
  observation_notes TEXT,
  recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Weekly reports log
CREATE TABLE weekly_reports (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  week_label TEXT NOT NULL,
  top1_artist TEXT,
  top2_artist TEXT,
  top3_artist TEXT,
  report_path TEXT,
  generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Publishing Pipeline Flow

```
1. SCAN
   └── Read Content-data/ via filesystem MCP
   └── Upsert asset records into SQLite

2. SCHEDULE
   └── Query unposted assets per artist
   └── Build 7-day calendar (Mon–Sun)
   └── Insert post records with status='scheduled'
   └── Export calendar to agent/schedules/week-<YYYY-WW>.md

3. CAPTION
   └── For each scheduled post → generate caption
   └── Adapt tone per platform rules
   └── Insert into captions table

4. PUBLISH
   └── For each post due today:
       a. Retrieve asset path + caption
       b. Attempt Playwright automation
       c. On success: update status='published', save screenshot
       d. On block: output manual guide + copy-paste caption

5. LOG
   └── Record analytics observations
   └── Update memory with what worked

6. REPORT
   └── Every Sunday: compile Top-3 report
   └── Save to agent/reports/week-<YYYY-WW>.md
```

## Platform-Specific Publishing Notes

### TikTok
- Navigate to tiktok.com/upload
- Upload video (≤60s for clips, full length for music videos)
- Paste caption (hook first, hashtags at end)
- Set to public, add sound if needed

### Instagram
- Use instagram.com via browser
- Reels: upload video → caption → hashtags → share
- Stories: upload image/video → add text overlay → 24h
- Feed: upload image → caption → tag artist

### WhatsApp Channel
- Navigate to web.whatsapp.com → MainStay channel
- Broadcast format: announcement text + media attachment
- Max 2x per week — reserve for meaningful drops or selected editorial updates

## Weekly Schedule Template

This is a starting cadence, not a music-only mandate. Choose suitable
available media and approved editorial items; keep the Top-3 as a weekly
music feature within broader culture programming.

| Day | Platform | Content Type | Editorial Item |
|-----|----------|-------------|--------|
| Monday | Instagram Feed | Promo image | Rotating |
| Tuesday | TikTok | Music video clip | Rotating |
| Wednesday | Instagram Story | Behind-the-scenes / teaser | Rotating |
| Thursday | TikTok | Full video or street mix | Rotating |
| Friday | Instagram Reel | New drop highlight | Rotating |
| Friday | WhatsApp | Drop announcement | Rotating |
| Sunday | Instagram Feed | Weekly Top-3 graphic | MainStay |

## Caption Formula

```
[HOOK — 1 sentence, no hashtags]

[BODY — 2-3 sentences: accurate context for the artist, track, story, or moment]

[CTA — follow/stream/share instruction]

[HASHTAGS — relevant artist/topic tags + suitable MainStay and South African culture tags; do not force music hashtags onto non-music coverage]
```
