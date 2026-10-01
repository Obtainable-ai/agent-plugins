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

### Document sync (`docs-to-peernotes`), at least one source

| Category | Placeholder | Options |
|----------|-------------|---------|
| Cloud storage | `~~cloud storage` | Google Drive, OneDrive, SharePoint |
| Wiki | `~~wiki` | Notion |

## Standard connectors (use your existing connection)

These are built-in Claude Cowork connectors. The plugin uses whichever is already connected — no plugin-specific sign-in needed.

| Connector | Used by |
|-----------|---------|
| Slack | Meeting notes (huddle canvases, recaps) |
| Gmail | Meeting notes (recap emails) |
| Google Calendar | Meeting notes (helper) |
| Google Drive | Meeting notes (shared transcript folders); Document sync |
| GitHub | GitHub summaries — install and connect via Settings → Connectors; grant it access to the org's private repos in GitHub's org settings |

## Bundled connectors

The plugin bundles these servers in `.mcp.json`. Installing the plugin offers each one; sign in only to the ones your team's syncs use. Unused ones can stay signed out.

| Connector | Endpoint | Used by |
|-----------|----------|---------|
| Peernotes | `https://api.peernotes.io/mcp` | All skills (required) |
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

All use OAuth sign-in via Settings → Connectors. Gong and Microsoft 365 still need an admin to consent or enable.

**Not available as hosted connectors:**
- **tl;dv:** there's no hosted server, only a self-hosted one.
- **Google Meet:** use Drive "Meet Recordings", Gmail or Calendar instead.

## Claude Cowork

Sign in to each connector you need from **Settings → Connectors → Peernotes plugin**. No `/mcp` command or local setup required.

Most connectors work immediately after sign-in. A few need one-time configuration first:

**Google services (Gmail, Google Calendar, Google Drive)** — sign in via Settings → Connectors. No OAuth client or Google Cloud project needed; Cowork handles authentication natively.

**Microsoft 365 (Outlook, Teams, OneDrive, SharePoint)** — needs a one-time Entra admin consent for the MCP app in your organization's tenant, then sign in via Settings → Connectors as usual.

**GitHub** — install and connect the GitHub connector from Settings → Connectors. Grant it access to the org's private repos in GitHub's org settings.

## Scheduling

Syncs run as cloud scheduled agents (`CronCreate`) — no local machine needed. `peernotes-team-setup` creates the agents and stores the schedule in the team settings note. Manage them later with `CronList` and `CronDelete`.
