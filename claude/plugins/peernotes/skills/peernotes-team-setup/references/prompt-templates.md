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
Team sources: <e.g. Fireflies team workspace; Zoom account recordings; Slack channels #eng-meetings, #sales-calls (incl. huddle transcripts); Drive shared folder "Meeting transcripts" (ID)>
Lookback: <2 days, or 3 days when today is Monday>
Exclusions: DMs, group DMs, private channels, 1:1 meetings, and titles containing 1:1, confidential, private, personal, HR, interview, performance, legal, compensation<, plus team-specific exclusions>

Copy every team meeting transcript in the lookback window from the team sources into Peernotes as meeting sources (one per meeting, transcript only, with meeting metadata), skipping excluded meetings, meetings without a transcript, and meetings already synced (by external ID). Sources are read-only. Finish with a short report of created, skipped, excluded and failed meetings. If Peernotes or all team sources are unavailable, report which connector is missing and stop.
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

## Peernotes · Linear summaries

```
Scheduled team run. Use the peernotes plugin's linear-summaries-to-peernotes skill in scheduled team mode: do not ask questions, do not wait for confirmation.

This sync runs on behalf of the team. Sync admin: <name, email>.
Peernotes workspace: <workspace name> (<workspace ORN>)
Sharing: <shared with workspace | private to admin (trial)>
Linear teams: <all teams with issue activity in the period | ENG, DES, …>
Product digest: <on | off>
Period: the previous calendar day (<IANA timezone>)
Exclusions: private Linear teams, and issues, projects or labels containing confidential, private, personal, HR, interview, performance, legal, compensation, security<, plus team-specific exclusions>

Save one Linear summary source per team with issue activity in the period, plus the product digest if on, skipping summaries that already exist (by Sync ID). Linear is read-only. Finish with a short report. If Peernotes or Linear is unavailable, report which connector is missing and stop.
```

## Peernotes · Slack threads

```
Scheduled team run. Use the peernotes plugin's slack-threads-to-peernotes skill in scheduled team mode: do not ask questions, do not wait for confirmation.

This sync runs on behalf of the team. Sync admin: <name, email>.
Peernotes workspace: <workspace name> (<workspace ORN>)
Sharing: <shared with workspace | private to admin (trial)>
Channels: <#eng (C…), #product (C…), #incidents (C…)>
Lookback: threads with activity in the last <2> days
Max threads this run: 30
Exclusions: DMs, group DMs, private channels, huddle threads, and threads containing 1:1, confidential, private, personal, HR, interview, performance, legal, compensation<, plus team-specific exclusions>

Save each interesting thread (decisions, designs, incidents, customer feedback, how-tos) in the listed channels as a thread source, and update threads that got new replies since they were saved (by external ID). Skip routine chatter. Slack is read-only. Finish with a short report of created, updated, skipped, excluded and failed threads. If Peernotes or Slack is unavailable, report which connector is missing and stop.
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

## Peernotes · Agent sessions

Personal and local: schedule it with `create_scheduled_task` (Claude desktop) or the user's crontab (`claude -p`), never `CronCreate`.

```
Scheduled personal run. Use the peernotes plugin's agent-sessions-to-peernotes skill in scheduled mode: do not ask questions, do not wait for confirmation.

Owner: <name, email> — sync only this user's own sessions on this machine.
Peernotes workspace: <workspace name> (<workspace ORN>)
Sharing: <private (default) | shared with workspace>
Agents: <Claude Code and Codex | Claude Code | Codex>
Repositories: <all | github.com/org/repo, …>
Lookback: sessions active in the last <2> days
Exclusions: sessions whose folder or title contains confidential, private, personal, HR, interview, performance, legal, compensation, secret, credentials<, plus the user's own exclusions>

Save each new session as an agent session source and update sessions that continued since they were saved (by external ID). Session files are read-only. Finish with a short report of created, updated, skipped, excluded and failed sessions. If Peernotes is unavailable or the session files can't be read on this machine, report it and stop.
```
