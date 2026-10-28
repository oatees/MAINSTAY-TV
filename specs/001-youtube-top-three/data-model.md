# Data Model: YouTube-First Weekly Top 3

This model describes the minimum information required by the feature. It does not
prescribe a database migration or implementation code.

## Weekly Top 3 Package

Represents the reviewable weekly YouTube publication package.

| Field | Meaning | Validation |
|---|---|---|
| Package ID | Stable identity for this weekly package | Unique and non-empty |
| Week label | Week this package represents | Required; only one package per week |
| Video asset reference | Selected finished video | Required before approval; must refer to an existing project asset |
| Title | YouTube video title | Required before approval |
| Description | YouTube video description | Required before approval |
| Thumbnail reference | Selected thumbnail image | Required before approval |
| Status | Current editorial and publication state | One of `draft`, `review`, `approved`, `publishing`, `published`, `rejected`, `unresolved` |
| Approved by / at | Editor identity and time of explicit approval | Required before publication submission |
| Created / updated at | Record timestamps | Required |

### State transitions

`draft` → `review` → `approved` → `publishing` → `published`

- Incomplete packages remain `draft` and identify missing fields or clearances.
- An editor may return a `review` package to `draft` for corrections.
- A rejected submission becomes `rejected`; an interrupted or ambiguous result
  becomes `unresolved`.
- `rejected` and `unresolved` packages require editor review before another
  attempt. An unresolved attempt must be reconciled against YouTube before retry
  to avoid duplicate publication.
- A package becomes `published` only after a visible YouTube confirmation is
  recorded.

## Track Entry

Represents one editor-selected track in the weekly Top 3.

| Field | Meaning | Validation |
|---|---|---|
| Package ID | Parent weekly package | Must reference one package |
| Position | Editorial order | Exactly one of 1, 2, or 3; unique within package |
| Track title | Track represented | Required |
| Artist name | Track artist or credited artists | Required |
| Editorial source | Human-provided reason or source for selection | Required; must not use Spotify-derived data |
| Rights confirmed by / at | Editor's confirmation that the track and recording may be published in the video | Required before package approval |

Each package must have exactly three entries, each with a unique position. Duplicate
track entries are not allowed.

## Publication Media Clearance

Represents rights checks for the video and media used in it.

| Field | Meaning | Validation |
|---|---|---|
| Package ID | Parent weekly package | Must reference one package |
| Media reference | Video, image, audio, or other included item | Required |
| Rights status | Whether publication rights are confirmed | Must be confirmed before approval |
| Confirmed by / at | Editor and confirmation time | Required when rights are confirmed |

All included media, including the finished video and thumbnail, must have confirmed
publication rights. A track entry's recording clearance must be represented before
the package can be approved.

## YouTube Publication

Represents one attempt and its confirmed result on YouTube.

| Field | Meaning | Validation |
|---|---|---|
| Package ID | Package being submitted | Must reference an approved package |
| Channel identity | YouTube channel selected by the editor | Must be reviewed before submission |
| Attempt status | `pending`, `published`, `rejected`, or `unresolved` | Required; only confirmed success is `published` |
| YouTube video reference | Video URL or identifier returned/visible after upload | Required for `published` |
| Attempted / confirmed at | Submission and result timestamps | Required as applicable |
| Outcome note | Rejection reason or unresolved details | Required for `rejected` or `unresolved` |

An uncertain attempt cannot be silently retried. The editor must first determine
whether YouTube created a video and associate that result with the original attempt.

## Relationships

- One **Weekly Top 3 Package** contains exactly three **Track Entries**.
- One package has clearance records for all media included in its video.
- One package may have one or more **YouTube Publication** attempts, but only one
  confirmed successful publication.
- **YouTube Publication** attempts do not import Spotify metadata, rankings,
  artwork, previews, recordings, or analytics.
