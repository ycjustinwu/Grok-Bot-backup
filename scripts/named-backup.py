#!/usr/bin/env python3
"""Incremental named-bot backup helper for memory-manager.

Cost rule: never fan-out the fleet. Justin (or 记忆管家) names bots;
this script only touches those rows + optional local skills sync.

Typical flow:
  1) python3 scripts/named-backup.py --bots second-brain --request
     → 记忆管家 SendToAgent each target the printed dump brief
  2) after dumps land under /workspace/<uuid>-memory-backup.md:
     python3 scripts/named-backup.py --bots second-brain --ingest --profiles --skip-unchanged --commit --push
  3) optional skills (local only, no SendToAgent):
     python3 scripts/named-backup.py --skills --commit --push

Exit codes:
  0 ok
  1 usage / unknown bot / secret scan fail
  2 named bots still waiting on dumps (ingest)
  3 git/push failure
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.md"
BOTS_DIR = ROOT / "bots"
SKILLS_DIR = ROOT / "skills"
WORKFLOWS = Path("/home/box/agent-data/workflows")
AGENTS = Path("/home/box/agent-data/agents")
DUMP_GLOB = Path("/workspace")
HKT = ZoneInfo("Asia/Hong_Kong")

SECRET_RE = re.compile(
    r"(?i)(?<!\[REDACTED:)"
    r"(?:api[_-]?key|secret|password|token|bearer|authorization)"
    r"|sk-[A-Za-z0-9]{16,}"
    r"|ghp_[A-Za-z0-9]{20,}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,}"
)

ROW_RE = re.compile(
    r"^\|\s*(?P<slug>[a-z0-9-]+)\s*\|\s*(?P<name>[^|]+?)\s*\|\s*"
    r"(?P<id>[0-9a-f-]{36})\s*\|\s*(?P<opt_in>[^|]+?)\s*\|\s*(?P<notes>.*?)\s*\|$"
)


def today_hkt() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d")


def load_registry() -> list[dict]:
    rows = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        d = m.groupdict()
        d["name"] = d["name"].strip()
        d["opt_in"] = d["opt_in"].strip()
        d["notes"] = d["notes"].strip()
        rows.append(d)
    return rows


def resolve_bots(selectors: list[str], rows: list[dict]) -> list[dict]:
    by_slug = {r["slug"]: r for r in rows}
    by_id = {r["id"]: r for r in rows}
    by_name = {r["name"].casefold(): r for r in rows}
    out: list[dict] = []
    seen = set()
    unknown = []
    for raw in selectors:
        key = raw.strip()
        if not key:
            continue
        hit = (
            by_slug.get(key)
            or by_id.get(key)
            or by_name.get(key.casefold())
        )
        if not hit:
            # partial name contains
            cands = [r for r in rows if key.casefold() in r["name"].casefold() or key.casefold() in r["slug"]]
            if len(cands) == 1:
                hit = cands[0]
            else:
                unknown.append(key)
                continue
        if hit["id"] in seen:
            continue
        seen.add(hit["id"])
        out.append(hit)
    if unknown:
        print("Unknown bot selectors:", ", ".join(unknown), file=sys.stderr)
        print("Use --list to see slug / name / id.", file=sys.stderr)
        sys.exit(1)
    return out


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def secret_scan(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if "[REDACTED:" in line:
            # still flag if an obvious live token sits beside placeholder
            if re.search(r"sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}", line):
                hits.append(f"{path}:{i}: suspicious token beside redaction")
            continue
        if SECRET_RE.search(line) and re.search(
            r"(?i)(sk-|ghp_|xox[baprs]-|['\"][A-Za-z0-9_\-]{24,}['\"]|=\\s*[^\\s\\[]{16,})",
            line,
        ):
            hits.append(f"{path}:{i}: {line.strip()[:120]}")
    return hits


def dump_path(bot_id: str) -> Path:
    return DUMP_GLOB / f"{bot_id}-memory-backup.md"


def print_list(rows: list[dict]) -> None:
    print(f"{'slug':28} {'纳入':4} id                                   name")
    for r in rows:
        print(f"{r['slug']:28} {r['opt_in']:4} {r['id']}  {r['name']}")


def request_messages(bots: list[dict]) -> None:
    print("# SendToAgent dump requests (named bots only — do NOT fleet fan-out)")
    print("# priority: true while waiting for dump; after receipt ACK priority: false")
    print()
    for b in bots:
        path = dump_path(b["id"])
        print(f"## {b['slug']} / {b['name']} / {b['id']}")
        print(f"target_id: {b['id']}")
        print("message:")
        print(
            f"记忆管家 named backup（增量，非全艦隊）。請把 durable memory 完整 dump 寫到 "
            f"`{path}`（整份覆蓋該檔即可）。必含：Identity／ONE JOB／ANTI-JOBS／partners；"
            f"locked rules；live snapshot（routines／最近狀態）；secrets 只許 `[REDACTED:name]`；"
            f"pending confirms 只列不執行。寫完用 SendToAgent 回 记忆管家 path＋行數＋md5，priority false。"
            f"不要重問確認、不要叫醒其他 Bot。"
        )
        print()


def refresh_profile(bot: dict, dry: bool) -> list[str]:
    changed: list[str] = []
    agent_dir = AGENTS / bot["id"]
    dest = BOTS_DIR / bot["slug"]
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "archive").mkdir(exist_ok=True)

    profile_src = agent_dir / "profile.json"
    settings_src = agent_dir / "settings.json"
    if not profile_src.exists():
        print(f"! {bot['slug']}: no disk profile at {profile_src}")
        return changed

    profile = json.loads(profile_src.read_text(encoding="utf-8"))
    settings = {}
    if settings_src.exists():
        settings = json.loads(settings_src.read_text(encoding="utf-8"))

    profile_md = dest / "profile.md"
    agent_spec = dest / "agent-spec.md"
    body_profile = (
        f"# {bot['name']} — profile\n\n"
        f"- slug: `{bot['slug']}`\n"
        f"- id: `{bot['id']}`\n"
        f"- name: {profile.get('name', bot['name'])}\n"
        f"- title: {profile.get('title', '')}\n"
        f"- description: {profile.get('description', '')}\n"
        f"- refreshed: {datetime.now(HKT).isoformat()}\n"
    )
    body_spec = (
        f"# {bot['name']} — agent-spec\n\n"
        f"- id: `{bot['id']}`\n"
        f"- slug: `{bot['slug']}`\n"
        f"- 纳入: {bot['opt_in']}\n"
        f"- notes: {bot['notes']}\n"
        f"- settings_keys: {', '.join(sorted(settings.keys())) if settings else '(none)'}\n"
        f"- source: `{profile_src}`\n"
        f"- refreshed: {datetime.now(HKT).isoformat()}\n"
    )

    for path, body in ((profile_md, body_profile), (agent_spec, body_spec)):
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == body:
            continue
        print(f"{'DRY ' if dry else ''}write {path.relative_to(ROOT)}")
        if not dry:
            path.write_text(body, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))
    return changed


def ingest_bot(bot: dict, date: str, skip_unchanged: bool, dry: bool) -> str:
    """Return status: ingested|unchanged|missing|secret_fail"""
    src = dump_path(bot["id"])
    dest_dir = BOTS_DIR / bot["slug"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "archive").mkdir(exist_ok=True)
    dest = dest_dir / "MEMORY.md"

    if not src.exists():
        print(f"WAIT {bot['slug']}: missing dump {src}")
        return "missing"

    hits = secret_scan(src)
    if hits:
        print(f"SECRET FAIL {bot['slug']}:")
        for h in hits[:20]:
            print(" ", h)
        return "secret_fail"

    new_hash = md5_file(src)
    if skip_unchanged and dest.exists() and md5_file(dest) == new_hash:
        print(f"SKIP {bot['slug']}: md5 {new_hash} matches MEMORY.md")
        return "unchanged"

    archive = dest_dir / "archive" / f"{date}.md"
    if dest.exists():
        print(f"{'DRY ' if dry else ''}archive {dest.relative_to(ROOT)} → {archive.relative_to(ROOT)}")
        if not dry:
            if archive.exists():
                # keep prior archive; stamp collision with time
                archive = dest_dir / "archive" / f"{date}-{datetime.now(HKT).strftime('%H%M%S')}.md"
            shutil.copy2(dest, archive)

    print(f"{'DRY ' if dry else ''}ingest {src.name} → {dest.relative_to(ROOT)} (md5 {new_hash})")
    if not dry:
        shutil.copy2(src, dest)
    return "ingested"


def sync_skills(dry: bool) -> list[str]:
    """Copy only workflow folders whose tree hash differs. Skip no-SKILL.md."""
    if not WORKFLOWS.is_dir():
        print("No workflows dir", file=sys.stderr)
        return []

    changed: list[str] = []
    index_lines = [
        "# User-created skills index",
        f"",
        f"Generated: {datetime.now(HKT).isoformat()} (Asia/Hong_Kong)",
        f"Source: `{WORKFLOWS}`",
        f"",
        "| slug | has SKILL.md | notes |",
        "|------|--------------|-------|",
    ]
    used = []
    for folder in sorted(p for p in WORKFLOWS.iterdir() if p.is_dir()):
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            print(f"skip skill (no SKILL.md): {folder.name}")
            continue
        used.append(folder.name)
        dest = SKILLS_DIR / folder.name
        src_hash = tree_hash(folder)
        dst_hash = tree_hash(dest) if dest.exists() else None
        note = "unchanged"
        if src_hash != dst_hash:
            note = "updated" if dst_hash else "new"
            print(f"{'DRY ' if dry else ''}skills {note}: {folder.name}")
            if not dry:
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(
                    folder,
                    dest,
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "node_modules", ".git", ".cache", "*.pyc"
                    ),
                )
            changed.append(f"skills/{folder.name}")
        index_lines.append(f"| {folder.name} | yes | {note} |")

    index_lines.append("")
    index_lines.append(f"Count: {len(used)}")
    index_body = "\n".join(index_lines) + "\n"
    index_path = SKILLS_DIR / "INDEX.md"
    old = index_path.read_text(encoding="utf-8") if index_path.exists() else None
    if old != index_body:
        print(f"{'DRY ' if dry else ''}write skills/INDEX.md")
        if not dry:
            SKILLS_DIR.mkdir(exist_ok=True)
            index_path.write_text(index_body, encoding="utf-8")
        changed.append("skills/INDEX.md")
    return changed


def tree_hash(root: Path) -> str:
    h = hashlib.md5()
    if not root.exists():
        return ""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in {"__pycache__", "node_modules", ".git", ".cache"}
        ]
        for name in filenames:
            if name.endswith(".pyc"):
                continue
            files.append(Path(dirpath) / name)
    for path in sorted(files, key=lambda p: str(p.relative_to(root))):
        rel = str(path.relative_to(root)).encode()
        h.update(rel)
        h.update(b"\0")
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest()


def append_changelog(bots: list[dict], skills_changed: list[str], dry: bool) -> None:
    date = today_hkt()
    lines = [f"## {date} named incremental backup", ""]
    if bots:
        lines.append(
            "- Bots: " + ", ".join(f"`{b['slug']}`" for b in bots) + " (named only; no fleet fan-out)."
        )
    if skills_changed:
        lines.append(
            "- Skills touched: "
            + ", ".join(f"`{s}`" for s in skills_changed[:30])
            + ("…" if len(skills_changed) > 30 else "")
        )
    if not bots and not skills_changed:
        return
    lines.append("- Mode: named / incremental (cost gate).")
    lines.append("")
    block = "\n".join(lines) + "\n"
    path = ROOT / "CHANGELOG.md"
    old = path.read_text(encoding="utf-8") if path.exists() else "# Changelog\n\n"
    if block.strip() in old:
        return
    # insert after title
    if old.startswith("# Changelog"):
        parts = old.split("\n", 2)
        new = parts[0] + "\n\n" + block + (parts[2] if len(parts) > 2 else "")
    else:
        new = block + old
    print(f"{'DRY ' if dry else ''}update CHANGELOG.md")
    if not dry:
        path.write_text(new, encoding="utf-8")


def git_commit_push(paths: list[str], message: str, do_push: bool, dry: bool) -> None:
    if dry:
        print(f"DRY commit: {message}")
        print("DRY paths:", ", ".join(paths) or "(none)")
        return
    if not paths:
        print("Nothing to commit.")
        return
    def run(cmd: list[str]) -> None:
        print("+", " ".join(cmd))
        subprocess.check_call(cmd, cwd=ROOT)

    run(["git", "add", "--"] + paths)
    # also changelog if updated
    if (ROOT / "CHANGELOG.md").exists():
        run(["git", "add", "CHANGELOG.md"])
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True
    ).strip()
    if not staged:
        print("Nothing staged after add.")
        return
    run(
        [
            "git",
            "-c",
            "user.email=memory-manager@local",
            "-c",
            "user.name=记忆管家",
            "commit",
            "-m",
            message,
        ]
    )
    if do_push:
        # one-shot gh helper; no global config change
        run(
            [
                "git",
                "-c",
                "credential.helper=!/usr/local/bin/gh auth git-credential",
                "push",
                "origin",
                "HEAD",
            ]
        )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Named-bot incremental backup (no fleet fan-out)."
    )
    ap.add_argument(
        "--bots",
        nargs="+",
        default=[],
        help="Bot selectors: slug, exact name, or uuid. Required unless --skills/--list only.",
    )
    ap.add_argument("--list", action="store_true", help="List registry and exit.")
    ap.add_argument(
        "--request",
        action="store_true",
        help="Print SendToAgent dump request text for named bots.",
    )
    ap.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest /workspace/<id>-memory-backup.md for named bots.",
    )
    ap.add_argument(
        "--profiles",
        action="store_true",
        help="Refresh profile.md / agent-spec.md from disk for named bots.",
    )
    ap.add_argument(
        "--skills",
        action="store_true",
        help="Local incremental skills sync (hash compare). No SendToAgent.",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Ingest even when dump md5 already matches MEMORY.md (default: skip unchanged).",
    )
    ap.add_argument("--date", default=None, help="Archive stamp YYYY-MM-DD (default today HKT).")
    ap.add_argument("--commit", action="store_true", help="git commit changed paths.")
    ap.add_argument("--push", action="store_true", help="git push after commit.")
    ap.add_argument("--dry-run", action="store_true", help="Print actions only.")
    args = ap.parse_args()

    rows = load_registry()
    if args.list:
        print_list(rows)
        return

    skip_unchanged = not args.force
    date = args.date or today_hkt()
    dry = args.dry_run
    bots: list[dict] = []
    if args.bots:
        bots = resolve_bots(args.bots, rows)
        not_in = [b for b in bots if b["opt_in"] != "是"]
        if not_in:
            print(
                "Refusing bots with 纳入≠是:",
                ", ".join(b["slug"] for b in not_in),
                file=sys.stderr,
            )
            sys.exit(1)
    elif not args.skills:
        ap.error("Name bots with --bots …, or pass --skills / --list.")

    if args.request:
        if not bots:
            ap.error("--request needs --bots")
        request_messages(bots)
        return

    if not (args.ingest or args.profiles or args.skills or args.commit or args.push):
        # default helpful plan
        print("Plan (no action). Named bots:" if bots else "Plan (skills-only possible).")
        for b in bots:
            src = dump_path(b["id"])
            mem = BOTS_DIR / b["slug"] / "MEMORY.md"
            status = "dump-ready" if src.exists() else "need-request"
            same = ""
            if src.exists() and mem.exists() and md5_file(src) == md5_file(mem):
                same = " (md5 already matches MEMORY.md)"
            print(f"  - {b['slug']}: {status}{same} → {src}")
        print(
            "Next: --request  → SendToAgent; then --ingest --profiles --skip-unchanged --commit --push"
        )
        print("Optional: --skills for local skill hash sync.")
        return

    changed_paths: list[str] = []
    statuses: dict[str, str] = {}

    if args.profiles:
        if not bots:
            ap.error("--profiles needs --bots")
        for b in bots:
            changed_paths.extend(refresh_profile(b, dry))

    if args.ingest:
        if not bots:
            ap.error("--ingest needs --bots")
        missing = 0
        secret_fail = 0
        for b in bots:
            st = ingest_bot(b, date, skip_unchanged, dry)
            statuses[b["slug"]] = st
            if st == "ingested":
                changed_paths.append(f"bots/{b['slug']}/MEMORY.md")
                changed_paths.append(f"bots/{b['slug']}/archive")
            elif st == "missing":
                missing += 1
            elif st == "secret_fail":
                secret_fail += 1
        if secret_fail:
            sys.exit(1)
        if missing:
            print(
                f"{missing} bot(s) still waiting on dumps — request them, then re-run --ingest.",
                file=sys.stderr,
            )
            # still allow partial commit of what we have unless all missing
            if missing == len(bots) and not args.profiles and not args.skills:
                sys.exit(2)

    skills_changed: list[str] = []
    if args.skills:
        skills_changed = sync_skills(dry)
        changed_paths.extend(skills_changed)

    if (args.ingest or args.skills or args.profiles) and (changed_paths or statuses):
        append_changelog(bots if (args.ingest or args.profiles) else [], skills_changed, dry)

    if args.commit or args.push:
        # unique preserve order
        uniq = list(dict.fromkeys(changed_paths))
        # expand archive dirs to actual files via git add -A pathspecs we already listed
        msg_bots = ",".join(b["slug"] for b in bots) or "skills"
        message = f"named incremental backup {date}: {msg_bots}"
        try:
            git_commit_push(uniq, message, do_push=args.push, dry=dry)
        except subprocess.CalledProcessError as e:
            print(f"git failed: {e}", file=sys.stderr)
            sys.exit(3)

    # summary
    if statuses:
        print("Ingest summary:")
        for slug, st in statuses.items():
            print(f"  {slug}: {st}")


if __name__ == "__main__":
    main()
