---
name: peernotes-team-setup
description: This skill should be used when a team admin asks to "set up Peernotes for my team", "set up our Peernotes syncs", "schedule the team syncs", "run a one-time team sync", "backfill the last 90 days into Peernotes", "change what we sync to Peernotes", "pause the GitHub summaries", or "show our Peernotes schedules". One person runs this on behalf of the team, choosing the team workspace, team-level sources and exclusions, and scheduling the three syncs as cloud agents via CronCreate (meeting notes included by default, GitHub summaries daily).
---

# Peernotes team setup

Peernotes is a team product. One person, the **sync admin**, installs this plugin, connects the team's sources with their own access, and runs the syncs **on behalf of the team** into a shared team workspace. Teammates see the results in Peernotes without installing anything (they may install the plugin only to ask Claude questions about Peernotes).

Syncs run as cloud scheduled agents (`CronCreate`) in Claude Cowork — no local machine needed. Everything synced becomes visible to the whole workspace, so the setup must be explicit about what is included and excluded.

## The three syncs

| Sync | Skill it runs | Default schedule | Default lookback |
|------|---------------|------------------|------------------|
| Meeting notes | `transcripts-to-peernotes` | Weekdays ~6 pm | 2 days (3 on Mondays) |
| GitHub summaries | `github-summaries-to-peernotes` | Daily ~8 am | The previous calendar day |
| Document sync | `docs-to-peernotes` | Daily ~1 am | 2 days |

**Meeting notes is part of every scheduled setup by default.** Include it alongside any other syncs the admin chose, even if they only named GitHub or documents. Leave it out only when the admin explicitly says they don't want meeting notes. GitHub summaries and Document sync stay optional.

GitHub summaries run daily and cover exactly the previous calendar day in the admin's timezone (Sync ID per day), so daily digests never overlap. This is the one exception to the "lookback = interval + 1 day" rule below.

All three syncs save every synced item as a Peernotes **source** (a Markdown file, or the original file for binaries), never as notes or thoughts. Only the team settings note below is a note.

Run types: **Run now** (in this conversation) or **Recurring** (system cron). Sync IDs prevent duplicates when runs overlap.

## Step 0: Prerequisites

1. Check Peernotes is connected (as in the sync skills). Stop if not.
2. `listWorkspaces`, and `search` the chosen workspace for the settings note `Peernotes team sync settings` (see Step 4). If it exists, load the current configuration from it.
3. Check for existing scheduled agents: call `CronList` and show any agents whose name starts with "Peernotes ·". If the settings note names a different sync admin than the current user, warn that another person already runs the team syncs, and confirm before proceeding (two admins syncing the same sources creates overlapping work).

## Step 1: Team basics (first setup, or when changing)

Ask once, in as few questions as possible:
- **Team workspace**: from `listWorkspaces`. Record name and ORN.
- **Sharing**: shared with the workspace (default and recommended for team syncs), or private to the admin for a trial run first.
- **Syncs to enable** (multi-select) and whether to schedule them or just run now; list Meeting notes first, already included and marked "(included by default)"; the admin can deselect it.
- **When** (Recurring: default or custom schedule) and **range** (Run now: date range; defaults last 7 days, or 90 days for a first document import).

## Step 2: Team scope and exclusions

Configure team-level sources, not personal ones. Details and coverage options in `references/team-sources.md`.

- **Meeting notes**: which team-wide sources to use (notetaker team workspace, Zoom account recordings, specific Slack channels including huddle canvases posted there, a shared transcripts folder or mailbox label). Explain that the admin's own inbox only covers meetings the admin attended.
- **GitHub summaries**: the GitHub org and repos (default: all repos in the org with activity in the period, max 25) and whether to add a cross-repo "Team engineering digest" (default on).
- **Document sync**: shared drives / team folders (Drive, SharePoint/OneDrive), Notion teamspaces or pages. Personal "My Drive" / personal OneDrive are excluded unless a specific folder is listed.
- **Exclusions** (defaults, which the admin can edit): DMs and group DMs, private channels, 1:1 meetings, meetings or documents whose title contains `1:1`, `confidential`, `private`, `personal`, `HR`, `interview`, `performance`, `legal`, `compensation`, and folders with those names. Add any team-specific exclusions (channels, people, keywords).

Show a short summary of what will be visible to the whole workspace and get the admin's confirmation before continuing.

### Connect missing sources before scheduling

Every chosen sync needs its source connector connected **and** working before its task is created. Scheduled runs are unattended, so a missing connector means every run fails silently.

