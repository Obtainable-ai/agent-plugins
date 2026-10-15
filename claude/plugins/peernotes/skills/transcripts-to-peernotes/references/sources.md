# Transcript sources: where to look and how

Use whichever connectors are available. Replace the date range with the user's choice.

## ~~email (Gmail, Outlook)

Many meeting tools email a recap or transcript. Gmail query:

```
newer_than:7d (subject:(transcript OR "meeting notes" OR "notes by gemini" OR recap OR "meeting summary") OR from:(gemini-notes@google.com OR meet-recordings-noreply@google.com OR no-reply@zoom.us OR otter.ai OR fireflies.ai OR fathom.video OR gong.io OR tldv.io OR read.ai OR granola.so))
```

For Outlook, search the same subjects and sender domains in the date range. Read the full thread; pull transcript text from the body and any .txt/.vtt/.docx/.pdf attachments.

| Sender | What's in the email |
|--------|---------------------|
| Google Meet / Gemini | Summary in body; full transcript in a linked Google Doc |
| Zoom | Summary in body; transcript via link or .vtt |
| Otter, Fireflies, Fathom, tl;dv, Read.ai, Granola | Summary / action items in body; transcript link |
| Gong | Call brief; link to the call |

## ~~meeting platform (Zoom, Google Meet, Microsoft Teams, Slack)

- List meetings or recordings in the range, then fetch the transcript for each (Zoom cloud recording transcripts, Teams meeting transcripts).
- Google Meet transcripts and Gemini notes are saved as Google Docs in the organizer's Drive ("Meet Recordings" folder); read them via ~~cloud storage.
- Native platform transcripts are usually the most complete; prefer them when de-duplicating.

### Slack huddles → canvas + transcript file

Slack records each huddle as a Slackbot "A huddle started" message in the channel, with a **Huddle notes canvas** attached. The canvas holds Slack's AI summary and links the **huddle transcript**, a separate file. Only the transcript is synced; the AI summary is not.

1. **Find them.** Search Slack in the date range for files titled like `Huddle notes` in the channel (content type: files). Each result is a canvas; the huddle's channel message links it too.
2. **Read the canvas** with the connector's file or canvas read tool (base name like `slack_read_file` or `slack_read_canvas`). From it take:
   - the transcript file ID, from the embedded line `![F…](https://<team>.slack.com/files/USLACKBOT/F…/huddle_transcript)`. No such line → the huddle has no transcript: skip it ("no transcript").
   - start and end time, from "AI took notes for this huddle from **8:00:37 PM - 8:38:59 PM PDT**" on the canvas date.
   - the huddle link, from "[View huddle in channel](https://<team>.slack.com/archives/<channel>/p<digits>)". `url` = that link without its query string; `externalId` = `<channel>/<ts>`, where `ts` is the `p` number with a dot before its last 6 digits (`p1792033236064659` → `1792033236.064659`).
   - attendee user IDs, from the `<@U…>` mentions in the Attendees section.
3. **Read the transcript file** with the file read tool and its file ID. It is JSON (`application/vnd.slack-huddle-transcript`): a list of `{transcript: {results: [...]}}` entries. For each result with `isPartial: false`, take `alternatives[0].transcript` (the text), `startTimeMs`, and the speaker from `alternatives[0].items[*].speakerExternalUserId` (the user ID is the part after the last `-`). Sort by `startTimeMs`, merge consecutive results from the same speaker less than a minute apart, and write one `**<Name>** [<m:ss since the first result>]: <text>` turn each. Resolve user IDs to names (and emails for attendees) with the connector's user-profile tool. If the transcript file can't be read or parsed, record the huddle as failed.
4. **Provider** is `SLACK_HUDDLE`. **Name** is `<channel's meeting name, e.g. "Daily Standup">, <YYYY-MM-DD>`; if two huddles fall on the same date, append the start time, e.g. `Daily Standup, 2026-03-16 (7:00 AM)`.
5. **Never edit the canvas or post in Slack.** Canvas tools can write; only read.

## ~~notetaker (Fireflies, Otter, Fathom, Gong, tl;dv, Read.ai, Granola)

- Use the connector's list/search tools for meetings or calls in the range, then fetch each transcript (and summary if offered).
- Keep speaker names and the vendor's link to the meeting.

## ~~cloud storage (Google Drive, OneDrive, SharePoint, Dropbox)

Search files modified in the range whose name or content matches `transcript`, `meeting notes`, `Notes by Gemini`, or with extensions `.vtt`, `.srt`, `.txt`, `.docx`. Look in "Meet Recordings" (Drive) and "Recordings" (OneDrive/SharePoint) folders. Read file content with the connector's read/download tool.

## ~~calendar (helper, not a source)

List events in the range to get authoritative titles, times and attendees, and to match transcripts from other sources to the right meeting. Event descriptions sometimes link to notes docs.

## Uploaded files

Transcript files attached to the conversation (.txt, .vtt, .srt, .docx, .pdf, .md) need no connector. Parse title, date and attendees from the file name or content; ask the user if they can't be determined.
