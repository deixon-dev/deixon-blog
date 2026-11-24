#!/usr/bin/env python3
"""Structural checks for the blog: front matter, series nav, cross-refs, evidence links.

Usage: python3 scripts/check.py   (exit 0 = all green)
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = sorted((ROOT / "blog" / "_posts").glob("*.md"))
failures = []

# Frozen evidence is byte-pinned, not allowlisted: run43-SCORES.json leaks
# absolute paths from the run that produced it, but its sha256 is published
# in part 22, so the file itself is untouchable. The exemption below holds
# only for these exact bytes; any edit re-arms the leak check AND fails for
# breaking the published hash.
FROZEN_LEAK_EXEMPT: dict[str, str] = {}   # run43's records moved to the private evidence store (2026-11-23)


def fail(msg):
    failures.append(msg)
    print(f"FAIL: {msg}")


parts = {}
for p in POSTS:
    t = p.read_text()
    if not t.startswith("---"):
        fail(f"{p.name}: missing front matter")
        continue
    fm = t.split("---")[1]
    for k in ("title:", "description:", "layout: post", "series: specfence", "date:", "part:"):
        if k not in fm:
            fail(f"{p.name}: front matter lacks {k}")
    m = re.search(r"^part:\s*(\d+)\s*$", fm, re.M)
    if m:
        parts[int(m.group(1))] = p
    if "{% include series.html %}" not in t:
        fail(f"{p.name}: missing series nav include")

names = {p.stem for p in POSTS}
for p in POSTS:
    for ref in re.findall(r"post_url ([\d\-a-z]+)", p.read_text()):
        if ref not in names:
            fail(f"{p.name}: post_url {ref} resolves to nothing")

if sorted(parts) != list(range(1, len(POSTS) + 1)):
    fail(f"part numbers are not 1..{len(POSTS)}: {sorted(parts)}")
for n, p in parts.items():
    if f"Part {n} of {len(POSTS)}" not in p.read_text():
        fail(f"{p.name}: header is not 'Part {n} of {len(POSTS)}' for part {n}")

nav = (ROOT / "blog" / "_includes" / "series.html").read_text()
if 'sort: "part"' not in nav:
    fail('series.html: nav must sort by "part" (filenames share dates, so path order is not series order)')

for p in POSTS:
    for m in re.findall(r"specfence-blog/(?:tree|blob)/main/([^)]*)", p.read_text()):
        if not (ROOT / m).exists():
            fail(f"{p.name}: evidence link {m} missing")

for f in list((ROOT / "blog").rglob("*.md")) + list((ROOT / "evidence").rglob("*.md")) \
        + list((ROOT / "evidence").rglob("*.json")) + list((ROOT / "evidence").rglob("*.log")):
    if "/Users/" in f.read_text():
        rel = str(f.relative_to(ROOT))
        pinned = FROZEN_LEAK_EXEMPT.get(rel)
        if pinned is not None and hashlib.sha256(f.read_bytes()).hexdigest() == pinned:
            print(f"INFO: {rel}: absolute path leak exempt (frozen bytes, sha256 {pinned[:12]}...)")
        else:
            fail(f"{rel}: absolute path leak")

for rel, pinned in FROZEN_LEAK_EXEMPT.items():
    f = ROOT / rel
    if f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() != pinned:
        fail(f"{rel}: frozen evidence changed; published sha256 {pinned[:12]}... no longer matches")

print(f"{len(POSTS)} posts checked, {len(failures)} failure(s)")
sys.exit(1 if failures else 0)
