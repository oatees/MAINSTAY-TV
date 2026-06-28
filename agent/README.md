# MainStay TV — Social Media Manager Agent

This folder is the agent's working directory.

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

## Platforms

| Platform | Handle | Automation |
|----------|--------|-----------|
| TikTok | @mainstaytv | Playwright (browser) |
| Instagram | @mainstaytv | Playwright (browser) |
| WhatsApp | MainStayTV channel | Playwright (browser) |

## Notes
- All media assets live in `Content-data/` — never move them
- The agent will never post the same content to the same platform within 48 hours
- WhatsApp is broadcast-only — max 2 posts per week
- If a platform blocks automation, the agent outputs a manual guide with copy-paste caption
