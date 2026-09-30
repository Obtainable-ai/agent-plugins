# Team-level sources

The sync admin's connections determine what can be synced. Prefer sources that cover the whole team rather than one person's account.

## Meeting notes: getting team-wide coverage

| Option | Coverage | What the admin needs |
|--------|----------|----------------------|
| AI notetaker team workspace (Fireflies, Otter Teams, Gong, Fathom Team, Read.ai) | All meetings the notetaker joined for the team | Admin or team-wide access in the notetaker, and its connector |
| Zoom account cloud recordings | All recorded meetings on the Zoom account | Zoom admin role with access to account recordings, and the Zoom connector |
| Slack channels | Huddle notes canvases and recap posts in the chosen channels | Membership in those channels; list specific channels (public by default) |
| Shared transcripts folder (Drive shared drive, SharePoint) | Anything teammates or tools save there (e.g. Google Meet "Meet Recordings", exported transcripts) | Access to the folder; ask the team to save or auto-route transcripts there |
| Shared mailbox or label | Recap emails teammates forward or auto-forward | Access to that mailbox/label; set up a forwarding rule convention |
| Admin's own inbox or calendar | Only meetings the admin attended | Admin's Gmail/Outlook; fine as a supplement, not team coverage |

Recommend the notetaker team workspace or Zoom account when available; otherwise a shared folder or channel convention.

## GitHub

- Org-level: all repos in the org with activity in the period (cap 25 per run; list the rest in the report).
- Or an explicit repo list for the team.
- The admin's GitHub access limits which private repos are visible; only summarize repos the whole workspace is allowed to know about.

## Documents

- Google Drive: shared drives or specific shared folders. Exclude "My Drive" unless a folder is listed.
- SharePoint / OneDrive: team sites and document libraries; exclude personal OneDrive unless a folder is listed.
- Notion: teamspaces or specific parent pages. Skip private pages.
- Only sync documents that the workspace members could reasonably access; when a document's sharing is restricted to a few people, skip it and list it in the report.

## Default exclusions

DMs and group DMs · private channels · 1:1 meetings · titles, folders or pages containing `1:1`, `confidential`, `private`, `personal`, `HR`, `interview`, `performance`, `legal`, `compensation` · credential-like files. The admin can add or remove exclusions during setup.
