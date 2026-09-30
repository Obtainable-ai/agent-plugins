# Obtainable agent plugins

Plugins for Obtainable's products, for coding and work agents. Claude and Codex plugins live side by side in this repository but are built and published separately; they don't share files.

## Plugins

| Plugin | Agent | Product | Description |
|--------|-------|---------|-------------|
| [`peernotes`](./claude/plugins/peernotes) | Claude Code, Cowork | [Peernotes](https://peernotes.io) | Keeps a team's Peernotes workspace filled with meeting notes, daily GitHub code summaries and documents, and lets you search and manage Peernotes content from Claude. |

Codex plugins: none yet. See [codex/README.md](./codex/README.md).

## Repository layout

```text
.claude-plugin/marketplace.json   Claude marketplace (must be at the repo root)
.agents/plugins/marketplace.json  Codex marketplace (added with the first Codex plugin)
claude/plugins/<name>/            Claude plugins
codex/plugins/<name>/             Codex plugins
.github/workflows/validate.yml    Validates the marketplaces and every plugin
```

Both agents clone the whole repository when a marketplace is added, so keep it small and don't use Git LFS.

## Claude

### Install (Claude Code)

Add the marketplace once:

```bash
claude plugin marketplace add obtainable-ai/agent-plugins
```

Then install any plugin as `<plugin>@obtainable`:

```bash
claude plugin install peernotes@obtainable
```

Run `/mcp` to sign in to the plugin's servers. claude.ai connectors don't carry over to Claude Code, so each plugin includes its own servers in its `.mcp.json`. See each plugin's `CONNECTORS.md` for details.

### Company-wide rollout

An admin can register the marketplace and turn on plugins for everyone through managed settings (claude.ai admin → Claude Code → Managed settings, or MDM):

```json
{
  "extraKnownMarketplaces": {
    "obtainable": {
      "source": { "source": "github", "repo": "obtainable-ai/agent-plugins" }
    }
  },
  "enabledPlugins": {
    "peernotes@obtainable": true
  }
}
```

To distribute through claude.ai Organization settings → Plugins & skills instead, the repository must be private or internal on GitHub.

### Adding a Claude plugin

1. Create `claude/plugins/<name>/` with a `.claude-plugin/plugin.json` whose `name` matches the folder. Give it a `version`, `description` and `author`.
2. Add an entry to `.claude-plugin/marketplace.json` with `"source": "./claude/plugins/<name>"`.
3. Add a row to the Plugins table above.
4. Validate:

   ```bash
   claude plugin validate --strict .
   ```

   ```bash
   claude plugin validate --strict ./claude/plugins/<name>
   ```

To keep a plugin working in both Claude Code and Cowork, stick to skills, commands and remote HTTP MCP servers (`"type": "http"`). Don't add a `bin/` folder, hooks or monitors: Cowork and claude.ai won't install a plugin with `bin/`.

Bump `version` in the plugin's `plugin.json` with every change. Installed copies stay on their current version until it changes.

### Scheduling syncs

Some plugins, such as Peernotes, run syncs on a schedule:

- **Cowork, or the Claude desktop app's Code tab:** use scheduled tasks. The Peernotes `peernotes-team-setup` skill creates them for you.
- **Claude Code CLI:** run a skill unattended from cron on a machine that has `git` and `gh` logins:

  ```bash
  claude -p "/peernotes:github-summaries-to-peernotes"
  ```

  Cloud routines (`/schedule`) can only reach connectors. They can't use local `git` or `gh` logins.

## Codex

See [codex/README.md](./codex/README.md) for how Codex plugins will be added. Codex adds this repository with:

```bash
codex plugin marketplace add obtainable-ai/agent-plugins
```
