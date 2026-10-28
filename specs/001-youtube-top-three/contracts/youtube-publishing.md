# YouTube Publishing Contract

**Boundary**: Human-reviewed browser workflow for publishing one approved weekly
Top 3 video to the MainStay TV YouTube channel. This is an interaction contract,
not a YouTube API specification.

## Inputs

- Approved weekly package containing exactly three editor-selected track entries.
- Finished video, title, description, thumbnail, and confirmed publication rights
  for every included work and media item.
- Editor's authenticated YouTube session and confirmation of the intended channel.

## Preconditions

- Package status is `approved`.
- All required package fields are present.
- Rights for the finished video, thumbnail, tracks, recordings, and other included
  media are explicitly confirmed.
- Spotify Platform data and Spotify Content are absent from package inputs.
- The editor has reviewed the rendered publication materials and intends to publish
  them to YouTube.

## Interaction

1. Present the video, title, description, thumbnail, selected channel, and rights
   confirmation for final editor review.
2. Do not submit while any required information is missing or the editor has not
   approved the package.
3. Use the existing browser-assisted/manual publishing convention. The editor
   completes the final YouTube publish action; the workflow does not perform
   unattended public publication.
4. Record the visible result and, on success, the YouTube video URL or identifier.
5. If the result is rejected or ambiguous, preserve the attempt details and do not
   report publication success.

## Outputs

- **Published**: YouTube visibly confirms the upload/publication and a video
  reference is recorded.
- **Rejected**: YouTube visibly rejects the attempt; record the reason if shown.
- **Unresolved**: The attempt outcome cannot be established; retain it for editor
  reconciliation before any retry.

## Safety and retry rules

- Never store account passwords or expose private account credentials in package
  records, notes, reports, or screenshots.
- Stop if the signed-in channel is not the intended MainStay TV channel.
- Do not mark an attempt `published` based only on initiating upload or seeing a
  progress indicator.
- For an unresolved attempt, check the channel's recent videos before retrying.
  If a video exists, record it against the existing attempt; do not create a
  second publication.
- This contract grants no rights to included music or visual material; the editor
  must confirm rights before approval.
- No Spotify integration, content, or data transfer is part of this interface.
