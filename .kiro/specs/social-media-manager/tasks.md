# Social Media Manager Agent — Implementation Tasks

## Phase 1: Foundation

- [ ] 1. Initialize the agent directory structure
  - Create `agent/`, `agent/reports/`, `agent/schedules/`, `agent/screenshots/` folders
  - Create `agent/README.md` documenting how to use the agent

- [ ] 2. Initialize the SQLite database
  - Create `agent/mainstay.db`
  - Run all CREATE TABLE statements from the design doc
  - Seed the `artists` table with Delah Dube and GOLIDE

- [ ] 3. Build the asset scanner
  - Scan `Content-data/delah/` and `Content-data/GOLIDE/`
  - Classify each file as image/video/audio by extension
  - Detect video duration where possible
  - Insert all assets into the `assets` table
  - Print a summary: "Found X images, Y videos, Z audio files for N artists"

## Phase 2: Scheduling & Copy

- [ ] 4. Build the weekly schedule generator
  - Accept a start date (default: next Monday)
  - Query available unposted assets per artist
  - Apply the weekly template from the design doc
  - Insert post records into the `posts` table
  - Export the schedule as `agent/schedules/week-<YYYY-WW>.md`

- [ ] 5. Build the caption generator
  - For each scheduled post, generate platform-specific caption using the formula
  - Adapt tone: TikTok (punchy), Instagram (storytelling), WhatsApp (announcement)
  - Insert into `captions` table linked to post
  - Output a preview of all captions for the week

- [ ] 6. Generate the first week's full campaign
  - Run steps 4 + 5 together for week of June 30, 2026
  - Include both GOLIDE and Delah Dube
  - Output the full calendar with captions ready to use

## Phase 3: Publishing

- [ ] 7. Build the Playwright publish flow for TikTok
  - Navigate to tiktok.com/upload
  - Attach video file, paste caption
  - Log result, save screenshot to `agent/screenshots/`
  - Update post status in database

- [ ] 8. Build the Playwright publish flow for Instagram
  - Handle Reels, Feed posts, and Stories separately
  - Navigate instagram.com, upload media, paste caption
  - Log result, save screenshot
  - Update post status in database

- [ ] 9. Build the WhatsApp broadcast flow
  - Navigate web.whatsapp.com → MainStayTV channel
  - Compose announcement message + attach media
  - Log result, save screenshot
  - Update post status in database

- [ ] 10. Build the manual publish fallback
  - When automation is blocked, output a formatted guide:
    - Step-by-step instructions
    - Caption pre-formatted for copy-paste
    - Asset path to use
    - Screenshot of where to click

## Phase 4: Analytics & Reporting

- [ ] 11. Build the analytics logger
  - Accept manual input: views, likes, shares, comments, follows
  - Link to post record in database
  - Update memory MCP with what content type performed well

- [ ] 12. Build the Weekly Top-3 compiler
  - Query analytics table for the past 7 days
  - Rank artists/tracks by engagement score (views + likes + shares)
  - Generate `agent/reports/week-<YYYY-WW>.md` with Top-3 summary
  - Insert record into `weekly_reports` table

## Phase 5: Automation Hooks

- [ ] 13. Create a `fileCreated` hook
  - Trigger when a new file lands in `Content-data/`
  - Auto-run asset scanner and notify agent to update inventory

- [ ] 14. Create a `userTriggered` hook — "Publish Today's Posts"
  - Run the publisher for all posts scheduled for today
  - Output results summary

- [ ] 15. Create a `userTriggered` hook — "Generate This Week's Schedule"
  - Run schedule generator + caption generator for the current week
  - Output the full calendar preview