1. `ListConnectors` and check each chosen sync's source: GitHub for GitHub summaries; Google Drive / SharePoint / OneDrive / Notion for documents; at least one transcript source for meeting notes (notetaker, Zoom, Slack, Gmail/Outlook, Google Calendar, shared Drive folder). See `references/team-sources.md`.
2. For each missing or unusable source:
   - **Standard connectors not yet connected** (Slack, Gmail, Google Calendar, Google Drive, GitHub; see `CONNECTORS.md`): these are built-in Cowork connectors. Direct the admin to Settings → Connectors to connect them; no plugin-specific sign-in is needed. Once connected, reload with `ToolSearch` to confirm tools appear.
   - **Bundled with this plugin but not signed in** (Microsoft 365, Notion, Zoom, Dropbox, Fireflies, Otter, Fathom, Gong, Read.ai, Granola; see `CONNECTORS.md`): its tools are missing or return an auth error. Two kinds of bundled connectors behave differently when not signed in — do not confuse "no tools" with "not installed":
     - **Plugin-managed connectors** (Granola, Fireflies, Otter, Fathom, Gong, Read.ai, Zoom, Dropbox, Notion): expose an `mcp__plugin_peernotes_<Name>__authenticate` tool when not signed in. Start the OAuth flow by calling that tool.
     - **Direct HTTP MCP connectors** (Microsoft 365): show **no tools at all** when not signed in — this is normal, not a sign the connector is absent. Direct the admin to Settings → Connectors → the Peernotes plugin to sign in. Once signed in, reload with `ToolSearch` to confirm tools appear.
       - **Microsoft 365** needs a one-time Entra admin consent before sign-in will complete — see `CONNECTORS.md` → Claude Cowork.
   - **Installed but off in this chat** (`connected: true`, `enabledInChat: false`): ask the admin to turn it on in this chat's connector settings.
   - **GitHub** (for GitHub summaries): use the GitHub connector. Check in this order:
     1. GitHub connector tools present → already set up. Remind the admin to grant the connector access to the org's private repos in GitHub's org settings.
     2. Not present → `SearchMcpRegistry` + `SuggestConnectors` for the GitHub connector, or reconnect in Settings → Connectors if already installed.
   - **Not connected**: `SearchMcpRegistry` with the source's name and category keywords, then `SuggestConnectors` with the matching `directoryUuid`s so the admin can install and sign in from the card. Ask the admin to connect it now.
   - **Connected but failing** (for example an "insufficient scope" or auth error on a quick read-only probe like listing one file or one repo): ask the admin to disconnect and reconnect it in Settings → Connectors and approve read access.
   - **Not bundled and not in the registry**: say so plainly and suggest adding a custom connector from Settings → Connectors.
3. After suggesting, ask with AskUserQuestion: "Connected — check again" / "Schedule anyway (runs fail until connected)" / "Skip this sync". On "check again", reload tools (`ToolSearch`) and re-probe. Only create a task for a source that still isn't working if the admin picks "Schedule anyway", and repeat that warning in Step 5.
4. For Run now, stop that sync until its source works.

## Step 3: Execute

**Run now**: run the sync skill interactively with the configuration above (skip its own scope questions), in team mode.

**Recurring**: create a cloud scheduled agent for each sync with `CronCreate`.

Scheduling rules:
- Pass the admin's IANA timezone as `timezone` so the schedule is timezone-aware and survives DST.
- Shift 8 minutes earlier than the round hour/half-hour (e.g. 6 pm → `52 17`, 8 am → `52 7`, 1 am → `52 0`).
- Lookback = interval + 1 day, so a missed or slow run still covers its window. Exception: GitHub summaries always cover exactly the previous calendar day.
- Set `name` to the sync name (e.g. `"Peernotes · Meeting notes"`) so it's easy to find with `CronList`.
- Set `prompt` to the filled template from `references/prompt-templates.md`.

Example calls (fill in `<…>` values):

```
CronCreate(name="Peernotes · Meeting notes",   schedule="52 17 * * 1-5", timezone="America/Los_Angeles", prompt=<filled meeting notes template>)
CronCreate(name="Peernotes · GitHub summaries", schedule="52 7  * * *",   timezone="America/Los_Angeles", prompt=<filled github summaries template>)
CronCreate(name="Peernotes · Document sync",    schedule="52 0  * * *",   timezone="America/Los_Angeles", prompt=<filled document sync template>)
```

Syncs turned off → delete with `CronDelete` using the agent's ID from `CronList`.

## Step 4: Publish the team settings note

Keep one note in the team workspace, shared with the workspace, titled `Peernotes team sync settings`, so the team can see what is synced and who runs it. Create it on first setup directly as a note, never a thought: `generateNote` with `thoughtOrns: []`, `sharedWithWorkspace: true`, and prompt "Reproduce faithfully as a note titled 'Peernotes team sync settings'; do not summarize. Material: <the content below>"; on later changes, regenerate it with `generateNote` and its `noteOrn`.

```
# Peernotes team sync settings
Sync admin: <name, email>
Last updated: <YYYY-MM-DD>
Workspace: <name>

## Meeting notes: <off | recurring schedule | one-time on date>
Sources: <…>

## GitHub summaries: <…>
Org / repos: <…> · Team digest: <on/off>

## Document sync: <…>
Sources: <shared drives, folders, Notion teamspaces>

## Excluded
<exclusion list>

To request changes, comment on this note or contact the sync admin.
Sync ID: settings:team-sync
```

## Step 5: Confirm

One line per sync: schedule in plain language ("weekdays at 5:52 pm Pacific"), scope, workspace, visibility. Remind the admin that if they leave or lose access to the source connectors, the syncs will fail and should be handed over (Step 6).

## Managing later

- **Show**: call `CronList` and read the settings note.
- **Change scope**: `CronDelete` the old agent, then `CronCreate` a new one with the updated prompt; update the settings note.
- **Change schedule**: `CronDelete` the old agent, then `CronCreate` a new one with the updated schedule expression; update the settings note.
- **Pause / resume**: `CronDelete` to pause; `CronCreate` with the same prompt and schedule to resume.
- **Cancel / remove**: `CronDelete` the agent; update the settings note.

## Step 6: Hand over to a new sync admin

Scheduled agents run under the creating admin's connected accounts. To hand over: the new admin installs the plugin, connects their own source connectors in Settings → Connectors, then runs this skill — it loads the configuration from the settings note and creates fresh scheduled agents with `CronCreate`. The old admin then deletes their agents with `CronDelete`. Update `Sync admin` in the settings note.
