# Implementation Plan: YouTube-First Weekly Top 3

**Branch**: `001-youtube-top-three` | **Date**: 2026-10-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-youtube-top-three/spec.md`

## Summary

Add a minimal, editor-controlled weekly Top 3 workflow to the existing MainStay TV
agent. The editor supplies three ordered tracks and rights confirmations, reviews
one YouTube video package, and explicitly approves publishing. Reuse the repository's
existing SQLite recordkeeping and Playwright/manual publishing conventions. Spotify
data and content are excluded. The initial workflow will be browser-assisted with a
human completing the final YouTube publication action; it will not add YouTube API
credentials or unattended public publishing.

## Technical Context

**Language/Version**: No product runtime or implementation language is established;
the existing project consists of agent instructions, JSON workflow configuration,
and a SQLite schema.

**Primary Dependencies**: Existing agent workflow, Playwright browser interaction,
and SQLite database conventions. No new runtime dependency is planned.

**Storage**: Existing SQLite database at `agent/mainstay.db`; update its schema
definition in `agent/init-db.sql` if implementation requires persistent package
records.

**Testing**: Manual acceptance scenarios and database validation; the repository
currently has no product test runner or automated test suite.

**Target Platform**: MainStay TV's local agent workflow and its authenticated
YouTube channel in a desktop browser.

**Project Type**: Agent-driven content workflow; not an existing web application
or standalone service.

**Performance Goals**: One review-ready package for a week; editor preparation
should take no more than ten minutes for at least four of five representative
editors, as specified by SC-002.

**Constraints**: Exactly three editor-selected tracks; rights confirmation and
explicit review before publish; YouTube only; Spotify-free; do not claim success
without publication confirmation; no unattended public publishing in the initial
workflow.

**Scale/Scope**: One package and one YouTube video per week, one editor, and the
existing local agent/database workflow.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Pre-research**: The repository's constitution file is still the unfilled
  template. It defines no project-specific principles or gates to evaluate. No
  conflicts can be identified, but formal constitutional compliance cannot be
  certified until the constitution is completed.
- **Scope and safety**: The plan follows the spec's YouTube-only scope, requires
  editor rights confirmation and approval, and excludes Spotify access and content.
  No unjustified scope expansion or known policy conflict is introduced.
- **Gate result**: Proceed with planning; constitution compliance remains
  unverified because the governing principles are not yet defined. Resolve the
  constitution before implementation if project governance requires a formal pass.

## Project Structure

### Documentation (this feature)

```text
specs/001-youtube-top-three/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── youtube-publishing.md
└── tasks.md              # Phase 2 output (/speckit-tasks); not created here
```

### Existing project surfaces

```text
agent/
├── README.md              # Agent workflow and supported platforms
├── init-db.sql            # SQLite schema and seed data
├── reports/
├── schedules/
└── screenshots/
.kiro/
├── hooks/                 # Existing agent-triggered workflows
└── steering/              # Agent behavior and platform constraints
Content-data/              # Existing media assets; do not move assets
```

**Structure Decision**: Keep this feature in the existing local agent workflow,
SQLite schema, and agent guidance surfaces. Do not introduce a web application,
service, or a new source-code project. Add no contract for a programmatic YouTube
API; the publishing boundary is a human-reviewed browser workflow described in
`contracts/youtube-publishing.md`.

## Constitution Check (Post-Design)

- The design introduces no new services, external data sources, or non-YouTube
  destinations.
- The package model enforces the three-track limit and captures rights and approval
  before publication.
- The publishing contract leaves final submission with the editor and distinguishes
  confirmed publication from rejected or unresolved outcomes.
- The Spotify NO-GO boundary remains explicit and independently documented.
- **Gate result**: No new conflict identified. Formal constitution compliance
  remains unverified because `.specify/memory/constitution.md` is an unfilled
  template.

## Complexity Tracking

No constitution violations are being accepted. No additional application, service,
or abstraction is proposed.
