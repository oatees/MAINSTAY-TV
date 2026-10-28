# Quickstart: Validate YouTube-First Weekly Top 3

This is a manual acceptance guide for the planned agent workflow. The repository
does not currently provide a product test runner or an automated YouTube integration.
Do not use uncleared media or publish a test video publicly.

## Prerequisites

- Access to a local copy of the repository and its existing SQLite database setup.
- A test package with three editor-selected, non-duplicate tracks.
- A finished test video and thumbnail for which the editor has confirmed publication
  rights.
- Access to the intended YouTube channel. For end-to-end upload validation, use a
  controlled test channel and keep the test upload private; do not test with a
  public release.
- No Spotify Platform access, Spotify Content, or Spotify-derived ranking data.

## Validation scenarios

### 1. Prepare a valid weekly package

1. Ask the agent to prepare a weekly Top 3 package for a chosen test week.
2. Supply exactly three ordered tracks, a cleared video, title, description, and
   thumbnail; confirm rights for all included material.
3. Review the package before approval.

**Expected**: The package contains the same three tracks in the supplied order and
all publication materials; status remains reviewable until explicit approval.

### 2. Verify incomplete package is blocked

1. Repeat package preparation with only two tracks, or omit one required material
   or rights confirmation.
2. Attempt to approve the package.

**Expected**: Approval is blocked, the missing requirement is identified, and no
YouTube submission occurs.

### 3. Verify approved browser-assisted publishing

1. Use a controlled test channel and rights-cleared private test media.
2. Approve the complete package, verify the channel and all displayed materials,
   then complete the final YouTube action as the editor.
3. Verify the resulting video reference and status.

**Expected**: The video is private on the intended test channel and the package
records `published` only after YouTube confirms the result.

### 4. Verify rejection and uncertain outcome handling

1. Simulate a visible rejection or an interrupted browser session during upload.
2. Check the package and publication attempt state.

**Expected**: The attempt is recorded as `rejected` or `unresolved`, never as
`published` without confirmation. An unresolved attempt is checked against the
channel before any retry.

### 5. Verify the Spotify boundary

1. Attempt to provide Spotify metadata, artwork, preview audio, recordings,
   Platform data, or Spotify-derived rankings as package inputs.

**Expected**: These inputs are refused; the feature remains YouTube-only and
Spotify-free. Follow
[spotify-policy-go-no-go.md](./checklists/spotify-policy-go-no-go.md) before
proposing any separate Spotify-related scope.

## Local record validation

After implementation adds package persistence, verify that the local record
contains exactly three unique positions, all required rights and approval details,
and one consistent publication outcome. Confirm that an unresolved attempt cannot
be silently marked published or retried as a second upload.

The current repository has no implemented feature or test command; no shell
commands are provided until implementation defines one.
