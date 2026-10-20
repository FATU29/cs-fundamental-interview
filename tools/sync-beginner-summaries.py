#!/usr/bin/env python3
"""Use each article's plain-language sentence on topic cards."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
summaries = {}
for path in ROOT.glob("*/*.md"):
    if path.parent.name in {"assets", "tools", "_template"}:
        continue
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Nói đơn giản:**"):
            summaries[path.stem] = line.split(":**", 1)[1].strip()
            break

registry = ROOT / "registry.js"
lines = registry.read_text(encoding="utf-8").splitlines()
current_slug = None
changed = 0
for i, line in enumerate(lines):
    match = re.search(r'slug: "([^"]+)"', line)
    if match:
        current_slug = match.group(1)
    if current_slug and "summary:" in line and current_slug in summaries:
        prefix = line.split("summary:", 1)[0] + "summary: "
        # Registry summaries are plain strings, so JSON quoting is safe JS here.
        lines[i] = prefix + json.dumps(summaries[current_slug], ensure_ascii=False) + ","
        changed += 1
        current_slug = None
registry.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"updated {changed} registry summary/ies")
