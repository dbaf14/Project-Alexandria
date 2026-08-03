#!/usr/bin/env python3
"""
update_readme.py

Regenerates the "Overview" section in README.md from meta/statistics.json.
Runs as the final step of the pipeline (after build_index.py), so the
numbers always reflect the current state of category/ and connections/.

The section is delimited by two HTML comment markers in README.md:

    <!-- OVERVIEW:START -->
    ...
    <!-- OVERVIEW:END -->

Everything between (and including) these markers is replaced on every run.
Do not edit the content between the markers by hand — it will be
overwritten on the next pipeline run.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATS_FILE = ROOT / "meta" / "statistics.json"
README_FILE = ROOT / "README.md"

START_MARKER = "<!-- OVERVIEW:START -->"
END_MARKER = "<!-- OVERVIEW:END -->"

# Human-readable label per entry "type", used to build lines like
# "12 from GitHub". Falls back to "of type '<type>'" for unknown types.
TYPE_LABELS = {
    "github": "from GitHub",
    "paper": "from science papers",
    "patent": "from patents",
    "documentation": "from documentation",
    "dataset": "from datasets",
    "research_project": "from research projects",
    "historical_document": "from historical documents",
    "other": "from other sources",
}


def build_overview_block(stats):
    total = stats.get("total_entries", 0)
    by_category = stats.get("by_category", {})
    by_type = stats.get("by_type", {})
    num_categories = len([c for c, count in by_category.items() if count > 0])

    lines = [START_MARKER, "## Overview", ""]
    lines.append(
        "_Automatically updated after each pipeline run "
        "(`scripts/update_readme.py`) — do not edit this section by hand._"
    )
    lines.append("")
    lines.append(
        f"**Currently {total} analyzed {'entry' if total == 1 else 'entries'} "
        f"available in {num_categories} categor{'y' if num_categories == 1 else 'ies'}.**"
    )
    lines.append("")

    if total == 0:
        lines.append(
            "_No entries yet. Be the first to add one — "
            "see [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)._"
        )
    else:
        for type_key, count in sorted(by_type.items(), key=lambda kv: -kv[1]):
            if count <= 0:
                continue
            label = TYPE_LABELS.get(type_key, f"of type '{type_key}'")
            lines.append(f"- {count} {label}")

    lines.append(END_MARKER)
    return "\n".join(lines)


def main():
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        stats = json.load(f)

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    block = build_overview_block(stats)

    if START_MARKER in content and END_MARKER in content:
        start_idx = content.index(START_MARKER)
        end_idx = content.index(END_MARKER) + len(END_MARKER)
        content = content[:start_idx] + block + content[end_idx:]
    else:
        # Markers missing (e.g. someone removed them) - insert right after
        # the main title so the overview stays at the very top.
        title_marker = "# Project Alexandria"
        if title_marker in content:
            idx = content.index(title_marker)
            insert_at = content.index("\n\n", idx) + 2
            content = content[:insert_at] + block + "\n\n" + content[insert_at:]
        else:
            content = block + "\n\n" + content

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"README.md overview updated: {stats.get('total_entries', 0)} entries.")


if __name__ == "__main__":
    main()
