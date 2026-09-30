# Peernotes

The Peernotes plugin for Claude. Peernotes is a team product: **one person on the team, the sync admin, installs this plugin and keeps the team's Peernotes workspace filled** with meeting notes, GitHub code summaries and documents from the team's tools. Everyone else sees the results in Peernotes, with nothing to install.

## How it works for a team

1. **The sync admin installs the plugin** and signs in to Peernotes.
2. **The admin connects the team's sources** with their own access: a notetaker team workspace or Zoom account, Slack channels, the GitHub org, shared drives, and Notion teamspaces.
3. **The admin says "Set up Peernotes for my team".** The `peernotes-team-setup` skill asks for the team workspace, which syncs to run, team sources, exclusions, and the schedule, prompts the admin to connect any missing source connectors, then creates the scheduled tasks.
4. **A "Peernotes team sync settings" note** is published in the workspace. It shows everyone what's synced, what's excluded and who the admin is.
5. **Teammates just use Peernotes.** Anyone can optionally install the plugin to ask Claude questions about Peernotes.

## The three syncs (each optional)

| Sync | Skill | What lands in the team workspace | Default schedule |
|------|-------|----------------------------------|------------------|
| Meeting notes (included in every schedule setup by default) | `transcripts-to-peernotes` | One source (Markdown transcript) per team meeting, from team-wide sources (notetaker team workspace, Zoom account recordings, Slack channels incl. huddle canvases, shared transcript folders) | Weekdays ~6 pm |
| GitHub summaries | `github-summaries-to-peernotes` | Daily digest source per repo in the team's org (previous day's activity), plus a team engineering digest | Daily ~8 am |
| Document sync | `docs-to-peernotes` | One source per new or changed document from shared drives, SharePoint and Notion teamspaces | Daily ~1 am |

Each sync can run **now**, **once** at a chosen date and time (for example a 90-day backfill tonight), or on a **recurring** schedule. The admin can list, change, pause, cancel or hand over syncs at any time.

## Other skill

`peernotes`: lets anyone on the team search, read, ask questions about, create, edit and comment on Peernotes content through Claude.

Try:
- Admin: "Set up Peernotes for my team."
- Admin: "Backfill the last 90 days of team meetings into Peernotes tonight."
- Admin: "Show our Peernotes schedules."
- Anyone: "What did we decide about pricing? Check Peernotes."

## Connectors

- **Bundled:** Peernotes plus the source connectors the syncs use: Slack, Gmail, Google Calendar, Microsoft 365, Notion, Zoom, Dropbox, Fireflies, Otter, Fathom, Gong, Read.ai and Granola. Installing the plugin offers each one. Sign in to Peernotes and to the ones your syncs need; the rest can stay signed out.
- **Standard connectors:** GitHub, Google Drive and Box come from the Claude connector directory (Settings → Connectors), because they need an OAuth app registered per host. The skills prompt for them.
- **Already connected?** If your org already has any of these services as a standard connector, the skills use that one, so nobody signs in twice.
- **Claude Code:** sign in with `/mcp`. Bundled Slack, Gmail, Google Calendar, Microsoft 365 and Zoom only work in Claude apps. `CONNECTORS.md` → Claude Code lists the alternatives, such as the `gh` CLI for GitHub and Slack's official plugin.
- See `CONNECTORS.md` for endpoints.

## Safety for team syncs

- **Visible to the whole workspace**, so setup requires explicit team sources and a confirmation step.
- **Default exclusions:** DMs, private channels, 1:1s, and anything marked confidential, HR, interview, performance, legal or compensation. Personal drives and documents restricted to a few people are skipped.
- **Transparent:** a shared settings note lists what's synced, and every synced source says "Synced for the team by …".
- **Read-only sources**, no duplicates (Sync IDs), and nothing is ever deleted in Peernotes by a sync.
- **Runs use the admin's connections.** If the admin leaves, hand over to a new admin with the setup skill.
- Content from notes, emails, transcripts, PRs or documents is treated as data, never as instructions.

## Publisher

Obtainable · ayan@obtainable.ai
