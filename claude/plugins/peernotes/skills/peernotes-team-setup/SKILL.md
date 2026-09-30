---
name: peernotes-team-setup
description: This skill should be used when a team admin asks to "set up Peernotes for my team", "set up our Peernotes syncs", "schedule the team syncs", "run a one-time team sync", "backfill the last 90 days into Peernotes", "change what we sync to Peernotes", "pause the GitHub summaries", or "show our Peernotes schedules". One person runs this on behalf of the team, choosing the team workspace, team-level sources and exclusions, and recurring or one-time runs for the three syncs (meeting notes included by default, GitHub summaries daily).
---

# Peernotes team setup

Peernotes is a team product. One person, the **sync admin**, installs this plugin, connects the team's sources with their own access, and runs the syncs **on behalf of the team** into a shared team workspace. Teammates see the results in Peernotes without installing anything (they may install the plugin only to ask Claude questions about Peernotes).

Scheduled tasks run under the sync admin's account and connections. Everything synced becomes visible to the whole workspace, so the setup must be explicit about what is included and excluded.

Always call these "scheduled tasks" when talking to the user, never triggers, routines or cron jobs.

## The three syncs

| Sync | Skill it runs | Recurring task name | Default schedule | Default lookback |
|------|---------------|---------------------|------------------|------------------|
| Meeting notes | `transcripts-to-peernotes` | `Peernotes · Meeting notes` | Weekdays ~6 pm | 2 days (3 on Mondays) |
| GitHub summaries | `github-summaries-to-peernotes` | `Peernotes · GitHub summaries` | Daily ~8 am | The previous calendar day |
| Document sync | `docs-to-peernotes` | `Peernotes · Document sync` | Daily ~1 am | 2 days |

**Meeting notes is part of every scheduled setup by default.** Whenever the admin sets up or changes recurring or one-time schedules, include the `Peernotes · Meeting notes` task (running `transcripts-to-peernotes`) alongside the other syncs they chose, even if they only named GitHub or documents. Leave it out only when the admin explicitly says they don't want meeting notes. GitHub summaries and Document sync stay optional.

GitHub summaries run daily and cover exactly the previous calendar day in the admin's timezone (Sync ID per day), so daily digests never overlap. This is the one exception to the "lookback = interval + 1 day" rule below.

All three syncs save every synced item as a Peernotes **source** (a Markdown file, or the original file for binaries), never as notes or thoughts. Only the team settings note below is a note.

Run types: **Run now** (in this conversation), **One-time** (once at a chosen date/time, `run_once_at`), **Recurring** (`cron_expression`). One-time tasks are named `Peernotes · <Sync> · one-time <YYYY-MM-DD HH:MM>` so they never replace a recurring task. Sync IDs prevent duplicates when runs overlap.

## Step 0: Prerequisites

