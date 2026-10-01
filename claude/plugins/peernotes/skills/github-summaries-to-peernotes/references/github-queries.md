# GitHub queries for code summaries

Replace `<start>`/`<end>` with ISO dates (YYYY-MM-DD).

## Finding repos (default scope)

- `search_repositories` / list repos for the authenticated user and their orgs, then keep those with `pushed:>=<start>`.
- Or search PRs involving the user: `is:pr involves:@me updated:>=<start>` and take the distinct repos.
- Cap at 10 repos per run unless the prompt lists repos explicitly; mention any skipped.

## Search queries

| Need | Query |
|------|-------|
| Merged PRs | `repo:<owner>/<repo> is:pr is:merged merged:<start>..<end>` |
| Open PRs with activity | `repo:<owner>/<repo> is:pr is:open updated:<start>..<end>` |
| Awaiting review | `repo:<owner>/<repo> is:pr is:open review:required` |
| Closed issues | `repo:<owner>/<repo> is:issue is:closed closed:<start>..<end>` |
| New issues | `repo:<owner>/<repo> is:issue created:<start>..<end>` |

## Commits

Take the commit list and file changes from the local clone (`references/local-diff.md`). Use the connector below only when the clone failed for that repo; then take PR size from `pull_request_read` file stats instead of the diff.

Fallback: `list_commits` on the default branch with `since=<start>T00:00:00Z` and `until=<end>T23:59:59Z`. Drop commits whose SHA belongs to a merged PR (squash/merge commits reference `(#<n>)` in the message). Group bot commits (dependabot, renovate) into one line: "N dependency updates".

## Releases

`list_releases`; keep those with `published_at` in the period. Use the release notes body for the summary.

## Theming merged PRs

Classify by labels first, then conventional-commit prefixes in titles:

| Theme | Signals |
|-------|---------|
| Features | `feat`, `feature`, `enhancement` |
| Fixes | `fix`, `bug`, `hotfix` |
| Refactors | `refactor`, `chore`, `cleanup` |
| Infra & deps | `ci`, `build`, `deps`, `infra`, dependabot/renovate |
| Docs | `docs` |

Flag as risk: reverts, PRs merged without approving review, very large PRs (>1,000 lines changed), changes to auth/security/migrations paths.

