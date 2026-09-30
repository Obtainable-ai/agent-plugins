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
| Chat | `~~chat` | Slack (messages and huddle-notes canvases), Microsoft Teams |
| Meeting platform | `~~meeting platform` | Zoom, Google Meet, Microsoft Teams |
| AI notetaker | `~~notetaker` | Fireflies, Otter, Fathom, Gong, tl;dv, Read.ai, Granola |
| Cloud storage | `~~cloud storage` | Google Drive, OneDrive, SharePoint, Dropbox, Box |
| Calendar (optional helper) | `~~calendar` | Google Calendar, Outlook Calendar |

### GitHub summaries (`github-summaries-to-peernotes`)

| Category | Options |
|----------|---------|
| Source control | `gh` CLI (`gh auth login`, no OAuth app needed) or GitHub connector |

### Document sync (`docs-to-peernotes`), at least one source

| Category | Placeholder | Options |
|----------|-------------|---------|
| Cloud storage | `~~cloud storage` | Google Drive, OneDrive, SharePoint |
| Wiki | `~~wiki` | Notion |

## Bundled connectors

The plugin bundles these servers in `.mcp.json`. Installing the plugin offers each one, and you sign in only to the ones your team's syncs use. Unused ones can stay signed out.

| Connector | Endpoint | Used by |
|-----------|----------|---------|
| Peernotes | `https://api.peernotes.io/mcp` | All skills (required) |
| Slack | `https://slack.mcp.claude.com/mcp` | Meeting notes (huddle canvases, recaps) |
| Gmail | `https://gmail.mcp.claude.com/mcp` | Meeting notes (recap emails) |
| Google Calendar | `https://gcal.mcp.claude.com/mcp` | Meeting notes (helper) |
| Microsoft 365 | `https://microsoft365.mcp.claude.com/mcp` | Meeting notes (Outlook, Teams); Document sync (OneDrive, SharePoint). Needs a one-time Entra admin consent |
| Notion | `https://mcp.notion.com/mcp` | Document sync |
| Zoom | `https://zoom.us/mcp/meeting/streamable` | Meeting notes |
| Dropbox | `https://mcp.dropbox.com/mcp` | Meeting notes (transcript folders) |
| Fireflies | `https://api.fireflies.ai/mcp` | Meeting notes |
| Otter | `https://mcp.otter.ai/mcp` | Meeting notes |
| Fathom | `https://api.fathom.ai/mcp` | Meeting notes |
| Gong | `https://mcp.gong.io/mcp` | Meeting notes (paid seat, admin must enable) |
| Read.ai | `https://api.read.ai/mcp` | Meeting notes (beta) |
| Granola | `https://mcp.granola.ai/mcp` | Meeting notes |

All use OAuth sign-in with no per-organization app setup (Microsoft 365 and Gong still need an admin to consent or enable). If an organization already has one of these as a standard connector, the skills use that one instead.

**Not bundled, use the standard Claude connectors:** these servers need an OAuth app registered for each host or organization, so a plugin can't ship a working sign-in for them. The Claude connector directory already has them, and the skills show a connect card when they're missing.
- **Google Drive:** used by meeting notes (shared transcript folders) and document sync.
- **Box:** used by meeting notes (transcript folders).

**GitHub** does not need a connector or OAuth app: the `gh` CLI (`gh auth login`) is sufficient and is the recommended path. A GitHub connector can be used instead if already installed.

**Not available as hosted connectors:**
- **tl;dv:** there's no hosted server, only a self-hosted one.
- **Google Meet:** use Drive "Meet Recordings", Gmail or Calendar instead.

## Claude Code

Claude Code (the CLI, IDE extensions and the desktop app's Code tab) loads the same plugin, with a few differences:

- **Sign-in:** run `/mcp` to sign in to the bundled servers. Settings → Connectors and connect cards aren't available, and claude.ai connectors don't carry over.
- **Bundled servers that only work in Claude apps:** Slack, Gmail, Google Calendar and Microsoft 365 are hosted on `*.mcp.claude.com`, and the Zoom entry relies on the app's own Zoom sign-in. In Claude Code these show as failed or can't finish sign-in. That's expected, so leave them signed out and use the alternatives below.
- **Everything else bundled** (Peernotes, Notion, Dropbox, Fireflies, Otter, Fathom, Gong, Read.ai, Granola) signs in through `/mcp` as usual.

| Need | Claude Code alternative |
|------|-------------------------|
| Slack | Install Slack's official plugin: `claude plugin install slack@claude-plugins-official`, then `/mcp` to sign in. The workspace admin may need to approve the Slack MCP integration first |
| GitHub | The local `gh` CLI (`gh auth login`), which also covers private repos. Or the `github@claude-plugins-official` plugin with a personal access token in `GITHUB_PERSONAL_ACCESS_TOKEN` |
| Gmail, Google Calendar, Google Drive | Google's MCP servers (`https://gmailmcp.googleapis.com/mcp/v1`, `https://calendarmcp.googleapis.com/mcp/v1`, `https://drivemcp.googleapis.com/mcp/v1`) need an OAuth client from the organization's own Google Cloud project: `claude mcp add --transport http --client-id <id> --client-secret gmail <url>`. Otherwise use a notetaker or Dropbox for transcripts, and Notion for documents |
| Zoom, Microsoft 365 (Outlook, Teams, OneDrive, SharePoint) | No public server that works without per-organization app registration. Use a notetaker (Fireflies, Otter, Fathom, Gong, Read.ai, Granola) that records these meetings |

## Scheduling

- **Cowork and claude.ai:** `peernotes-team-setup` uses the app's built-in scheduled tasks, so no extra connector is needed. Scheduled tasks run under the sync admin's account.
- **Claude desktop app, Code tab:** Desktop scheduled tasks run on the admin's machine while the app is open, with local `git` and `gh` logins.
- **Claude Code CLI:** run a sync unattended from cron or a CI job, for example `claude -p "/peernotes:github-summaries-to-peernotes"`. Signed-in `/mcp` servers and local `git`/`gh` logins work there. Cloud routines (`/schedule`) can reach only connectors, not local logins.
