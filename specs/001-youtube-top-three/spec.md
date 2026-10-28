# Feature Specification: YouTube-First Weekly Top 3

**Feature Branch**: `Not created (no branch hook configured)`

**Created**: 2026-10-28

**Status**: Draft

**Input**: User description: "turn the recommendation into a concrete, minimal YouTube-first feature spec and map the Spotify policy boundary into a separate go/no-go checklist before any implementation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Prepare and publish the weekly Top 3 (Priority: P1)

A MainStay TV editor selects three tracks for the week, confirms that the materials
are cleared for publication, prepares a video package, reviews it, and publishes one
video to YouTube. YouTube is the only destination in this first release.

**Why this priority**: It delivers the channel's weekly music feature on its primary
destination without expanding into cross-posting or unapproved Spotify use.

**Independent Test**: An editor can create a package from three editor-selected
tracks, review the package, and publish one approved video to YouTube.

**Acceptance Scenarios**:

1. **Given** an editor has entered exactly three ordered tracks and selected
   publication-cleared media, **When** the editor prepares the weekly package,
   **Then** the package contains those three tracks in that order and a YouTube
   video, title, description, and thumbnail for review.
2. **Given** any track or media item lacks confirmed publication rights, **When**
   the editor attempts to approve or publish the package, **Then** publication is
   blocked and the missing clearance is identified.
3. **Given** a complete package has confirmed rights and editor approval,
   **When** the editor publishes it, **Then** one YouTube video is submitted and
   its resulting publication status is recorded.
4. **Given** YouTube does not confirm publication, **When** the submission fails
   or its outcome is uncertain, **Then** the package remains visibly unresolved
   and is not reported as successfully published.

### Edge Cases

- Fewer or more than three tracks, or duplicate tracks, prevent package approval.
- Missing video, title, description, thumbnail, or rights confirmation keeps the
  package in draft and identifies what must be supplied.
- A rejected or interrupted YouTube submission remains unresolved; retrying must
  not silently create or claim a second successful publication.
- Spotify-derived rankings, data, metadata, artwork, previews, and recordings are
  not accepted as inputs to this feature.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: An editor MUST be able to create one weekly package with exactly
  three distinct, ordered track entries.
- **FR-002**: Track selection and ordering MUST be editor-provided; the feature
  MUST NOT calculate rankings from streaming or listening data.
- **FR-003**: Each package MUST include a selected video, title, description, and
  thumbnail suitable for editor review before publication.
- **FR-004**: The editor MUST confirm publication rights for the video and all
  included media before the package can be approved.
- **FR-005**: The feature MUST require explicit editor approval before submitting
  a package for publication.
- **FR-006**: The feature MUST publish to YouTube only and MUST record whether the
  submission is pending, published, rejected, or unresolved.
- **FR-007**: The feature MUST NOT access, use, display, or distribute Spotify
  Platform data or Spotify Content. Spotify-derived rankings and media are
  explicitly outside this release.
- **FR-008**: A failed or uncertain submission MUST be reported as such and MUST
  preserve the package for review without indicating successful publication.

### Key Entities

- **Weekly Top 3 package**: One week's ordered selections, video and publication
  materials, rights confirmations, approval, and YouTube publication status.
- **Track entry**: An editor-selected track represented by its title, artist,
  position, and editorial source.
- **YouTube publication**: The outcome and status of submitting an approved
  weekly package to the channel.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every approved package contains exactly three distinct track entries
  in the editor's chosen order.
- **SC-002**: At least four of five representative editors can prepare a
  review-ready package in ten minutes or less without assistance.
- **SC-003**: Every published video has recorded editor approval and confirmed
  publication rights before submission.
- **SC-004**: The first release distributes only to YouTube and uses no Spotify
  Platform data or Spotify Content.

## Assumptions

- The weekly Top 3 is an editorial selection, not an automatically generated
  chart or claim about platform-wide popularity.
- The editor supplies or selects a finished video and publication materials;
  automatic video editing is not required.
- The editor is responsible for confirming rights to every track, recording,
  image, and other item included in the video.
- One video per week is sufficient for the minimum release.
- The Spotify policy checklist in
  [spotify-policy-go-no-go.md](./checklists/spotify-policy-go-no-go.md) is a
  separate gate for any future Spotify-related proposal; this feature remains
  Spotify-free regardless of that checklist's outcome.

## Out of Scope

- Spotify integration, Spotify-derived rankings or analytics, and use of Spotify
  audio, previews, metadata, or artwork.
- Automatic trend discovery, multi-platform cross-posting, multiple weekly
  videos, and automatic video editing.
- Any assertion that a track is popular or ranked based on platform data.
