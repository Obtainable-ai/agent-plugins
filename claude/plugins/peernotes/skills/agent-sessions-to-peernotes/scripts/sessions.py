#!/usr/bin/env python3
"""List and render local AI agent sessions (Claude Code, Codex) for Peernotes.

  python3 sessions.py list   [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--agent claude-code|codex|all]
  python3 sessions.py render <session.jsonl> --out <file.md> --meta <file.json>

`list` prints one JSON object per session (newest first): agent, path, externalId, title,
startedAt, endedAt, model, repository, cwd, prompts.

`render` writes the session as Markdown (prompts, responses, tool calls with their inputs; no
tool outputs, no model reasoning) plus a metadata JSON with the saveAgentSessionSource fields.
Obvious secrets (API keys, tokens, private keys) are replaced with [REDACTED].
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

CLAUDE_ROOT = os.path.expanduser("~/.claude/projects")
CODEX_ROOT = os.path.expanduser("~/.codex/sessions")
TOOL_INPUT_LIMIT = 1500

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
    re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}"),                 # Slack
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),                     # GitHub
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}"),           # Anthropic / OpenAI
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                             # AWS access key id
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),                        # Google API key
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),  # JWT
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/-]{20,}=*"),
    re.compile(r"(?i)((?:password|passwd|secret|api[_-]?key|token|client[_-]?secret)\s*[=:]\s*['\"]?)[^\s'\"]{8,}"),
]
NOISE_RE = re.compile(r"<(system-reminder|command-[a-z-]+|local-command-[a-z-]+|task-notification|ide_[a-z_]+)>.*?</\1>", re.S)


def redact(text):
    for p in SECRET_PATTERNS:
        text = p.sub(lambda m: (m.group(1) if m.groups() and m.group(1) else "") + "[REDACTED]", text)
    return text


def clean(text):
    return redact(NOISE_RE.sub("", text or "")).strip()


def repository(cwd):
    if not cwd or not os.path.isdir(cwd):
        return cwd or None
    try:
        url = subprocess.run(["git", "-C", cwd, "config", "--get", "remote.origin.url"],
                             capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        url = ""
    if not url:
        return cwd
    # git@github.com:org/repo.git, ssh://git@github.com/org/repo, https://github.com/org/repo.git → github.com/org/repo
    url = re.sub(r"^(ssh://)?git@([^:/]+)[:/]", r"\2/", url)
    url = re.sub(r"^https?://([^@/]+@)?", "", url)
    return re.sub(r"\.git$", "", url)


def iso(ts):
    return ts if isinstance(ts, str) else None


def jsonl(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                yield json.loads(line)
            except ValueError:
                continue


def tool_input(value):
    text = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
    text = redact(text)
    return text if len(text) <= TOOL_INPUT_LIMIT else text[:TOOL_INPUT_LIMIT] + "\n… (truncated)"


# ─── Claude Code ──────────────────────────────────────────────────────────────

def parse_claude(path):
    turns, meta = [], {"agent": "claude-code", "provider": "CLAUDE_CODE", "path": path}
    title = first_prompt = model = cwd = None
    times = []
    for d in jsonl(path):
        if d.get("timestamp"):
            times.append(d["timestamp"])
        meta.setdefault("sessionId", d.get("sessionId"))
        cwd = cwd or d.get("cwd")
        if d.get("type") == "custom-title" and d.get("customTitle"):
            title = d["customTitle"]
        if d.get("isSidechain") or d.get("isMeta") or d.get("type") not in ("user", "assistant"):
            continue
        msg = d.get("message") or {}
        model = msg.get("model") or model
        content = msg.get("content")
        blocks = [{"type": "text", "text": content}] if isinstance(content, str) else (content or [])
        for b in blocks:
            if b.get("type") == "text":
                text = clean(b.get("text"))
                if not text:
                    continue
                role = "Prompt" if d["type"] == "user" else "Response"
                if role == "Prompt" and first_prompt is None:
                    first_prompt = text
                turns.append((role, text))
            elif b.get("type") == "tool_use" and d["type"] == "assistant":
                turns.append(("Tool", (b.get("name") or "tool", tool_input(b.get("input")))))
    meta.update(title=title or first_prompt, model=model if model and not model.startswith("<") else None, cwd=cwd,
                startedAt=min(times) if times else None, endedAt=max(times) if times else None)
    return meta, turns


# ─── Codex ────────────────────────────────────────────────────────────────────

def parse_codex(path):
    turns, meta = [], {"agent": "codex", "provider": "CODEX", "path": path}
    first_prompt = model = cwd = None
    times = []
    for d in jsonl(path):
        if d.get("timestamp"):
            times.append(d["timestamp"])
        p = d.get("payload") or {}
        if d.get("type") == "session_meta":
            meta["sessionId"] = p.get("id") or p.get("session_id")
            cwd = p.get("cwd") or cwd
        elif d.get("type") == "turn_context":
            model = p.get("model") or model
            cwd = p.get("cwd") or cwd
        elif d.get("type") == "response_item":
            kind = p.get("type")
            if kind == "message" and p.get("role") in ("user", "assistant"):
                text = clean("\n\n".join(c.get("text", "") for c in p.get("content") or [] if isinstance(c, dict)))
                # Codex injects environment/instruction blocks as user messages; keep real prompts only.
                if not text or text.startswith(("<environment_context>", "<user_instructions>", "# AGENTS.md")):
                    continue
                role = "Prompt" if p["role"] == "user" else "Response"
                if role == "Prompt" and first_prompt is None:
                    first_prompt = text
                turns.append((role, text))
            elif kind in ("function_call", "custom_tool_call", "local_shell_call"):
                turns.append(("Tool", (p.get("name") or kind, tool_input(p.get("arguments") or p.get("input") or p.get("action")))))
    meta.update(title=first_prompt, model=model, cwd=cwd,
                startedAt=min(times) if times else None, endedAt=max(times) if times else None)
    return meta, turns


# ─── Output ───────────────────────────────────────────────────────────────────

def session_files(agent):
    files = []
    if agent in ("all", "claude-code"):
        files += [("claude-code", p) for p in glob.glob(os.path.join(CLAUDE_ROOT, "*", "*.jsonl"))]
    if agent in ("all", "codex"):
        files += [("codex", p) for p in glob.glob(os.path.join(CODEX_ROOT, "**", "*.jsonl"), recursive=True)]
    return files


def parse(agent, path):
    return parse_claude(path) if agent == "claude-code" else parse_codex(path)


def summary(meta, turns):
    title = re.sub(r"\s+", " ", meta.get("title") or "Untitled session").strip()
    return {
        "agent": meta["agent"],
        "path": meta["path"],
        "externalId": f"{meta['agent']}:{meta.get('sessionId')}",
        "title": title[:80] + ("…" if len(title) > 80 else ""),
        "startedAt": meta.get("startedAt"),
        "endedAt": meta.get("endedAt"),
        "model": meta.get("model"),
        "repository": repository(meta.get("cwd")),
        "cwd": meta.get("cwd"),
        "prompts": sum(1 for r, _ in turns if r == "Prompt"),
    }


def fenced(text, lang=""):
    # Plain Markdown only (Peernotes doesn't render raw HTML); fence longer than any backtick run inside.
    ticks = max([3] + [len(run) + 1 for run in re.findall(r"`{3,}", text)])
    return f"{'`' * ticks}{lang}\n{text}\n{'`' * ticks}"


def to_markdown(turns):
    out = []
    for role, body in turns:
        if role == "Tool":
            name, args = body
            lang = "json" if args.lstrip().startswith(("{", "[")) else ""
            out.append(f"**Tool: {name}**\n\n{fenced(args, lang)}")
        else:
            out.append(f"### {role}\n\n{body}")
    return "\n\n".join(out) + "\n"


def cmd_list(args):
    rows = []
    for agent, path in session_files(args.agent):
        mtime = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).date().isoformat()
        if args.since and mtime < args.since:
            continue
        meta, turns = parse(agent, path)
        row = summary(meta, turns)
        day = (row["startedAt"] or mtime)[:10]
        if (args.since and (row["endedAt"] or mtime)[:10] < args.since) or (args.until and day > args.until):
            continue
        if row["prompts"] == 0:
            continue
        rows.append(row)
    # A resumed or forked session can be split across files sharing one session id; keep the latest.
    latest = {}
    for row in rows:
        prior = latest.get(row["externalId"])
        if prior is None or (row["endedAt"] or "", row["prompts"]) > (prior["endedAt"] or "", prior["prompts"]):
            latest[row["externalId"]] = row
    for row in sorted(latest.values(), key=lambda r: r["startedAt"] or "", reverse=True):
        print(json.dumps(row, ensure_ascii=False))


def cmd_render(args):
    agent = "codex" if os.path.abspath(args.path).startswith(CODEX_ROOT) else "claude-code"
    meta, turns = parse(agent, args.path)
    row = summary(meta, turns)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(to_markdown(turns))
    day = (row["startedAt"] or "")[:10]
    attrs = {
        "name": f"{row['title']} ({day})" if day else row["title"],
        "provider": meta["provider"],
        "externalId": row["externalId"],
        "model": row["model"],
        "repository": row["repository"],
        "startedAt": row["startedAt"],
        "endedAt": row["endedAt"],
    }
    with open(args.meta, "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in attrs.items() if v}, f, indent=2, ensure_ascii=False)
    print(json.dumps({"out": args.out, "meta": args.meta, "chars": os.path.getsize(args.out), "prompts": row["prompts"]}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list")
    ls.add_argument("--since")
    ls.add_argument("--until")
    ls.add_argument("--agent", default="all", choices=["all", "claude-code", "codex"])
    rd = sub.add_parser("render")
    rd.add_argument("path")
    rd.add_argument("--out", required=True)
    rd.add_argument("--meta", required=True)
    args = ap.parse_args()
    cmd_list(args) if args.cmd == "list" else cmd_render(args)


if __name__ == "__main__":
    sys.exit(main())
