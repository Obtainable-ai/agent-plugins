# Scheduled task prompt templates

Each run starts a fresh session with no memory, so prompts must be complete and standalone. Fill in the `<…>` values; omit lines that don't apply.

The templates below are for **recurring** tasks (rolling lookback). For a **one-time** task, make two changes:

1. Replace the first line with:
   `One-time scheduled team run. Use the peernotes plugin's <skill> skill in scheduled team mode: do not ask questions, do not wait for confirmation.`
2. Replace the `Lookback:` / `Period:` line with an explicit range:
   `Range: <YYYY-MM-DD> to <YYYY-MM-DD> (inclusive, <IANA timezone>)`
   For document sync, add `Max documents this run: <N>` if the admin asked for a full import.

## Peernotes · Meeting notes

```
Scheduled team run. Use the peernotes plugin's transcripts-to-peernotes skill in scheduled team mode: do not ask questions, do not wait for confirmation.

This sync runs on behalf of the team. Sync admin: <name, email>.
Peernotes workspace: <workspace name> (<workspace ORN>)
Sharing: <shared with workspace | private to admin (trial)>
Team sources: <e.g. Fireflies team workspace; Zoom account recordings; Slack channels #eng-meetings, #sales-calls (incl. huddle canvases); Drive shared folder "Meeting transcripts" (ID)>
Lookback: <2 days, or 3 days when today is Monday>
Exclusions: DMs, group DMs, private channels, 1:1 meetings, and titles containing 1:1, confidential, private, personal, HR, interview, performance, legal, compensation<, plus team-specific exclusions>

Copy every team meeting transcript in the lookback window from the team sources into Peernotes as sources (one Markdown transcript source per meeting), skipping excluded meetings and meetings already synced (by Sync ID). Sources are read-only. Finish with a short report of created, skipped, excluded and failed meetings. If Peernotes or all team sources are unavailable, report which connector is missing and stop.
```

## Peernotes · GitHub summaries

```
Scheduled team run. Use the peernotes plugin's github-summaries-to-peernotes skill in scheduled team mode: do not ask questions, do not wait for confirmation.

This sync runs on behalf of the team. Sync admin: <name, email>.
Peernotes workspace: <workspace name> (<workspace ORN>)
Sharing: <shared with workspace | private to admin (trial)>
Repositories: <all repos in org <org> with activity in the period (max 25) | owner/repo, owner/repo>
Team engineering digest: <on | off>
Period: the previous calendar day (<IANA timezone>)

Save one code summary digest source per repository with activity in the period, plus the team engineering digest if on, skipping digests that already exist (by Sync ID). GitHub is read-only. Finish with a short report. If Peernotes or GitHub is unavailable, report which connector is missing and stop.
```

## Peernotes · Document sync

```
Scheduled team run. Use the peernotes plugin's docs-to-peernotes skill in scheduled team mode: do not ask questions, do not wait for confirmation.

This sync runs on behalf of the team. Sync admin: <name, email>.
Peernotes workspace: <workspace name> (<workspace ORN>)
Sharing: <shared with workspace | private to admin (trial)>
Team sources:
- Google Drive: <shared drives / folders with IDs>
- SharePoint/OneDrive: <sites / libraries / folders>
- Notion: <teamspaces / parent pages with IDs>
Lookback: documents modified in the last <2> days
Exclusions: personal drives, restricted documents shared with only a few people, and names/paths containing confidential, private, personal, HR, interview, performance, legal, compensation<, plus team-specific exclusions>

Save new documents as sources and update the existing source for changed ones (by Sync ID and Source modified), up to 50 documents this run. Sources are read-only; never delete anything in Peernotes. Finish with a short report. If Peernotes or a listed source is unavailable, report which connector is missing and continue with the others.
```
