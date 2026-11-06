#!/usr/bin/env python3
"""Incremental named-bot backup helper for memory-manager.

Cost rule: never fan-out the fleet. Justin names bots; only those + optional
local skills sync are touched.

Versioning / file management:
  - bots/<slug>/MEMORY.md          current snapshot (whole-file replace)
  - bots/<slug>/archive/<stamp>.md prior versions (never overwritten)
  - bots/<slug>/VERSIONS.md        append-only version index (md5, lines, stamp)
  - meta/backup-runs/<run-id>.md   per-run log
  - CHANGELOG.md                   human summary (newest first)
  - optional git tag backup-named-<run-id> or backup-<slug>-<date>

Typical flow:
  python3 scripts/named-backup.py --bots second-brain --request
  python3 scripts/named-backup.py --bots second-brain --ingest --profiles --tag --commit --push
  python3 scripts/named-backup.py --skills --commit --push
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
RUNS_DIR = ROOT / "meta" / "backup-runs"
WORKFLOWS = Path("/home/box/agent-data/workflows")
AGENTS = Path("/home/box/agent-data/agents")
DUMP_ROOT = Path("/workspace")
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


def now_hkt() -> datetime:
    return datetime.now(HKT)


def today_hkt() -> str:
    return now_hkt().strftime("%Y-%m-%d")


def run_id() -> str:
    return now_hkt().strftime("%Y-%m-%dT%H%M%S%z")


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
    seen: set[str] = set()
    unknown: list[str] = []
    for raw in selectors:
        key = raw.strip()
        if not key:
            continue
        hit = by_slug.get(key) or by_id.get(key) or by_name.get(key.casefold())
        if not hit:
            cands = [
                r
                for r in rows
                if key.casefold() in r["name"].casefold() or key.casefold() in r["slug"]
            ]
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


def line_count(path: Path) -> int:
    return sum(1 for _ in path.open("r", encoding="utf-8", errors="replace"))


def secret_scan(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if "[REDACTED:" in line:
            if re.search(r"sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}", line):
                hits.append(f"{path}:{i}: suspicious token beside redaction")
            continue
        if SECRET_RE.search(line) and re.search(
            r"(?i)(sk-|ghp_|xox[baprs]-|['\"][A-Za-z0-9_\-]{24,}['\"]|\=\s*[^\s\[]{16,})",
            line,
        ):
            hits.append(f"{path}:{i}: {line.strip()[:120]}")
    return hits


def dump_path(bot_id: str) -> Path:
    return DUMP_ROOT / f"{bot_id}-memory-backup.md"


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
    ts = now_hkt().isoformat()
    body_profile = (
        f"# {bot['name']} — profile\n\n"
        f"- slug: `{bot['slug']}`\n"
        f"- id: `{bot['id']}`\n"
        f"- name: {profile.get('name', bot['name'])}\n"
        f"- title: {profile.get('title', '')}\n"
        f"- description: {profile.get('description', '')}\n"
        f"- refreshed: {ts}\n"
    )
    body_spec = (
        f"# {bot['name']} — agent-spec\n\n"
        f"- id: `{bot['id']}`\n"
        f"- slug: `{bot['slug']}`\n"
        f"- 纳入: {bot['opt_in']}\n"
        f"- notes: {bot['notes']}\n"
        f"- settings_keys: {', '.join(sorted(settings.keys())) if settings else '(none)'}\n"
        f"- source: `{profile_src}`\n"
        f"- refreshed: {ts}\n"
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


def ensure_versions_header(path: Path, bot: dict) -> None:
    if path.exists():
        return
    path.write_text(
        (
            f"# Versions — {bot['name']} (`{bot['slug']}`)\n\n"
            f"Agent id: `{bot['id']}`\n\n"
            f"| version | stamped (HKT) | md5 | lines | archive path | notes |\n"
            f"|---------|---------------|-----|-------|--------------|-------|\n"
        ),
        encoding="utf-8",
    )


def next_version_number(versions_path: Path) -> int:
    if not versions_path.exists():
        return 1
    n = 0
    for line in versions_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| v") or re.match(r"^\|\s*\d+\s*\|", line):
            n += 1
        elif re.match(r"^\|\s*v?\d+", line):
            n += 1
    # count data rows only (skip header/separator)
    data = [
        ln
        for ln in versions_path.read_text(encoding="utf-8").splitlines()
        if ln.startswith("|") and not ln.startswith("| version") and not ln.startswith("|---")
    ]
    return len(data) + 1


def append_version_row(
    bot: dict,
    *,
    stamp: str,
    md5: str,
    lines: int,
    archive_rel: str | None,
    notes: str,
    dry: bool,
) -> str:
    dest_dir = BOTS_DIR / bot["slug"]
    versions = dest_dir / "VERSIONS.md"
    if dry:
        ver = "v?"
        print(f"DRY versions row {bot['slug']}: {stamp} md5={md5} lines={lines}")
        return ver
    ensure_versions_header(versions, bot)
    ver_n = next_version_number(versions)
    ver = f"v{ver_n}"
    arch = archive_rel or "—(current first write)"
    row = f"| {ver} | {stamp} | `{md5}` | {lines} | `{arch}` | {notes} |\n"
    with versions.open("a", encoding="utf-8") as f:
        f.write(row)
    print(f"versions {bot['slug']}: {ver} → {versions.relative_to(ROOT)}")
    return ver


def ingest_bot(bot: dict, stamp_date: str, skip_unchanged: bool, dry: bool) -> dict:
    """Return result dict: status, md5, lines, archive, version."""
    src = dump_path(bot["id"])
    dest_dir = BOTS_DIR / bot["slug"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = dest_dir / "archive"
    archive_dir.mkdir(exist_ok=True)
    dest = dest_dir / "MEMORY.md"

    if not src.exists():
        print(f"WAIT {bot['slug']}: missing dump {src}")
        return {"status": "missing"}

    hits = secret_scan(src)
    if hits:
        print(f"SECRET FAIL {bot['slug']}:")
        for h in hits[:20]:
            print(" ", h)
        return {"status": "secret_fail"}

    new_hash = md5_file(src)
    new_lines = line_count(src)
    if skip_unchanged and dest.exists() and md5_file(dest) == new_hash:
        print(f"SKIP {bot['slug']}: md5 {new_hash} matches MEMORY.md")
        return {
            "status": "unchanged",
            "md5": new_hash,
            "lines": new_lines,
        }

    stamp = now_hkt().strftime("%Y-%m-%dT%H%M%S")
    archive_rel = None
    prev_hash = md5_file(dest) if dest.exists() else None
    prev_lines = line_count(dest) if dest.exists() else None

    if dest.exists():
        # unique stamp — never overwrite an archive slot
        candidate = archive_dir / f"{stamp}.md"
        archive_rel = str(candidate.relative_to(ROOT))
        print(f"{'DRY ' if dry else ''}archive {dest.relative_to(ROOT)} → {archive_rel}")
        if not dry:
            shutil.copy2(dest, candidate)
            # also record previous version row if VERSIONS missing history for current
            # (current becomes archived; new current logged below)

    print(
        f"{'DRY ' if dry else ''}ingest {src.name} → {dest.relative_to(ROOT)} "
        f"(md5 {new_hash}, {new_lines} lines)"
    )
    if not dry:
        shutil.copy2(src, dest)

    note = "named ingest"
    if prev_hash:
        note = f"named ingest; previous md5 `{prev_hash}` ({prev_lines} lines)"
    ver = append_version_row(
        bot,
        stamp=stamp,
        md5=new_hash,
        lines=new_lines,
        archive_rel=archive_rel,
        notes=note,
        dry=dry,
    )
    return {
        "status": "ingested",
        "md5": new_hash,
        "lines": new_lines,
        "archive": archive_rel,
        "version": ver,
        "prev_md5": prev_hash,
    }


def tree_hash(root: Path) -> str:
    h = hashlib.md5()
    if not root.exists():
        return ""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in {"__pycache__", "node_modules", ".git", ".cache"}
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


def sync_skills(dry: bool) -> list[dict]:
    if not WORKFLOWS.is_dir():
        print("No workflows dir", file=sys.stderr)
        return []

    changed: list[dict] = []
    index_lines = [
        "# User-created skills index",
        "",
        f"Generated: {now_hkt().isoformat()} (Asia/Hong_Kong)",
        f"Source: `{WORKFLOWS}`",
        "",
        "| slug | has SKILL.md | notes |",
        "|------|--------------|-------|",
    ]
    used = []
    for folder in sorted(p for p in WORKFLOWS.iterdir() if p.is_dir()):
        if not (folder / "SKILL.md").exists():
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
            changed.append(
                {"slug": folder.name, "note": note, "md5": src_hash, "path": f"skills/{folder.name}"}
            )
        index_lines.append(f"| {folder.name} | yes | {note} |")

    index_lines += ["", f"Count: {len(used)}", ""]
    index_body = "\n".join(index_lines)
    index_path = SKILLS_DIR / "INDEX.md"
    old = index_path.read_text(encoding="utf-8") if index_path.exists() else None
    if old != index_body:
        print(f"{'DRY ' if dry else ''}write skills/INDEX.md")
        if not dry:
            SKILLS_DIR.mkdir(exist_ok=True)
            index_path.write_text(index_body, encoding="utf-8")
        changed.append({"slug": "INDEX.md", "note": "index", "md5": "", "path": "skills/INDEX.md"})
    return changed


def write_run_log(
    rid: str,
    bots: list[dict],
    ingest_results: dict[str, dict],
    skills_changed: list[dict],
    profile_paths: list[str],
    dry: bool,
) -> str | None:
    if dry:
        print(f"DRY run log meta/backup-runs/{rid}.md")
        return f"meta/backup-runs/{rid}.md"
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNS_DIR / f"{rid}.md"
    lines = [
        f"# Backup run `{rid}`",
        "",
        f"- Mode: named incremental (no fleet fan-out)",
        f"- Timezone: Asia/Hong_Kong",
        f"- Operator: 记忆管家",
        "",
        "## Bots",
        "",
    ]
    if not bots:
        lines.append("(none)")
    else:
        lines += [
            "| slug | status | version | md5 | lines | archive |",
            "|------|--------|---------|-----|-------|---------|",
        ]
        for b in bots:
            r = ingest_results.get(b["slug"], {})
            lines.append(
                f"| `{b['slug']}` | {r.get('status', '—')} | {r.get('version', '—')} | "
                f"`{r.get('md5', '—')}` | {r.get('lines', '—')} | `{r.get('archive', '—')}` |"
            )
    lines += ["", "## Profiles refreshed", ""]
    if profile_paths:
        lines += [f"- `{p}`" for p in profile_paths]
    else:
        lines.append("(none)")
    lines += ["", "## Skills", ""]
    if skills_changed:
        for s in skills_changed:
            lines.append(f"- `{s['path']}` — {s['note']}" + (f" md5 `{s['md5']}`" if s.get("md5") else ""))
    else:
        lines.append("(none)")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"run log → {path.relative_to(ROOT)}")
    return str(path.relative_to(ROOT))


def append_changelog(
    rid: str,
    bots: list[dict],
    ingest_results: dict[str, dict],
    skills_changed: list[dict],
    tag_name: str | None,
    dry: bool,
) -> None:
    date = today_hkt()
    lines = [f"## {date} named incremental backup (`{rid}`)", ""]
    ingested = [b for b in bots if ingest_results.get(b["slug"], {}).get("status") == "ingested"]
    skipped = [b for b in bots if ingest_results.get(b["slug"], {}).get("status") == "unchanged"]
    waiting = [b for b in bots if ingest_results.get(b["slug"], {}).get("status") == "missing"]
    if bots:
        lines.append(
            "- Bots named: " + ", ".join(f"`{b['slug']}`" for b in bots) + " (no fleet fan-out)."
        )
    for b in ingested:
        r = ingest_results[b["slug"]]
        prev = r.get("prev_md5")
        prev_s = f"; was `{prev}`" if prev else ""
        lines.append(
            f"- `{b['slug']}` {r.get('version')}: md5 `{r.get('md5')}` ({r.get('lines')} lines)"
            f"{prev_s}; archive `{r.get('archive')}`; VERSIONS.md updated."
        )
    if skipped:
        lines.append("- Unchanged (md5 match, skipped): " + ", ".join(f"`{b['slug']}`" for b in skipped) + ".")
    if waiting:
        lines.append("- Still waiting on dump: " + ", ".join(f"`{b['slug']}`" for b in waiting) + ".")
    if skills_changed:
        sk = [s for s in skills_changed if s["slug"] != "INDEX.md"]
        lines.append(
            "- Skills touched: "
            + ", ".join(f"`{s['slug']}` ({s['note']})" for s in sk[:40])
            + ("…" if len(sk) > 40 else "")
            + "."
        )
    if tag_name:
        lines.append(f"- Git tag: `{tag_name}`.")
    lines.append(f"- Run log: `meta/backup-runs/{rid}.md`.")
    lines.append("")
    block = "\n".join(lines) + "\n"
    path = ROOT / "CHANGELOG.md"
    old = path.read_text(encoding="utf-8") if path.exists() else "# Changelog\n\n"
    if f"(`{rid}`)" in old:
        return
    if old.startswith("# Changelog"):
        rest = old.split("\n", 1)[1].lstrip("\n")
        new = "# Changelog\n\n" + block + rest
    else:
        new = block + old
    print(f"{'DRY ' if dry else ''}update CHANGELOG.md")
    if not dry:
        path.write_text(new, encoding="utf-8")


def git_commit_push(
    paths: list[str],
    message: str,
    do_push: bool,
    tag_name: str | None,
    dry: bool,
) -> str | None:
    if dry:
        print(f"DRY commit: {message}")
        print("DRY paths:", ", ".join(paths) or "(none)")
        if tag_name:
            print(f"DRY tag: {tag_name}")
        return None

    def run(cmd: list[str]) -> None:
        print("+", " ".join(cmd))
        subprocess.check_call(cmd, cwd=ROOT)

    if not paths:
        print("Nothing to commit.")
        return None

    run(["git", "add", "--"] + paths)
    if (ROOT / "CHANGELOG.md").exists():
        run(["git", "add", "CHANGELOG.md"])
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True
    ).strip()
    if not staged:
        print("Nothing staged after add.")
        return None
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
    head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    if tag_name:
        run(["git", "tag", "-f", tag_name, "HEAD"])
    if do_push:
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
        if tag_name:
            run(
                [
                    "git",
                    "-c",
                    "credential.helper=!/usr/local/bin/gh auth git-credential",
                    "push",
                    "origin",
                    tag_name,
                    "--force",
                ]
            )
    return head


def main() -> None:
    ap = argparse.ArgumentParser(description="Named-bot incremental backup (no fleet fan-out).")
    ap.add_argument("--bots", nargs="+", default=[], help="slug / name / uuid")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--request", action="store_true")
    ap.add_argument("--ingest", action="store_true")
    ap.add_argument("--profiles", action="store_true")
    ap.add_argument("--skills", action="store_true")
    ap.add_argument("--force", action="store_true", help="Ingest even when md5 matches")
    ap.add_argument("--date", default=None, help="Archive date stamp YYYY-MM-DD (default today HKT)")
    ap.add_argument(
        "--tag",
        action="store_true",
        help="Create git tag backup-named-<run-id> (or backup-<slug>-<date> if exactly one bot ingested)",
    )
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = load_registry()
    if args.list:
        print_list(rows)
        return

    skip_unchanged = not args.force
    stamp_date = args.date or today_hkt()
    dry = args.dry_run
    rid = run_id()
    bots: list[dict] = []
    if args.bots:
        bots = resolve_bots(args.bots, rows)
        not_in = [b for b in bots if b["opt_in"] != "是"]
        if not_in:
            print("Refusing bots with 纳入≠是:", ", ".join(b["slug"] for b in not_in), file=sys.stderr)
            sys.exit(1)
    elif not args.skills:
        ap.error("Name bots with --bots …, or pass --skills / --list.")

    if args.request:
        if not bots:
            ap.error("--request needs --bots")
        request_messages(bots)
        return

    if not (args.ingest or args.profiles or args.skills or args.commit or args.push):
        print("Plan (no action). Named bots:" if bots else "Plan (skills-only possible).")
        for b in bots:
            src = dump_path(b["id"])
            mem = BOTS_DIR / b["slug"] / "MEMORY.md"
            status = "dump-ready" if src.exists() else "need-request"
            same = ""
            if src.exists() and mem.exists() and md5_file(src) == md5_file(mem):
                same = " (md5 already matches MEMORY.md)"
            vers = BOTS_DIR / b["slug"] / "VERSIONS.md"
            ver_note = f"; VERSIONS.md exists" if vers.exists() else ""
            print(f"  - {b['slug']}: {status}{same}{ver_note} → {src}")
        print("Next: --request → SendToAgent; then --ingest --profiles --tag --commit --push")
        print("Optional: --skills for local skill hash sync.")
        return

    changed_paths: list[str] = []
    ingest_results: dict[str, dict] = {}
    profile_paths: list[str] = []

    if args.profiles:
        if not bots:
            ap.error("--profiles needs --bots")
        for b in bots:
            profile_paths.extend(refresh_profile(b, dry))
        changed_paths.extend(profile_paths)

    if args.ingest:
        if not bots:
            ap.error("--ingest needs --bots")
        missing = secret_fail = 0
        for b in bots:
            result = ingest_bot(b, stamp_date, skip_unchanged, dry)
            ingest_results[b["slug"]] = result
            st = result["status"]
            if st == "ingested":
                changed_paths.append(f"bots/{b['slug']}/MEMORY.md")
                changed_paths.append(f"bots/{b['slug']}/archive")
                changed_paths.append(f"bots/{b['slug']}/VERSIONS.md")
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
            if missing == len(bots) and not args.profiles and not args.skills:
                sys.exit(2)

    skills_changed: list[dict] = []
    if args.skills:
        skills_changed = sync_skills(dry)
        changed_paths.extend(s["path"] for s in skills_changed)

    tag_name = None
    ingested_slugs = [
        s for s, r in ingest_results.items() if r.get("status") == "ingested"
    ]
    if args.tag and (ingested_slugs or skills_changed or profile_paths):
        if len(ingested_slugs) == 1 and not skills_changed:
            tag_name = f"backup-{ingested_slugs[0]}-{stamp_date}"
        else:
            tag_name = f"backup-named-{rid}"

    run_path = None
    if args.ingest or args.skills or args.profiles:
        run_path = write_run_log(
            rid, bots, ingest_results, skills_changed, profile_paths, dry
        )
        if run_path:
            changed_paths.append(run_path)
        append_changelog(rid, bots, ingest_results, skills_changed, tag_name, dry)

    head = None
    if args.commit or args.push:
        uniq = list(dict.fromkeys(changed_paths))
        msg_bots = ",".join(b["slug"] for b in bots) or "skills"
        message = f"named incremental backup {stamp_date}: {msg_bots} ({rid})"
        try:
            head = git_commit_push(uniq, message, do_push=args.push, tag_name=tag_name, dry=dry)
        except subprocess.CalledProcessError as e:
            print(f"git failed: {e}", file=sys.stderr)
            sys.exit(3)

    if ingest_results:
        print("Ingest summary:")
        for slug, r in ingest_results.items():
            extra = ""
            if r.get("version"):
                extra = f" {r['version']} md5={r.get('md5')}"
            print(f"  {slug}: {r.get('status')}{extra}")
    if tag_name:
        print(f"Tag: {tag_name}" + (f" @ {head}" if head else ""))
    if run_path:
        print(f"Run log: {run_path}")


if __name__ == "__main__":
    main()
