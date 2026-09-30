# Local clone and diff

How to use a local clone to see what the code actually changed in the period. Run every command in a shell, one repo at a time. `<owner>/<repo>`, `<branch>` (the default branch, from the connector or `git remote show origin`), `<start>`/`<end>` (YYYY-MM-DD) and `<tz>` (the admin's IANA timezone, e.g. `America/Los_Angeles`) are placeholders.

## 1. Clone (treeless of file contents)

```bash
WORK="$(mktemp -d ./gh-digest-XXXX)"
git clone --quiet --filter=blob:none --no-checkout --single-branch --branch <branch> \
  https://github.com/<owner>/<repo>.git "$WORK/repo"
cd "$WORK/repo"
```

- `--filter=blob:none` downloads commits and trees but fetches file contents only when a diff needs them; `--no-checkout` skips writing a working tree. Don't use `--depth`: the base commit sits before the period.
- Give the clone a 3-minute limit (`timeout 180`). On failure, record the reason (`auth`, `not found`, `timeout`, `network`) and move to the connector-only path.
- Private repos clone only if the shell's git already has credentials for github.com. Don't configure any: never write tokens to URLs, git config, files or the environment.
- If the repo has no commits, skip 2a for it.

## 2. Resolve the period

Interpret dates in the admin's timezone. `--since`/`--until` are inclusive.

```bash
export TZ=<tz>
END=$(git rev-list -1 --first-parent --before="<end> 23:59:59" HEAD)
BASE=$(git rev-list -1 --first-parent --before="<start> 00:00:00" HEAD)
[ -z "$BASE" ] && BASE=4b825dc642cb6eb9a060e54bf8d69288fbee4904   # empty tree: repo is newer than the period
```

If `END` is empty or `BASE = END`, the default branch didn't change in the period: skip 2a (the repo may still have PR/issue activity).

## 3. Commit list

```bash
git log --first-parent --since="<start> 00:00:00" --until="<end> 23:59:59" \
  --format='%H%x09%an%x09%ad%x09%s' --date=short HEAD
```

- Read PR numbers from `Merge pull request #<n>` (merge commits) and a trailing `(#<n>)` (squash merges). Commits with neither are **direct commits**.
- Group bot authors (`dependabot`, `renovate`, `github-actions`) into one line.
- Per-PR change: `git diff --numstat <sha>^1 <sha>` for a merge or squash commit (the first parent is the branch before it). Skip if the commit is a root commit.

## 4. Whole-period change

Use the same exclusions for every diff command:

```bash
EXCL=(':(exclude,glob)**/*.lock' ':(exclude,glob)**/package-lock.json' ':(exclude,glob)**/pnpm-lock.yaml'
      ':(exclude,glob)**/yarn.lock' ':(exclude,glob)**/go.sum' ':(exclude,glob)**/poetry.lock' ':(exclude,glob)**/Cargo.lock'
      ':(exclude,glob)**/*.min.*' ':(exclude,glob)**/*.map' ':(exclude,glob)**/dist/**' ':(exclude,glob)**/build/**'
      ':(exclude,glob)**/vendor/**' ':(exclude,glob)**/node_modules/**' ':(exclude,glob)**/*.snap'
      ':(exclude,glob)**/.env*' ':(exclude,glob)**/*.pem' ':(exclude,glob)**/*.key' ':(exclude,glob)**/*secret*'
      ':(exclude,glob)**/*credential*')

git diff --numstat --find-renames $BASE $END -- . "${EXCL[@]}"        # per-file +/−, renames
git diff --dirstat=files,3 $BASE $END -- . "${EXCL[@]}"               # hotspots by directory
git diff --summary --find-renames $BASE $END -- . "${EXCL[@]}"        # created / deleted / renamed / mode changes
```

Stats line: sum `--numstat` (binary files show `-`; count them as files changed only). Report excluded lock/generated changes as a single "dependency/lockfile updates" mention, not in the totals.

## 5. Read hunks selectively

Pick up to **15 files per repo**, in this order: migrations and schema; auth, security, permissions, payments; public APIs, routes, CLI and exported interfaces; new files/modules; config and CI/deploy; then the largest remaining source changes. Skip tests unless a test file is the only signal for a change.

```bash
git diff --find-renames --unified=3 $BASE $END -- <path> | head -n 400
```

- At most **400 lines per file** and **3,000 lines per repo** in total. For a file over the limit, use its `--numstat` line and the first hunks only.
- Take away *what the code now does*: new or removed functions, classes, endpoints, tables, flags, dependencies and behaviour changes. Name identifiers; never copy hunks or code into the digest.
- If a hunk contains something that looks like a secret (tokens, keys, passwords, connection strings), stop reading that file, don't repeat the value anywhere, and add "possible secret committed in `<path>`" under Risks & follow-ups.

## 6. Clean up

```bash
cd - >/dev/null && rm -rf "$WORK"
```

Always remove the clone, including after a failure.

## Risk signals from the diff

Add to Risks & follow-ups: reverts (`Revert "…"`); force-pushed or rewritten history (a period commit missing from the branch); a single change over 1,000 lines; migrations without a matching rollback; deleted tests; new dependencies; edits to CI/deploy, auth or permissions; and PRs whose diff touches areas their description doesn't mention.
