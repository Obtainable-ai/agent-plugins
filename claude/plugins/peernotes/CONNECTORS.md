# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. Workflows are described by category rather than product, so they work with whichever tools you use.

## Required

| Connector | Used by | Notes |
|-----------|---------|-------|
| Peernotes | All skills | Gives Claude access to all your Peernotes data (search, read, create, edit, comment, manage) and is the destination for every sync. |

## Per sync (each sync is optional; the sync admin connects only what the team uses)

Connect team-level access where possible: a notetaker team workspace or Zoom admin account rather than a personal inbox, the GitHub org, shared drives and Notion teamspaces. See `skills/peernotes-team-setup/references/team-sources.md`.

### Meeting notes (`transcripts-to-peernotes`), at least one source

| Category | Placeholder | Options |
|----------|-------------|---------|
| Email | `~~email` | Gmail, Microsoft Outlook |
| Meeting platform | `~~meeting platform` | Zoom, Google Meet, Microsoft Teams, Slack |
| AI notetaker | `~~notetaker` | Fireflies, Otter, Fathom, Gong, tl;dv, Read.ai, Granola |
| Cloud storage | `~~cloud storage` | Google Drive, OneDrive, SharePoint, Dropbox |
| Calendar (optional helper) | `~~calendar` | Google Calendar, Outlook Calendar |

### GitHub summaries (`github-summaries-to-peernotes`)

| Category | Options |
|----------|---------|
| Source control | GitHub connector |

### Linear summaries (`linear-summaries-to-peernotes`)

| Category | Options |
|----------|---------|
| Project tracker | Linear connector (bundled) |

### Slack threads (`slack-threads-to-peernotes`)

| Category | Options |
|----------|---------|
| Chat | Slack connector (standard) |

### Document sync (`docs-to-peernotes`), at least one source

| Category | Placeholder | Options |
|----------|-------------|---------|
| Cloud storage | `~~cloud storage` | Google Drive, OneDrive, SharePoint |
| Wiki | `~~wiki` | Notion |

### Agent sessions (`agent-sessions-to-peernotes`)

No source connector: the skill reads Claude Code (`~/.claude/projects`) and Codex (`~/.codex/sessions`) session files directly, so it runs only in Claude Code on the machine that holds them. Only Peernotes is required.

## Standard connectors (use your existing connection)

These are built-in Claude Cowork connectors. The plugin uses whichever is already connected — no plugin-specific sign-in needed.

| Connector | Used by |
|-----------|---------|
| Slack | Meeting notes (huddle canvases, recaps); Slack threads |
| Gmail | Meeting notes (recap emails) |
| Google Calendar | Meeting notes (helper) |
| Google Drive | Meeting notes (shared transcript folders); Document sync |

## Bundled connectors

The plugin bundles these servers in `.mcp.json`. Installing the plugin offers each one; sign in only to the ones your team's syncs use. Unused ones can stay signed out.

| Connector | Endpoint | Used by |
|-----------|----------|---------|
| Peernotes | `https://api.peernotes.io/mcp` | All skills (required) |
| GitHub | `https://api.githubcopilot.com/mcp/` | GitHub summaries. The org must also install the [Claude GitHub MCP connector app](https://github.com/apps/claude-github-mcp-connector) |
| Linear | `https://mcp.linear.app/mcp` | Linear summaries |
| Microsoft 365 | `https://mcp.microsoft365.com/mcp` | Meeting notes (Outlook, Teams); Document sync (OneDrive, SharePoint). Needs a one-time Entra admin consent |
| Notion | `https://mcp.notion.com/mcp` | Document sync |
| Zoom | `https://zoom.us/mcp/meeting/streamable` | Meeting notes |
| Dropbox | `https://mcp.dropbox.com/mcp` | Meeting notes (transcript folders) |
| Fireflies | `https://api.fireflies.ai/mcp` | Meeting notes |
| Otter | `https://mcp.otter.ai/mcp` | Meeting notes |
| Fathom | `https://api.fathom.ai/mcp` | Meeting notes |
| Gong | `https://mcp.gong.io/mcp` | Meeting notes (paid seat, admin must enable) |
| Read.ai | `https://api.read.ai/mcp` | Meeting notes (beta) |
| Granola | `https://mcp.granola.ai/mcp` | Meeting notes |

All use OAuth sign-in via Settings → Connectors. Gong and Microsoft 365 still need an admin to consent or enable, and GitHub needs its GitHub App installed on the org.

**Not available as hosted connectors:**
- **tl;dv:** there's no hosted server, only a self-hosted one.
- **Google Meet:** use Drive "Meet Recordings", Gmail or Calendar instead.

## Claude Cowork

Sign in to each connector you need from **Settings → Connectors → Peernotes plugin**. No `/mcp` command or local setup required.

Most connectors work immediately after sign-in. A few need one-time configuration first:

**Google services (Gmail, Google Calendar, Google Drive)** — sign in via Settings → Connectors. No OAuth client or Google Cloud project needed; Cowork handles authentication natively.

**Microsoft 365 (Outlook, Teams, OneDrive, SharePoint)** — needs a one-time Entra admin consent for the MCP app in your organization's tenant, then sign in via Settings → Connectors as usual.

**GitHub** — two steps:
1. **Install the GitHub App on your org:** open https://github.com/apps/claude-github-mcp-connector, click **Install** (or **Configure** if it's already installed), choose the team's GitHub organization, and grant access to **All repositories** or the repos the team wants summarized. An org owner must approve it; others can request it from the same page.
2. **Sign in:** connect **GitHub** from Settings → Connectors → Peernotes plugin.

Without the app, the connector only sees public repos and repos your personal account can reach, so the daily summaries miss the org's private repos.

## Scheduling

Syncs run as cloud scheduled agents (`CronCreate`) — no local machine needed. `peernotes-team-setup` creates the agents and stores the schedule in the team settings note. Manage them later with `CronList` and `CronDelete`.
