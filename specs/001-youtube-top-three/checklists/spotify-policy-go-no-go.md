# Spotify Policy Go/No-Go Checklist

**Purpose**: Decide whether a proposed Spotify-related feature may proceed to
implementation. This checklist does not authorize use by itself.
**Created**: 2026-10-28
**Feature**: [YouTube-First Weekly Top 3](../spec.md)
**Current feature decision**: NO-GO for Spotify integration; the specified release
must remain Spotify-free.
**Review status**: Pending review for any future Spotify-related proposal.

## Decision Rule

- **GO** for a Spotify-related proposal only when every applicable check below is
  satisfied, the proposed use has been reviewed against the current official terms
  and policies, and the responsible reviewer records approval and the review date.
- **NO-GO** if a check fails, is unclear, or has not been reviewed. Do not access
  Spotify Platform data or use Spotify Content while the decision is NO-GO.
- A YouTube-only implementation of the current specification may proceed only
  with Spotify access, Spotify-derived inputs, and Spotify Content excluded.

## Required Checks

- [ ] Describe the exact proposed Spotify data, content, and user interactions;
  do not rely on a general statement such as "use Spotify for the Top 3."
- [ ] Confirm the use is expressly permitted by the current Spotify Developer
  Terms, Developer Policy, and any applicable product or branding requirements.
  Record the exact clauses and reviewer.
- [ ] Confirm the use does not integrate Spotify streams or content with another
  service, including YouTube. Spotify's Developer Policy lists this as prohibited.
- [ ] Confirm no Spotify sound recording is synchronized with video or other
  visual media. Spotify's Developer Policy lists this as prohibited.
- [ ] Confirm no Spotify Platform or Spotify Content is analyzed to create
  rankings, derived listening metrics, benchmarks, user profiles, or similar
  outputs. Spotify's Developer Policy lists this as prohibited.
- [ ] Confirm no Spotify Platform or Spotify Content is used to train or otherwise
  be ingested into an AI or machine-learning model.
- [ ] Confirm no Spotify Content is used in a way that implies Spotify, artist,
  creator, or rights-holder endorsement without applicable permission.
- [ ] If Spotify metadata, cover art, or preview clips are proposed, verify every
  applicable attribution, Spotify mark, link-back, and non-standalone-use rule;
  also resolve whether the proposed cross-service context is allowed.
- [ ] Confirm the proposed service and any public, business, advertising, or
  sponsored use comply with Spotify's commercial-use and public-use restrictions.
- [ ] Confirm required access, account eligibility, user consent, privacy
  disclosures, data controls, security, and retention obligations are satisfied.
- [ ] Confirm the proposal does not rely on scraping, copying, or another data
  source as a workaround for a Spotify restriction.
- [ ] Record the decision, reviewer, date, sources checked, permitted use, and
  explicit exclusions before implementation is authorized.

## Immediate NO-GO Cases for This Project

- Using Spotify streams, recordings, previews, or other Spotify Content in a
  YouTube video or synchronizing recordings with video.
- Deriving the weekly Top 3 ranking or other analysis from Spotify Content or
  Spotify Service data.
- Using Spotify Platform data or Spotify Content as input to AI or machine
  learning.
- Treating attribution, a link to Spotify, or possession of an account as
  permission to use Spotify Content in a YouTube publication.
- Beginning a Spotify integration while any required review is pending or
  policy interpretation is uncertain.

## Official References Reviewed

- [Spotify Developer Policy](https://developer.spotify.com/policy) — the page
  identified itself as effective 2025-05-15 when checked on 2026-10-28.
- [Spotify Developer Terms](https://developer.spotify.com/terms) — the page
  identified itself as version 10, effective 2025-05-15 when checked on
  2026-10-28.
- [Spotify Web API quota modes](https://developer.spotify.com/documentation/web-api/concepts/quota-modes)
  — check current access and eligibility if a future proposal involves the Web
  API.

**Decision**: NO-GO for Spotify use in this feature. Recheck the live official
references and obtain appropriate policy/legal review before evaluating any
future Spotify-related use; this checklist is not legal advice.
