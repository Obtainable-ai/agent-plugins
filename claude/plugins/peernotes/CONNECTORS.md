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
| Slack | `https://mcp.slack.com/mcp` | Meeting notes (huddle canvases, recaps) |
| Gmail | `https://gmailmcp.googleapis.com/mcp/v1` | Meeting notes (recap emails). Needs a Google Cloud OAuth client — see Claude Code below |
| Google Calendar | `https://calendarmcp.googleapis.com/mcp/v1` | Meeting notes (helper). Same OAuth client as Gmail |
| Google Drive | `https://drivemcp.googleapis.com/mcp/v1` | Meeting notes (shared transcript folders); Document sync. Same OAuth client |
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

All use OAuth sign-in. Gong and Microsoft 365 still need an admin to consent or enable. Google services (Gmail, Calendar, Drive) need an OAuth client from your org's Google Cloud project — see the Claude Code section below. If an organization already has one of these as a standard connector, the skills use that one instead.

**GitHub** does not use a connector: the `gh` CLI (`gh auth login --scopes 'repo'`) is sufficient and is the recommended path. A GitHub connector can be used instead if already installed.

**GitHub** does not need a connector or OAuth app: the `gh` CLI (`gh auth login`) is sufficient and is the recommended path. A GitHub connector can be used instead if already installed.

**Not available as hosted connectors:**
- **tl;dv:** there's no hosted server, only a self-hosted one.
- **Google Meet:** use Drive "Meet Recordings", Gmail or Calendar instead.

## Claude Code

Claude Code (the CLI, IDE extensions and the desktop app's Code tab) loads the same plugin. All bundled connectors work; sign in with `/mcp`. Settings → Connectors and connect cards aren't available, and claude.ai connectors don't carry over.

Most connectors sign in with `/mcp` and no extra setup. A few need one-time configuration first:

**Google services (Gmail, Google Calendar, Google Drive)** — these use Google's own MCP servers and require an OAuth client from your org's Google Cloud project before the `/mcp` sign-in will complete:

```sh
# Create an OAuth 2.0 client in Google Cloud Console (Desktop app type), then:
claude mcp add --transport http --client-id <client-id> --client-secret <client-secret> Gmail https://gmailmcp.googleapis.com/mcp/v1
claude mcp add --transport http --client-id <client-id> --client-secret <client-secret> "Google Calendar" https://calendarmcp.googleapis.com/mcp/v1
claude mcp add --transport http --client-id <client-id> --client-secret <client-secret> "Google Drive" https://drivemcp.googleapis.com/mcp/v1
```

Then run `/mcp` to complete sign-in. All three can share the same OAuth client if you add the three scopes (`gmail.readonly`, `calendar.readonly`, `drive.readonly`) to it.

**Microsoft 365 (Outlook, Teams, OneDrive, SharePoint)** — needs a one-time Entra admin consent for the MCP app in your organization's tenant, then sign in with `/mcp` as usual.

**GitHub** — no connector or OAuth app needed: the local `gh` CLI is the recommended path:

```sh
gh auth login --scopes 'repo'
```

Or use `GITHUB_PERSONAL_ACCESS_TOKEN` if you prefer the connector.

## Scheduling

Syncs are scheduled via system cron running `claude -p`. No dependency on any Claude app being open.

```cron
CRON_TZ=America/Los_Angeles
52 17 * * 1-5  cd <dir> && claude -p "$(cat peernotes-meeting-notes.txt)"    >> peernotes-meeting-notes.log 2>&1
52 7  * * *    cd <dir> && claude -p "$(cat peernotes-github-summaries.txt)" >> peernotes-github-summaries.log 2>&1
52 0  * * *    cd <dir> && claude -p "$(cat peernotes-doc-sync.txt)"         >> peernotes-doc-sync.log 2>&1
```

`peernotes-team-setup` generates the prompt files and the cron entries. Prerequisites: `/mcp` sign-ins and `gh`/`git` logins must be in place for the user running the job (test with a manual `claude -p` run first).
