# Codex plugins

No Codex plugins yet. Codex plugins are built separately from the Claude plugins in `../claude/`; they don't share files.

When the first one is added:

1. Create `codex/plugins/<name>/` with a `plugin.json` at its root, plus `skills/` and `mcp.json` as needed. See [Build plugins](https://developers.openai.com/codex/plugins/build/).
2. Create the Codex marketplace at the repo root, `.agents/plugins/marketplace.json`. Codex only reads it there. Point each entry at the plugin folder:

   ```json
   {
     "name": "obtainable",
     "interface": { "displayName": "Obtainable" },
     "plugins": [
       {
         "name": "<name>",
         "source": { "source": "local", "path": "./codex/plugins/<name>" },
         "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
         "category": "Productivity"
       }
     ]
   }
   ```

3. Add a Codex job to `.github/workflows/validate.yml`.

Codex can also read `.claude-plugin/marketplace.json`, which lists the Claude plugins. Check that Codex picks up `.agents/plugins/marketplace.json` rather than the Claude one, so Claude plugins don't appear in Codex.
