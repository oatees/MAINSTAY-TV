# Research: YouTube-First Weekly Top 3

**Date**: 2026-10-28
**Scope**: Resolve design choices needed to plan the minimum weekly Top 3 workflow.

## Decision: Use the existing agent workflow and local SQLite conventions

**Rationale**: The repository already describes a local content-management agent,
has an SQLite schema at `agent/init-db.sql`, and uses Playwright with manual
publishing guidance when automation is blocked. There is no product application
runtime, test runner, or YouTube integration to extend.

**Alternatives considered**:

- Add a standalone web application or service: rejected because the requested
  feature is one editor's weekly workflow and no such application exists here.
- Add a new database or replace SQLite: rejected because the existing schema is
  the established local record of posts, artists, and reports.

## Decision: Make YouTube publication browser-assisted and editor-controlled

**Rationale**: The existing publishing convention uses an authenticated browser
and falls back to a manual guide. YouTube's official upload guide describes API
upload as requiring a registered application, OAuth 2.0 authorization, and API
configuration; none is present in the repository. A human-review boundary avoids
introducing credentials, a new integration, or unattended public uploads in this
minimal feature. The editor must review the selected channel and package and
complete the final publish action. Record success only after YouTube visibly
confirms the outcome; if uncertain, leave it unresolved and reconcile before any
retry.

**Alternatives considered**:

- YouTube Data API upload: deferred because it needs a registered Google
  application, OAuth consent/credentials, and separate API-policy and operational
  decisions not included in the minimal feature scope.
- Fully unattended browser publishing: rejected because public distribution is
  consequential, account state and upload results can be ambiguous, and this
  workflow requires editor approval.

**Sources**:

- [YouTube Data API: Upload a video](https://developers.google.com/youtube/data/guides/uploading_a_video)
  documents application registration and OAuth 2.0 authorization requirements.
- Existing project workflow in `.kiro/hooks/publish-todays-posts.json` uses
  Playwright and requires a manual action when platform automation is blocked.

## Decision: Use editorial selection; do not calculate a Spotify-derived chart

**Rationale**: The feature specification requires editor-provided selections and
explicitly excludes Spotify data and content. The existing weekly report workflow
uses engagement observations from the project's own posts; it is not an input to
this feature's three-track selection.

**Alternatives considered**:

- Rank tracks using streaming-service metrics or Spotify metadata: rejected as
  outside the specification and inconsistent with the separate Spotify NO-GO
  checklist.
- Automatically derive rankings from existing post analytics: rejected because
  it changes the feature from an editorial Top 3 package to an analytics product.

**Source**: `specs/001-youtube-top-three/checklists/spotify-policy-go-no-go.md`
records the current policy boundary and the official Spotify references reviewed.

## Decision: Treat rights, editor approval, and publication status as explicit workflow state

**Rationale**: Publication must not proceed with unknown rights or without review.
The spec also requires that failed or uncertain publication not be reported as
success. Capturing approval and rights confirmation with the package makes these
gates auditable in the existing local workflow.

**Alternatives considered**:

- Rely on informal notes or assume rights from the presence of files: rejected
  because file availability does not establish publication permission.
- Mark an uncertain submission as failed and retry immediately: rejected because
  YouTube may have accepted the first submission despite an interrupted response.

## Resolved technical unknowns

- **Application type**: Existing local agent workflow, not a web or mobile app.
- **Storage**: Existing local SQLite database; no new persistence service.
- **YouTube integration**: Human-reviewed browser-assisted publishing, not a
  programmatic API integration in this release.
- **Track ranking source**: Editor selection only; no streaming analytics.
- **Testing approach**: Manual workflow acceptance checks and local record
  validation; no product test framework exists today.
