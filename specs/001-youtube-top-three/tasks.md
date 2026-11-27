# Tasks: YouTube-First Weekly Top 3

**Input**: Design documents from `/specs/001-youtube-top-three/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md),
[research.md](./research.md), [data-model.md](./data-model.md),
[contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: The specification does not request automated tests. Validate the
implemented workflow using the manual scenarios in `quickstart.md`.

## Phase 1: Setup

**Purpose**: Project initialization and basic structure.

No separate setup task is needed: the feature extends existing agent guidance,
JSON hooks, and SQLite schema without adding a runtime, dependency, or project.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add persistent records required by the weekly package workflow.

- [X] T001 Add `weekly_top3_packages`, `weekly_top3_tracks`, `weekly_top3_clearances`, and `youtube_publication_attempts` tables to `agent/init-db.sql`; enforce the data-model constraints: unique non-empty package ID; required week label with only one package per week; video, title, description, and thumbnail required before approval; package status in `draft`, `review`, `approved`, `publishing`, `published`, `rejected`, or `unresolved`; each track has a parent package, required title, artist, editorial source, and rights confirmation, with a unique position per package constrained to 1, 2, or 3; all included media have a reference and confirmed rights with editor and time before approval; each YouTube attempt has a parent approved package, reviewed channel identity, status in `pending`, `published`, `rejected`, or `unresolved`, a video reference for `published`, and outcome note for `rejected` or `unresolved`; allow only one confirmed successful publication per package; do not store account credentials

**Checkpoint**: The existing database initialization script creates all package
records without changing existing table behavior.

---

## Phase 3: User Story 1 - Prepare and publish the weekly Top 3 (Priority: P1)

**Goal**: Allow an editor to prepare and review a complete, rights-cleared
three-track package and publish one video to YouTube with an explicit human
publish action.

**Independent Test**: Follow all scenarios in
`specs/001-youtube-top-three/quickstart.md`. Confirm a valid package can be
reviewed and approved; incomplete rights or materials block approval; a
confirmed YouTube result is recorded; rejected or ambiguous submissions are
not reported as published and are reconciled before retry. Use controlled,
rights-cleared private test media and never publish a test video publicly.

### Implementation for User Story 1

- [X] T002 [P] [US1] Create the user-triggered weekly YouTube Top 3 workflow in `.kiro/hooks/weekly-youtube-top3.json`; have the editor provide exactly three distinct ordered tracks and their non-Spotify editorial sources, a finished video, title, description, thumbnail, and rights confirmations; keep incomplete packages in draft and identify missing fields or clearances; present all materials and the intended YouTube channel for review; require explicit editor approval before submission; leave the final YouTube publish action to the editor; record `published` only after visible confirmation and a video reference, record rejection or uncertainty without claiming success, and reconcile an uncertain attempt against the channel before retrying
- [X] T003 [P] [US1] Update `.kiro/steering/mainstay-agent.md` with the weekly YouTube Top 3 scope and safety rules: selection is editor-provided rather than computed from listening or streaming data; this feature must not access, use, display, or distribute Spotify Platform data or Spotify Content; require confirmed publication rights and explicit approval; stop if the selected YouTube channel is not MainStay TV; and never treat an unconfirmed or interrupted submission as published
- [X] T004 [P] [US1] Update `agent/README.md` to document the YouTube-only weekly Top 3 workflow, its user-triggered entry point `.kiro/hooks/weekly-youtube-top3.json`, the three-track and rights-confirmation requirements, the editor's final publish action, and the unresolved-outcome retry rule without removing existing platform instructions

**Checkpoint**: An editor can independently prepare, approve, and manually
publish one valid weekly package while incomplete or uncertain cases remain
blocked or unresolved.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate the complete workflow and verify the feature boundary.

- [X] T005 Run the manual acceptance scenarios in `specs/001-youtube-top-three/quickstart.md` against the implemented workflow and initialized local database; verify the exact-three-track rule, required-field and rights gates, explicit approval, intended-channel check, confirmed publication status, unresolved retry protection, and Spotify-free inputs; use a controlled private test channel and record any unmet scenario in `specs/001-youtube-top-three/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No separate setup task; no new runtime or dependency is
  required.
- **Foundational (Phase 2)**: T001 must complete before the workflow uses package
  persistence.
- **User Story 1 (Phase 3)**: Depends on T001. T002 implements the workflow;
  T003 and T004 can proceed in parallel with T002 because they modify separate
  guidance files.
- **Polish (Phase 4)**: T005 depends on T001-T004.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after T001. No other user stories or feature
  dependencies exist.

### Within User Story 1

- Create the database tables before implementing the workflow that reads and
  writes package state.
- T003 and T004 may run in parallel with T002; they change separate files and
  take their scope directly from the feature spec and contract.
- Complete T002-T004 before running T005.

### Parallel Opportunities

- After T001, T002, T003, and T004 can be handled concurrently because they
  modify separate files.
- T005 is a final validation task and is not parallelizable with implementation.

---

## Parallel Example: User Story 1

```text
After T001:
Task: Implement the user-triggered package and YouTube publishing workflow in .kiro/hooks/weekly-youtube-top3.json (T002)
Task: Add YouTube Top 3 policy and review guidance in .kiro/steering/mainstay-agent.md (T003)
Task: Document the editor workflow in agent/README.md (T004)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001 to establish package persistence.
2. Complete T002-T004 to deliver the editor workflow, policy boundary, and
   operator instructions.
3. Complete T005 using controlled private test media and the manual quickstart.
4. Do not expand the MVP to Spotify, other publishing destinations, API uploads,
   or unattended public publishing.

### Incremental Delivery

There is one user story. Deliver it as a complete increment after its database
prerequisite, and do not start a separate Spotify feature without a distinct
policy review and approved scope.

---

## Notes

- `[P]` marks tasks that can be performed in parallel on separate files.
- `[US1]` maps story tasks to User Story 1 in `spec.md`.
- No automated test tasks are included because the feature specification does
  not request them and the project has no established product test runner.

## Phase 5: Convergence

- [X] T006 Add the missing weekly Top 3 package, track, clearance, and YouTube publication tables with all data-model constraints to `agent/init-db.sql` per plan: storage decision (missing)
- [X] T007 Create the missing user-triggered weekly YouTube Top 3 workflow in `.kiro/hooks/weekly-youtube-top3.json` with three distinct ordered tracks, rights confirmations, explicit approval gate, and unresolved-retry handling per US1/AC1 (missing)
- [X] T008 Update `.kiro/steering/mainstay-agent.md` to remove the engagement-based ranking statement that conflicts with FR-002 and add the YouTube Top 3 scope and safety rules per FR-002 (contradicts)
- [X] T009 Document the YouTube-only weekly Top 3 workflow, entry point, and unresolved retry rule in `agent/README.md` per FR-006 (missing)
