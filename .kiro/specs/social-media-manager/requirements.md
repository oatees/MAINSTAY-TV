# Social Media Manager Agent — Requirements

## Overview
An AI-powered social media curation agent for MainStay (@mainstay) that curates approved local assets and editorial inputs, frames relevant music and culture, schedules channel content, and supports cross-platform publishing across TikTok, Instagram, and WhatsApp. Artist promotion remains one programming stream, not the channel's whole identity. External YouTube or Spotify account connections are not yet implemented; recommendations must use available local assets and explicitly provided signals until those integrations are designed and authorized.

## Requirements

### 1. Content Asset Management
**1.1** The agent MUST scan `Content-data/` and build an inventory of all media assets (images, audio, video) grouped by artist.
**1.2** The agent MUST store the asset inventory in the SQLite database with metadata: filename, artist, type, file size, date added.
**1.3** The agent MUST flag assets that have already been posted to avoid duplicates within 48 hours per platform.

### 2. Content Scheduling
**2.1** The agent MUST generate a 7-day posting calendar when asked, distributing suitable available assets and approved editorial items across TikTok, Instagram, and WhatsApp.
**2.2** The schedule MUST follow platform-specific rules:
  - TikTok: video clips ≤60s unless full music video
  - Instagram: mix of Reels (video), Feed posts (images), and Stories (24h time-sensitive)
  - WhatsApp: announcements and major drops only (max 2x per week)
**2.3** The agent MUST store the schedule in the database with status: `scheduled`, `published`, `skipped`.
**2.4** The agent MUST propose optimal posting times based on SA timezone (SAST, UTC+2).

### 3. Artist and Editorial Curation — Caption & Copy Generation
**3.1** The agent MUST generate platform-specific captions for artist features and other approved MainStay editorial posts.
**3.2** Captions MUST include:
  - Hook line (first 1-2 sentences, no hashtags — keeps the algorithm happy)
  - Body copy with accurate context for the featured artist, track, story, or media
  - Call to action appropriate to the post (follow, stream, watch, share)
  - Relevant hashtags; do not force music-only tags onto non-music coverage
**3.3** The agent MUST preserve MainStay's channel voice and adapt tone per platform:
  - TikTok: short, punchy, hook-first
  - Instagram: slightly longer, storytelling-friendly
  - WhatsApp: direct announcement style, no fluff
**3.4** The agent MUST store all generated copy in the database linked to the scheduled post.

### 4. Cross-Platform Publishing Pipeline
**4.1** The agent MUST follow a defined publish order: TikTok first → Instagram Reels (same or next day) → WhatsApp announcement (drop day only).
**4.2** For each publish action the agent MUST:
  - Identify the correct asset from `Content-data/`
  - Generate or retrieve the caption
  - Use Playwright to navigate to the platform and guide/execute the upload
  - Log the result (success/fail/manual-required) in the database
**4.3** The agent MUST take a screenshot after each publish attempt as confirmation.
**4.4** Where full automation is blocked by platform restrictions, the agent MUST output a step-by-step manual publish guide with the exact caption ready to copy-paste.

### 5. Weekly Top-3 Compiler
**5.1** The agent MUST produce a Weekly Top-3 report every week summarizing the top-performing tracks/artists based on available engagement data.
**5.2** The report MUST include: artist name, track, platforms posted, estimated reach/engagement notes.
**5.3** The report MUST be saved as a markdown file in `agent/reports/week-<YYYY-WW>.md`.

### 6. Analytics & Memory
**6.1** The agent MUST log engagement observations (manually entered or fetched) against each post record.
**6.2** The agent MUST use the Memory MCP to retain knowledge about: artist profiles, what content formats performed well, audience preferences.
**6.3** The agent MUST surface insights when building the next week's schedule (e.g. "Reels outperformed feed posts last week").

### 7. Database Schema
The SQLite database at `agent/mainstay.db` MUST contain:
- `assets` table — content inventory
- `posts` table — scheduled/published post log
- `artists` table — artist profiles and campaign status
- `captions` table — generated copy linked to posts
- `analytics` table — engagement notes and observations