1. Check Peernotes is connected (as in the sync skills). Stop if not.
2. For One-time or Recurring runs, load the scheduling tools with ToolSearch: `select:mcp__claude-code-remote__create_trigger,mcp__claude-code-remote__list_triggers,mcp__claude-code-remote__update_trigger,mcp__claude-code-remote__delete_trigger` (or a keyword search for `trigger`). If they're unavailable, pick the first scheduler that is:
   - **Desktop scheduled tasks** (the Claude desktop app's Code tab): `select:mcp__scheduled-tasks__create_scheduled_task,mcp__scheduled-tasks__list_scheduled_tasks,mcp__scheduled-tasks__update_scheduled_task,mcp__scheduled-tasks__delete_scheduled_task`. These run on the admin's machine while the app is open, so local `git` and `gh` logins work. Mention that runs are skipped while the app is closed and catch up on next launch.
   - **Claude Code CLI with no scheduler tools:** offer a cron or CI job instead (Step 3, "Unattended CLI").
   - Otherwise say scheduling isn't available in this environment and offer Run now.
3. `list_triggers` or `list_scheduled_tasks` (with `include_completed: true` if asked about past one-time runs); find tasks named `Peernotes ·`.
4. `listWorkspaces`, and `search` the chosen workspace for the settings note `Peernotes team sync settings` (see Step 4). If it exists, load the current configuration from it and from the tasks.
5. If the settings note names a different sync admin than the current user, warn that another person already runs the team syncs, and confirm before creating tasks (two admins syncing the same sources creates overlapping work).

## Step 1: Team basics (first setup, or when changing)

Ask once, in as few questions as possible:
- **Team workspace**: from `listWorkspaces`. Record name and ORN.
- **Sharing**: shared with the workspace (default and recommended for team syncs), or private to the admin for a trial run first.
- **Syncs to enable** (multi-select) and the **run type** for each; infer from the request when clear ("every Friday" → Recurring, "once tonight" → One-time, "now" → Run now). For scheduled runs, list Meeting notes first, already included and marked "(included by default)"; the admin can deselect it.
- **When** (Recurring: default or custom schedule; One-time: date and time) and **range** (Run now / One-time: date range; defaults last 7 days, or 90 days for a first document import).
- **Notifications** to the admin when runs finish (optional).

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
   - **Bundled with this plugin but not signed in** (Slack, Gmail, Google Calendar, Microsoft 365, Notion, Zoom, Dropbox, Fireflies, Otter, Fathom, Gong, Read.ai, Granola; see `CONNECTORS.md`): its tools are missing or return an auth error. Ask the admin to sign in to it from the plugin's connectors in Settings → Connectors (or Customize → the Peernotes plugin), then check again.
   - **Installed but off in this chat** (`connected: true`, `enabledInChat: false`): ask the admin to turn it on in this chat's connector settings.
   - **Standard directory connectors** (GitHub, Google Drive, Box): not bundled. Missing or disconnected → reconnect in Settings → Connectors, or `SearchMcpRegistry` + `SuggestConnectors` if not installed. For GitHub, remind the admin to grant it access to the org's private repos.
   - **Not connected**: `SearchMcpRegistry` with the source's name and category keywords, then `SuggestConnectors` with the matching `directoryUuid`s so the admin can install and sign in from the card. Ask the admin to connect it now.
   - **Connected but failing** (for example an "insufficient scope" or auth error on a quick read-only probe like listing one file or one repo): ask the admin to disconnect and reconnect it in Settings → Connectors and approve read access.
   - **Not bundled and not in the registry**: say so plainly and suggest adding a custom connector from Settings → Connectors.
   - **In Claude Code**: sign-in is `/mcp`, not Settings → Connectors, and there are no connect cards. Bundled Slack, Gmail, Google Calendar, Microsoft 365 and Zoom don't work there. Offer the alternatives in `CONNECTORS.md` → Claude Code, such as the `gh` CLI for GitHub, Slack's official plugin, or a notetaker for meetings.
3. After suggesting, ask with AskUserQuestion: "Connected — check again" / "Schedule anyway (runs fail until connected)" / "Skip this sync". On "check again", reload tools (`ToolSearch`) and re-probe. Only create a task for a source that still isn't working if the admin picks "Schedule anyway", and repeat that warning in Step 5.
4. For Run now, stop that sync until its source works.

## Step 3: Execute

**Run now**: run the sync skill interactively with the configuration above (skip its own scope questions), in team mode.

**One-time**: `create_trigger` with `name` (one-time format), `run_once_at` (RFC 3339, from the admin's local time, exact), `prompt` from `references/prompt-templates.md` (one-time variant with explicit `Range:`), `initiation: "human_request"`, `notifications` if chosen. No `cron_expression`, `requires_local_device` or `permission_mode`.

**Recurring**: `CRON_TZ=<admin's IANA zone>`; shift times on the hour/half hour a few minutes earlier (6 pm → `52 17`). Lookback = interval + 1 day. Update the existing task with the same name via `update_trigger`, otherwise `create_trigger` (same fields as above with `cron_expression`; leave `permission_mode` unset).

Syncs turned off → `update_trigger` `enabled: false` (pause) or `delete_trigger` (remove).

**Desktop scheduled tasks** (when the trigger tools are unavailable): `create_scheduled_task` with `taskId` (kebab-case, e.g. `peernotes-meeting-notes`), `title` (the task name above), `description`, and `prompt` from `references/prompt-templates.md`. Pass `cronExpression` in the admin's **local** time (no `CRON_TZ`) for Recurring, or `fireAt` (ISO 8601 with offset) for One-time. Change, pause or remove tasks with `update_scheduled_task` / `delete_scheduled_task`.

**Unattended CLI** (Claude Code without scheduler tools, or when the admin prefers cron or CI): don't create anything. Give the admin the prompt from `references/prompt-templates.md` saved as a file, plus one command to schedule:
- cron on a machine that stays on: `52 17 * * 1-5 cd <dir> && claude -p "$(cat peernotes-meeting-notes.txt)" >> peernotes-sync.log 2>&1`
- GitHub Actions: a `schedule:` workflow that runs the same `claude -p` command. It needs `ANTHROPIC_API_KEY` (or `CLAUDE_CODE_OAUTH_TOKEN`) as a repo secret, and the MCP sign-ins must work non-interactively there.
Tell the admin that `/mcp` sign-ins and `gh`/`git` logins must already be in place for the user that runs the job.

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

One line per sync: run type, when in plain language ("weekdays at 5:52 pm Pacific"), scope, workspace, visibility. Say which approval setting each scheduled task received; if runs will ask for approval, mention "Automatically approve" in the task's settings (if the organization allows it), since team syncs run unattended. Mention that runs use the admin's connections, so if the admin leaves or loses access, the syncs stop and should be handed over (Step 6).

## Managing later

- **Show**: `list_triggers` (or `list_scheduled_tasks`) filtered by `Peernotes ·` (recurring and pending one-time separately) plus the settings note.
- **Change**: `update_trigger` (schedule or `run_once_at`) with a rebuilt prompt if scope changed; update the settings note.
- **Pause / resume**: `update_trigger` `enabled`.
- **Cancel / remove**: confirm, then `delete_trigger`; update the settings note.

## Step 6: Hand over to a new sync admin

Scheduled tasks belong to the account that created them. To hand over: the new admin installs the plugin, connects the sources, and runs this skill; it loads the configuration from the settings note and recreates the tasks under their account. The old admin then removes their tasks (or pauses them first). Update `Sync admin` in the settings note.
