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

## ~~chat (Slack, Microsoft Teams)

- Search messages in the range for `transcript`, `meeting notes`, `recap`, `huddle notes`, and for posts by notetaker bots/apps (Zoom, Fireflies, Otter, Fathom, Read.ai, Slack huddle notes, Teams meeting recap).
- Check the channel or chat the user names first; otherwise search broadly.
- Read the full thread; transcripts are often in thread replies, snippets, canvases or attached files.
- Microsoft Teams meeting chats may include "Recap" posts with transcript links.

### Slack huddles → canvases

Slack captures huddle notes as **canvases**, not as regular messages. Handle them explicitly:

1. **Find them.** Search Slack in the date range for canvases/files titled like `Huddle notes` (e.g. "Huddle notes: <channel or people> – <date>"). Also search messages for "huddle" / "Huddle notes"; the huddle's message in the channel or DM links to its canvas. If the connector can filter by file type, restrict to canvases.
2. **Read the canvas.** Use the connector's canvas read tool (base name like `slack_read_canvas`) with the canvas ID from the search result or link. Do not use a message or thread reader for canvases; it returns only the link.
3. **Extract.** A huddle canvas typically contains a summary, discussion topics, action items and, when available, a transcript section or a link to the transcript. Use the transcript when present; otherwise use the full canvas content and say in the source that it is AI huddle notes, not a verbatim transcript.
4. **Metadata.** Title: the canvas title (strip the "Huddle notes:" prefix). Date/time: the huddle start time from the canvas or its message. Attendees: the participants listed on the canvas or huddle message. Source link: the canvas permalink.
5. **Never edit the canvas.** Canvas tools can write; only read.

## ~~meeting platform (Zoom, Google Meet, Microsoft Teams)

- List meetings or recordings in the range, then fetch the transcript for each (Zoom cloud recording transcripts, Teams meeting transcripts).
- Google Meet transcripts and Gemini notes are saved as Google Docs in the organizer's Drive ("Meet Recordings" folder); read them via ~~cloud storage.
- Native platform transcripts are usually the most complete; prefer them when de-duplicating.

## ~~notetaker (Fireflies, Otter, Fathom, Gong, tl;dv, Read.ai, Granola)

- Use the connector's list/search tools for meetings or calls in the range, then fetch each transcript (and summary if offered).
- Keep speaker names and the vendor's link to the meeting.

## ~~cloud storage (Google Drive, OneDrive, SharePoint, Dropbox, Box)

Search files modified in the range whose name or content matches `transcript`, `meeting notes`, `Notes by Gemini`, or with extensions `.vtt`, `.srt`, `.txt`, `.docx`. Look in "Meet Recordings" (Drive) and "Recordings" (OneDrive/SharePoint) folders. Read file content with the connector's read/download tool.

## ~~calendar (helper, not a source)

List events in the range to get authoritative titles, times and attendees, and to match transcripts from other sources to the right meeting. Event descriptions sometimes link to notes docs.

## Uploaded files

Transcript files attached to the conversation (.txt, .vtt, .srt, .docx, .pdf, .md) need no connector. Parse title, date and attendees from the file name or content; ask the user if they can't be determined.
