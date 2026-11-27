-- MainStay — channel database
-- Run: sqlite3 agent/mainstay.db < agent/init-db.sql
--
-- This schema is the channel's operating system: assets, posts, captions,
-- analytics, and the weekly music Top-3. The channel keeps its name
-- (@mainstay); its editorial concept can broaden without changing this
-- schema. Artist roster/content are tracked separately in seed data and
-- Content-data/.

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ─────────────────────────────────────────
-- ARTISTS (roster the channel currently presents)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS artists (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  name              TEXT NOT NULL,
  genre             TEXT,
  instagram_handle  TEXT,
  tiktok_handle     TEXT,
  active_campaign   BOOLEAN DEFAULT 1,
  notes             TEXT,
  created_at         DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- ASSETS (content inventory)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS assets (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  artist_id          INTEGER REFERENCES artists(id),
  filename           TEXT NOT NULL,
  filepath           TEXT NOT NULL UNIQUE,
  asset_type         TEXT CHECK(asset_type IN ('image','video','audio')),
  duration_seconds   INTEGER,
  file_size_kb       INTEGER,
  track_name         TEXT,
  posted_tiktok      BOOLEAN DEFAULT 0,
  posted_instagram   BOOLEAN DEFAULT 0,
  posted_whatsapp    BOOLEAN DEFAULT 0,
  last_posted_at     DATETIME,
  created_at         DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- POSTS (scheduled + published log)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS posts (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  asset_id        INTEGER REFERENCES assets(id),
  artist_id       INTEGER REFERENCES artists(id),
  platform        TEXT CHECK(platform IN (
                    'tiktok',
                    'instagram_reel',
                    'instagram_story',
                    'instagram_feed',
                    'whatsapp'
                  )),
  post_type       TEXT CHECK(post_type IN (
                    'promo','announcement','top3',
                    'story','reel','video','image'
                  )),
  scheduled_date  DATE,
  scheduled_time  TIME,
  status          TEXT CHECK(status IN (
                    'scheduled','published',
                    'skipped','failed','manual-required'
                  )) DEFAULT 'scheduled',
  published_at    DATETIME,
  screenshot_path TEXT,
  notes           TEXT,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- CAPTIONS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS captions (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id       INTEGER REFERENCES posts(id),
  platform      TEXT,
  hook_line     TEXT,
  body_copy     TEXT,
  call_to_action TEXT,
  hashtags      TEXT,
  full_caption  TEXT,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- ANALYTICS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS analytics (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id           INTEGER REFERENCES posts(id),
  platform          TEXT,
  views             INTEGER DEFAULT 0,
  likes             INTEGER DEFAULT 0,
  shares            INTEGER DEFAULT 0,
  comments          INTEGER DEFAULT 0,
  follows_gained    INTEGER DEFAULT 0,
  observation_notes TEXT,
  recorded_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- WEEKLY REPORTS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_reports (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  week_label   TEXT NOT NULL,
  top1_artist  TEXT,
  top2_artist  TEXT,
  top3_artist  TEXT,
  report_path  TEXT,
  generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- SEED DATA — roster the channel currently presents
--─────────────────────────────────────────
INSERT OR IGNORE INTO artists (id, name, genre, instagram_handle, tiktok_handle, notes) VALUES
(1, 'Delah Dube',  'R&B / Soul',      '@delahdube',  '@delahdube',
   'Track: Songbird (Interlude). Singer-songwriter from SA.'),
(2, 'GOLIDE',      'Hip-Hop / Street', '@golide_sa',  '@golide_sa',
   'Track: They Talk ft. Just Sam, Dukii, Lawkiid, Mbatha. Vaal-based.');

-- Useful views
CREATE VIEW IF NOT EXISTS unposted_assets AS
SELECT a.*, ar.name as artist_name
FROM assets a
JOIN artists ar ON a.artist_id = ar.id
WHERE a.posted_tiktok = 0
   OR a.posted_instagram = 0
   OR a.posted_whatsapp = 0;

CREATE VIEW IF NOT EXISTS this_week_schedule AS
SELECT p.*, c.full_caption, a.filename, ar.name as artist_name
FROM posts p
LEFT JOIN captions c ON c.post_id = p.id
LEFT JOIN assets a ON a.id = p.asset_id
LEFT JOIN artists ar ON ar.id = p.artist_id
WHERE p.scheduled_date BETWEEN date('now','weekday 0','-6 days') AND date('now','weekday 0');

-- ─────────────────────────────────────────
-- WEEKLY TOP 3 (YouTube-only feature)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_top3_packages (
  id                TEXT PRIMARY KEY CHECK(length(trim(id)) > 0),
  week_label        TEXT NOT NULL UNIQUE,
  video_ref         TEXT,
  title             TEXT,
  description       TEXT,
  thumbnail_ref     TEXT,
  status            TEXT NOT NULL DEFAULT 'draft' CHECK(status IN (
                      'draft','review','approved','publishing',
                      'published','rejected','unresolved'
                    )),
  approved_by       TEXT,
  approved_at       DATETIME,
  created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weekly_top3_tracks (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  package_id          TEXT NOT NULL REFERENCES weekly_top3_packages(id) ON DELETE CASCADE,
  position            INTEGER NOT NULL CHECK(position IN (1,2,3)),
  track_title         TEXT NOT NULL,
  artist_name         TEXT NOT NULL,
  editorial_source    TEXT NOT NULL,
  rights_confirmed_by TEXT,
  rights_confirmed_at DATETIME,
  UNIQUE(package_id, position),
  UNIQUE(package_id, track_title, artist_name)
);

CREATE TABLE IF NOT EXISTS weekly_top3_clearances (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  package_id     TEXT NOT NULL REFERENCES weekly_top3_packages(id) ON DELETE CASCADE,
  media_ref      TEXT NOT NULL,
  rights_status  TEXT NOT NULL DEFAULT 'pending' CHECK(rights_status IN ('pending','confirmed')),
  confirmed_by   TEXT,
  confirmed_at   DATETIME,
  UNIQUE(package_id, media_ref),
  CHECK (
    (rights_status = 'confirmed' AND confirmed_by IS NOT NULL AND confirmed_at IS NOT NULL)
    OR (rights_status = 'pending')
  )
);

CREATE TABLE IF NOT EXISTS youtube_publication_attempts (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  package_id        TEXT NOT NULL REFERENCES weekly_top3_packages(id) ON DELETE CASCADE,
  channel_identity  TEXT NOT NULL,
  status            TEXT NOT NULL DEFAULT 'pending' CHECK(status IN (
                      'pending','published','rejected','unresolved'
                    )),
  youtube_video_ref  TEXT,
  attempted_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  confirmed_at      DATETIME,
  outcome_note      TEXT,
  CHECK (status <> 'published' OR youtube_video_ref IS NOT NULL),
  CHECK (
    (status IN ('rejected','unresolved') AND outcome_note IS NOT NULL)
    OR (status IN ('pending','published'))
  )
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_one_published_per_package
  ON youtube_publication_attempts(package_id)
  WHERE status = 'published';
